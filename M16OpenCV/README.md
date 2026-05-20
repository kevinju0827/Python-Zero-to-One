# M16 OpenCV (Computer Vision)

## The "Why?"

For everything in this course so far, your scripts have manipulated text, numbers, JSON, or rows of database data. But the world is full of *images*—product photos in an online store, scans of receipts, security camera footage, the screenshots you just learned to capture in M14. Until a computer can "see" an image, it can do nothing with it except move the file around.

**OpenCV** (Open Source Computer Vision Library) is the world's most widely-used library for teaching computers to read images. It is the same toolkit that powers Instagram filters, QR-code scanners at supermarket checkouts, license-plate readers on highways, and the early stages of every modern self-driving car. The library itself is C++ at its core—but the Python bindings (`opencv-python`) are so well-designed that, in a few dozen lines, you can build tools that would have been a graduate research project two decades ago.

In this module, you will learn how a computer represents an image (as a giant grid of numbers), and then use OpenCV to perform the operations that show up in nearly every real vision project: loading and saving, resizing, color conversion, drawing on top of an image, applying filters, and locating things. This module is the visual sibling of everything you have already built—it lets your automations *see*, not just type.

## Goals

By the end of this module, you should be able to:

* Install `opencv-python` and load an image from disk.
* Explain how an image is represented as a 3-dimensional NumPy array of pixel values.
* Distinguish between **BGR** (OpenCV's default order) and **RGB**, and convert between them.
* Use `cv2.imread`, `cv2.imshow`, `cv2.imwrite`, `cv2.waitKey`, and `cv2.destroyAllWindows`.
* Resize, crop, and rotate images.
* Convert an image to grayscale.
* Apply common filters: Gaussian blur, edge detection (Canny).
* Draw rectangles, circles, and text onto an image.
* Process a folder of images in a batch.
* Recognize when OpenCV is the right tool and when a higher-level library (Pillow, scikit-image) might be simpler.

## Core Concepts

### An Image Is Just Numbers

When OpenCV loads a color image, you get a 3-dimensional grid of integers:

* The first dimension is **height** (rows of pixels).
* The second dimension is **width** (columns of pixels).
* The third dimension is the **color channel**—three values per pixel.

```python
import cv2

img = cv2.imread("photo.jpg")
print(img.shape)   # e.g., (1080, 1920, 3) — height, width, channels
print(img[0, 0])   # The pixel at the top-left, e.g., [27, 45, 200]
```

Each value is a single byte (0–255). A pure red pixel in OpenCV would be `[0, 0, 255]`—Blue, Green, then Red.

---

### BGR vs. RGB: The Most Common Pitfall

Most of the world (your screen, your design tools, every web standard) uses **RGB** order. OpenCV, for historical reasons, uses **BGR**. This means an image you display with `cv2.imshow` looks fine, but the same image plotted with `matplotlib` (which expects RGB) will have its red and blue channels swapped, making faces look like aliens.

When you mix libraries, convert explicitly:

```python
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

Forgetting this is so common that it is essentially every beginner's first OpenCV bug.

---

### The Standard Workflow

Almost every OpenCV script follows the same five steps:

1. **Load**: `img = cv2.imread("input.jpg")`. Returns `None` if the file is missing—always check for this.
2. **(Optional) Preprocess**: convert to grayscale, blur to reduce noise, resize for speed.
3. **Transform**: apply the actual operation (rotate, detect edges, draw a shape, etc.).
4. **Show or save**:
   * `cv2.imshow("window name", img)` opens a window.
   * `cv2.imwrite("output.jpg", img)` writes to disk.
5. **Clean up**: `cv2.waitKey(0)` waits for a key press; `cv2.destroyAllWindows()` closes preview windows.

```python
import cv2

img = cv2.imread("input.jpg")
if img is None:
    raise FileNotFoundError("input.jpg not found")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("output.jpg", gray)
```

---

### Geometric Operations

The everyday transformations you will reach for first:

```python
# Resize to an explicit width and height
small = cv2.resize(img, (640, 480))

# Resize by a scale factor (50% smaller)
half = cv2.resize(img, None, fx=0.5, fy=0.5)

# Crop is just NumPy slicing: image[y_start:y_end, x_start:x_end]
top_left = img[0:200, 0:200]

# Rotate by an explicit 90 degrees
rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
```

Remember the slicing order: **y first, then x** (rows before columns).

---

### Filters

Filters either smooth an image (blur) or extract features from it (edges, sharpness):

```python
# Gaussian blur—smooths noise and is the first step of many algorithms.
# Kernel size (5, 5) must be odd numbers; larger = blurrier.
blurred = cv2.GaussianBlur(img, (5, 5), 0)

# Edge detection: returns a binary image where edges are white and everything else is black.
# 100 and 200 are the lower/upper thresholds—tune them per image.
edges = cv2.Canny(img, 100, 200)
```

Edge detection is the foundation of many "the computer can see" tasks: finding a document on a desk to scan it, isolating a license plate, or counting objects on a conveyor belt.

---

### Drawing on Images

You can draw shapes and text directly on top of an image. The functions modify the image in place and return the modified array:

```python
# Rectangle: (top-left corner, bottom-right corner, BGR color, thickness)
cv2.rectangle(img, (50, 80), (250, 280), (0, 255, 0), 3)

# Circle: (center, radius, color, thickness)
cv2.circle(img, (150, 150), 40, (0, 0, 255), 2)

# Text: (image, text, bottom-left of text, font, size, color, thickness)
cv2.putText(img, "Hello!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
```

Drawing is how you visualize detection results. If your script claims it found a face, drawing a green rectangle around it lets you (and your user) verify with their own eyes.

---

### Batch Processing

A single image is rarely interesting. A folder of 200 is. Combine OpenCV with the `os` module (M07) to process every file in a directory:

```python
import os, cv2

input_dir = "raw"
output_dir = "processed"
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if not filename.lower().endswith((".jpg", ".png")):
        continue
    img = cv2.imread(os.path.join(input_dir, filename))
    if img is None:
        continue
    thumb = cv2.resize(img, (320, 240))
    cv2.imwrite(os.path.join(output_dir, filename), thumb)
```

This is the pattern behind "I processed 10,000 photos in two minutes" success stories—it is just a `for` loop and a transformation.

---

## Guided Practice

We will build a **batch thumbnail generator**—a script that takes a folder of photos and produces uniformly-sized, grayscale, watermarked thumbnails in seconds. It exercises every OpenCV concept above: loading with a `None` check, resizing, color conversion, drawing text, batch processing, and saving.

**Scenario**: A small blog needs a thumbnail at exactly 400×300 pixels in grayscale with a copyright watermark for every post. In Photoshop this would be minutes per image; with OpenCV the whole folder finishes in under a second.

**Step 1: Prepare the input and output folders.** Use `os.makedirs("originals", exist_ok=True)` and `os.makedirs("thumbnails", exist_ok=True)`. Drop at least three `.jpg` or `.png` files into `originals/` before running.

**Step 2: Filter to image files.** Walk `os.listdir("originals")` but only keep filenames ending in `(".jpg", ".jpeg", ".png", ".bmp", ".webp")`. Trying to read README.md as an image with `cv2.imread` would silently return `None`.

**Step 3: Process each file in a `for` loop.** The transformation pipeline:
1. `cv2.imread(path)` — and **skip with a warning if it returns `None`** (a corrupt or unsupported file shouldn't crash the whole batch).
2. `cv2.resize(img, (400, 300))` — uniform output size.
3. `cv2.cvtColor(thumb, cv2.COLOR_BGR2GRAY)` — drop colour information.
4. `cv2.putText(...)` to stamp a copyright string in the bottom-right corner. Use `cv2.getTextSize()` to position the text precisely so it never falls off the edge.
5. `cv2.imwrite(target_path, gray)` — save into `thumbnails/`.

**Step 4: Inspect the output.** Open the `thumbnails/` folder and confirm every image is 400×300, grayscale, and watermarked. You have just replicated, in ~25 lines, the kind of image pipeline that used to be a paid SaaS product.

The full implementation is in `thumbnail_generator_example.py`. The pattern—`for filename in folder: read → transform → write`—is the foundation of every batch image job you will ever build.

---

## Checkpoints

* [ ] **Photo Booth Mood Frame**:
      Build a tool that loads a photo and decorates it with a colored border whose color depends on the photo itself. For each image:
      1. Compute the **mean brightness** of the grayscale version (`gray.mean()`).
      2. If the brightness is below 80, treat the image as "moody" and add a thick **blue** border. Between 80 and 160 → green. Above 160 → orange.
      3. Use `cv2.copyMakeBorder(...)` to add a 40-pixel border in the chosen color.
      4. Save the framed image with a suffix, e.g., `sunset_framed.jpg`.
      Run it on at least three different photos and confirm each gets a different border color.
      *(Hint: the technique of "compute a metric, branch on it, render a result" is the recipe behind most data-driven creative tooling—from Spotify's color-changing now-playing screens to Apple Photos' auto-album themes. You are now doing the same thing.)*

* [ ] **QR Code Snapper**:
      Combine M14 + M16. Build a script that:
      1. Takes a screenshot of the entire screen (recall M14: `pyautogui.screenshot("screen.png")`).
      2. Loads it with OpenCV.
      3. Uses OpenCV's built-in QR code detector: `detector = cv2.QRCodeDetector()`, then `data, points, _ = detector.detectAndDecode(img)`.
      4. If a QR code is found, prints the decoded text and saves a copy of the screenshot with a green rectangle drawn around the QR region. If no QR code is found, prints a polite "no QR code visible right now" message.
      Test it by displaying a QR code on your phone screen and holding it in front of your laptop camera (or simply by displaying one in your browser on another part of your monitor). When it works, you have built the same scanning capability that powers payment apps and event check-in tools.

* [ ] **Personal Daily Time-Lapse**:
      Combine M11 + M14 + M16 for a finale project that uses four modules' worth of skills.
      1. (M14 + M11) During a work session, capture a screenshot every 30 seconds into a `frames/` folder. Frames should be named `frame_000001.png`, `frame_000002.png`, … so they sort correctly.
      2. (M16) Write a second, separate script that:
         * Reads every frame from `frames/` in order.
         * Resizes each to 1280×720 for compactness.
         * Writes them out as a single MP4 video using `cv2.VideoWriter`. Use 24 fps so a one-hour session collapses into a ~5-second time-lapse.
      3. Print the duration of the input session and the duration of the output video.
      *(Hint: this is the entire build pipeline behind every "I made a 5-minute timelapse of building my game" video you have seen on YouTube. When you finish it, take a step back: in M01 you couldn't print `"hello"`—and here at the end of M16 you have written a script that captures, processes, and re-encodes hours of your computer activity into a watchable video. That arc is the whole point of "Zero to One.")*
