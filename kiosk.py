"""BCREC Faculty Attendance Kiosk with passive anti-spoofing and active liveness."""
import os
import time
from collections import deque
from datetime import datetime
import cv2
import numpy as np
from anti_spoof import AntiSpoofEngine, REAL_THRESHOLD, TEMPORAL_FRAMES
from lite_core import FaceEngine, ensure_db, get_faculty, identify, largest_face, load_classifier, mark_attendance, open_camera
from liveness import LivenessChallenge

DETECT_EVERY = int(os.environ.get("DETECT_EVERY", "2"))
MIN_FACE_PX = int(os.environ.get("MIN_FACE_PX", "90"))
EMB_FRAMES = int(os.environ.get("EMB_FRAMES", "2"))
RESULT_HOLD = float(os.environ.get("RESULT_HOLD", "3"))
if os.name != "nt":
    cv2.setNumThreads(int(os.environ.get("OPENCV_THREADS", "2")))
FULLSCREEN = os.environ.get("KIOSK_FULLSCREEN", "1") == "1"
GREEN = (60, 170, 60)
AMBER = (40, 170, 240)
RED = (60, 60, 200)
WHITE = (255, 255, 255)
NAVY = (32, 22, 11)

def put(img, text, org, scale=0.8, color=WHITE, thick=2):
    cv2.putText(img, text, org, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thick, cv2.LINE_AA)

def reset_security(liveness, embeddings, spoof_history):
    embeddings.clear()
    spoof_history.clear()
    liveness.reset()

def build_result(res):
    if not res["accepted"]:
        return {"title": "Not recognised", "line": "Please try again", "color": RED}
    fac = get_faculty(res["faculty_id"])
    if fac is None:
        return {"title": "Unknown ID", "line": res["faculty_id"], "color": RED}
    status, t, late = mark_attendance(fac["id"])
    labels = {
        "checkin_first": "CHECK-IN" + ("  (LATE)" if late else ""),
        "checkin": "CHECK-IN (re-entry)",
        "checkout": "CHECK-OUT",
        "cooldown": "Already recorded",
    }
    return {"title": fac["name"], "line": f"{labels[status]}   {t}",
            "color": AMBER if late or status == "cooldown" else GREEN}

def main():
    ensure_db()
    bundle = load_classifier()
    if bundle is None:
        raise SystemExit("No classifier found. Run: python train_lite.py")
    engine = FaceEngine()
    anti = AntiSpoofEngine()
    liveness = LivenessChallenge()
    cap = open_camera()
    win = "BCREC Faculty Attendance"
    cv2.namedWindow(win, cv2.WINDOW_NORMAL)
    if FULLSCREEN:
        cv2.setWindowProperty(win, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    faces = np.empty((0, 15), np.float32)
    embeddings = []
    spoof_history = deque(maxlen=TEMPORAL_FRAMES)
    liveness_passed = False
    liveness_state = {"passed": False, "failed": False, "prompt": "Look at the camera", "progress": "0/3"}
    result = None
    result_until = 0.0
    last_spoof_text = "Anti-spoof: waiting"
    frame_i = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                time.sleep(0.05)
                continue
            frame_i += 1
            now = time.time()
            if now >= result_until:
                result = None
                if frame_i % DETECT_EVERY == 0:
                    faces = engine.detect_fast(frame)
                    if len(faces) != 1:
                        reset_security(liveness, embeddings, spoof_history)
                        liveness_passed = False
                        last_spoof_text = "Anti-spoof: waiting for face" if len(faces) == 0 else "ONE PERSON ONLY"
                    else:
                        face = largest_face(faces)
                        if face is None or float(face[2]) < MIN_FACE_PX:
                            reset_security(liveness, embeddings, spoof_history)
                            liveness_passed = False
                            last_spoof_text = "Move closer"
                        else:
                            anti_result = anti.score(frame, face)
                            if anti_result is None:
                                reset_security(liveness, embeddings, spoof_history)
                                liveness_passed = False
                                last_spoof_text = "Anti-spoof unavailable"
                            else:
                                spoof_history.append(anti_result["real"])
                                median_real = float(np.median(np.asarray(spoof_history)))
                                passive_real = len(spoof_history) >= TEMPORAL_FRAMES and median_real >= REAL_THRESHOLD
                                last_spoof_text = f"Anti-spoof REAL {median_real:.2f}" if passive_real else f"Anti-spoof {median_real:.2f}"
                                if not passive_real:
                                    embeddings.clear()
                                    liveness_passed = False
                                else:
                                    # We rely entirely on the passive MiniFAS Anti-Spoof model.
                                    liveness_passed = True
                                    if liveness_passed:
                                        embeddings.append(engine.embed(frame, face))
                                        if len(embeddings) >= EMB_FRAMES:
                                            mean = np.mean(embeddings, axis=0)
                                            norm = np.linalg.norm(mean)
                                            embeddings.clear()
                                            if norm > 0:
                                                mean /= norm
                                                res = identify(bundle, mean)
                                                result = build_result(res)
                                                result_until = time.time() + RESULT_HOLD
                                                print(f"[scan] {res.get('faculty_id')} conf={res.get('confidence', 0):.2f} cos={res.get('cosine', 0):.2f} anti={median_real:.2f} accepted={res.get('accepted')}")
                                                reset_security(liveness, embeddings, spoof_history)
                                                liveness_passed = False
            for f in faces:
                x, y, w, h = map(int, f[:4])
                box_color = GREEN if liveness_passed else AMBER
                cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)
            H, W = frame.shape[:2]
            cv2.rectangle(frame, (0, 0), (W, 55), NAVY, -1)
            put(frame, "BCREC Faculty Attendance", (10, 34), 0.75)
            put(frame, datetime.now().strftime("%d %b %Y  %H:%M:%S"), (W - 300, 34), 0.60)
            cv2.rectangle(frame, (0, H - 130), (W, H), NAVY, -1)
            
            if result:
                put(frame, result["title"], (12, H - 78), 0.95, result["color"], 2)
                put(frame, result["line"], (12, H - 40), 0.75, result["color"], 2)
            elif len(faces) == 0:
                put(frame, "Look at the camera", (12, H - 72), 0.72, WHITE, 2)
                put(frame, last_spoof_text, (12, H - 32), 0.60, AMBER, 2)
            elif not liveness_passed:
                # Replaced the active prompt with a fast static verifying prompt
                put(frame, "Analyzing liveness...", (12, H - 72), 0.70, AMBER, 2)
                put(frame, last_spoof_text, (12, H - 32), 0.58, WHITE, 2)
            else:
                put(frame, "Recognizing face...", (12, H - 72), 0.68, GREEN, 2)
                put(frame, last_spoof_text, (12, H - 32), 0.58, WHITE, 2)
            cv2.imshow(win, frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q")):
                break
            if key == ord("r"):
                bundle = load_classifier() or bundle
                print("[kiosk] classifier reloaded")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
