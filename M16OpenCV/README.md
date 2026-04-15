# M16 OpenCV (Computer Vision)

## The "Why?"

Computers don't see images the way humans do; they see huge grids of numbers representing color intensity. **OpenCV** (Open Source Computer Vision Library) is the industry-standard tool for teaching computers how to "see." It is used for everything from Instagram filters and QR code scanners to self-driving cars and medical imaging. By learning OpenCV, you can write scripts that can automatically analyze, edit, and understand visual data.

## Goals

Understand how images are represented in Python as numerical arrays, learn how to load and display images, and perform basic image manipulations like resizing and color conversion.

## Core Concepts

### Images as Arrays
In Python, an image is represented as a massive list of lists (a 3D array). Each point in the grid is a **Pixel**, which contains three numbers representing color: Blue, Green, and Red.

### BGR vs RGB
**Warning!** While most of the world uses **RGB** (Red, Green, Blue), OpenCV uses **BGR** (Blue, Green, Red) by default. This is a common pitfall to remember when processing colors or displaying images in other libraries.

### Basic Processing Workflow
Most computer vision tasks follow a similar "Pipeline":
1. **Load** the original image.
2. **Convert** to Grayscale (to simplify the data for the computer).
3. **Apply** a transformation (resize, filter, detect).
4. **Save** or **Show** the final result.

## Guided Practice

We will write a script that loads a photo, converts it to grayscale (black and white), and saves the result as a new file.

*   **Step 1: Install OpenCV**
    ```bash
    pip install opencv-python
    ```

*   **Step 2: Create `image_processor_example.py`**
    (Make sure you have an image file named `sample_input.jpg` in the same folder!)
    ```python
    import cv2
    import os

    # Move to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 1. Load the image from your folder
    img = cv2.imread('sample_input.jpg')

    if img is None:
        print("Error: Could not find 'sample_input.jpg'. Please place an image in this folder.")
    else:
        # 2. Convert the color image to Grayscale (B&W)
        # This makes it easier for many computer vision algorithms to process
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 3. Show both images in windows
        cv2.imshow('Original Color', img)
        cv2.imshow('Black and White', gray_img)

        # 4. Save the new grayscale image to a file
        cv2.imwrite('output_grayscale.jpg', gray_img)
        print("Successfully saved 'output_grayscale.jpg'")

        # Wait for the user to press any key before closing the windows
        print("Press any key on an image window to exit.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    ```

## Checkpoints

* [ ] **The Resizer**:
    Use `cv2.resize()` to shrink an image to exactly 50% of its original size and save it as `thumbnail.jpg`.
* [ ] **Face Detector (Intro)**:
    Research how to use a "Haar Cascade" (a pre-trained file like `haarcascade_frontalface_default.xml`) to draw a green rectangle around a face in a photo.
* [ ] **The Privacy Blur**:
    Combine this with M14 (PyAutoGUI). Write a script that takes a screenshot of your desktop, then uses OpenCV's `cv2.GaussianBlur()` to blur the entire image so no private information is readable before saving it.