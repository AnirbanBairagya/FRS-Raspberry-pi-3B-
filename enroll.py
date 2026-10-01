"""
Native faculty enrollment.

Three guided camera captures are taken:
  1. Straight
  2. Slightly left
  3. Slightly right

This is intentionally native-camera based rather than browser Base64 capture,
so it is suitable for a Raspberry Pi kiosk.
"""

import argparse
import os
import sqlite3
import uuid

import cv2
import numpy as np

from lite_core import (
    COSINE_THRESHOLD,
    DB_PATH,
    KNOWN_FACES_DIR,
    FaceEngine,
    build_reference_embeddings,
    ensure_db,
    get_faculty,
    largest_face,
    open_camera,
)

PROMPTS = [
    "Look STRAIGHT at the camera",
    "Turn slightly LEFT",
    "Turn slightly RIGHT",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--dept", default="")
    ap.add_argument("--designation", default="")
    ap.add_argument("--email", default="")
    ap.add_argument("--phone", default="")
    ap.add_argument("--camera", default=None)
    args = ap.parse_args()

    ensure_db()
    os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

    if get_faculty(args.id):
        raise SystemExit(f"Faculty ID {args.id} already exists. Nothing was changed.")

    engine = FaceEngine()
    cap = open_camera(args.camera)
    shots = []
    saved_paths = []

    try:
        for i, prompt in enumerate(PROMPTS):
            while True:
                ok, frame = cap.read()
                if not ok:
                    continue

                faces = engine.detect_fast(frame)
                view = frame.copy()

                for f in faces:
                    x, y, w, h = map(int, f[:4])
                    cv2.rectangle(
                        view,
                        (x, y),
                        (x + w, y + h),
                        (0, 200, 0),
                        2,
                    )

                msg = "OK - press SPACE" if len(faces) == 1 else "Need exactly one face"
                cv2.putText(
                    view,
                    f"[{i + 1}/3] {prompt}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2,
                )
                cv2.putText(
                    view,
                    msg,
                    (10, 65),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )
                cv2.imshow("BCREC Faculty Enrollment", view)

                key = cv2.waitKey(1) & 0xFF
                if key == 27:
                    raise SystemExit("Enrollment aborted. No database record was created.")

                if key == 32 and len(faces) == 1:
                    shots.append(frame.copy())
                    break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    # Duplicate check happens BEFORE any image is written to disk.
    print("Checking for duplicate faces...")
    existing = build_reference_embeddings(engine)

    for shot in shots:
        face = largest_face(engine.detect(shot))
        if face is None:
            raise SystemExit("A captured photo no longer contains a detectable face. Nothing was saved.")
        emb = engine.embed(shot, face)
        for fid, refs in existing.items():
            if len(refs) and float(np.max(refs @ emb)) >= COSINE_THRESHOLD:
                raise SystemExit(
                    f"This face matches enrolled faculty {fid}. Nothing was saved."
                )

    uid = uuid.uuid4().hex[:8]

    try:
        for i, shot in enumerate(shots):
            path = os.path.join(
                KNOWN_FACES_DIR,
                f"{args.id}_{uid}_{i}.jpg",
            )
            if not cv2.imwrite(path, shot):
                raise RuntimeError(f"Could not write {path}")
            saved_paths.append(path)

        conn = sqlite3.connect(DB_PATH)
        try:
            conn.execute(
                """
                INSERT INTO faculty
                (faculty_id, name, department, designation, image_path, email, phone, active, created_at)
                VALUES (?,?,?,?,?,?,?,?,datetime('now'))
                """,
                (
                    args.id,
                    args.name,
                    args.dept,
                    args.designation,
                    saved_paths[0],
                    args.email,
                    args.phone,
                    1,
                ),
            )
            conn.commit()
        finally:
            conn.close()
    except Exception:
        for path in saved_paths:
            try:
                os.remove(path)
            except OSError:
                pass
        raise

    print(
        f"Enrolled {args.name} ({args.id}) with 3 photos.\n"
        "Run train_lite.py before expecting the new face to be recognized."
    )


if __name__ == "__main__":
    main()
