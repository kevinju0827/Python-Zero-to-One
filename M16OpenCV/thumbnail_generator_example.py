"""Guided Practice 1 — Batch generate watermarked grayscale thumbnails.

Scenario: every blog post needs a 400x300 grayscale thumbnail with a
copyright watermark in the corner. Photoshop takes minutes per image;
OpenCV finishes the whole folder in under a second.

Put a few .jpg/.png files into ./originals/ before running.
"""

import os

import cv2

os.chdir(os.path.dirname(os.path.abspath(__file__)))

INPUT_DIR = "originals"
OUTPUT_DIR = "thumbnails"
TARGET_SIZE = (400, 300)   # (width, height)
WATERMARK = "(C) 2026 YOURNAME"

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Filter to image extensions so we don't try to read README.md as a picture.
image_exts = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(image_exts)]

if not files:
    print(f"No images found in '{INPUT_DIR}/'. Drop some .jpg/.png files there and re-run.")
    raise SystemExit(0)

processed = 0
for filename in files:
    source_path = os.path.join(INPUT_DIR, filename)
    img = cv2.imread(source_path)
    if img is None:
        print(f"[skip] could not read {filename}")
        continue

    # 1. Resize to a consistent thumbnail size.
    thumb = cv2.resize(img, TARGET_SIZE)

    # 2. Convert to grayscale. cvtColor returns a 2D array (no channel dim).
    gray = cv2.cvtColor(thumb, cv2.COLOR_BGR2GRAY)

    # 3. Stamp a watermark in the bottom-right.
    #    Position is the BOTTOM-LEFT corner of the text, hence the offset math.
    h, w = gray.shape
    text_size, _ = cv2.getTextSize(WATERMARK, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    text_w, text_h = text_size
    origin = (w - text_w - 10, h - 10)
    cv2.putText(gray, WATERMARK, origin, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1, cv2.LINE_AA)

    # 4. Save with the same filename in the output folder.
    target_path = os.path.join(OUTPUT_DIR, filename)
    cv2.imwrite(target_path, gray)
    processed += 1
    print(f"[ok] {filename} -> {target_path}")

print(f"\nDone. {processed} thumbnail(s) written to {OUTPUT_DIR}/")
