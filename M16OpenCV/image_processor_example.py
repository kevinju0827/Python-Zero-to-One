import cv2
import os

# 1. Set working directory to the script location
# This ensures that 'sample_input.jpg' is searched for in the correct folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 2. Load the input image
# Replace 'sample_input.jpg' with an actual file on your computer to test this script
img_name = 'sample_input.jpg'
image = cv2.imread(img_name)

# 3. Handle errors if the file is missing
if image is None:
    print(f"Error: Could not find or open '{img_name}'.")
    print("Please place a JPEG image file in this folder and rename it to 'sample_input.jpg'.")
else:
    # 4. Perform Image Manipulation
    # Convert BGR (color) image to Grayscale (B&W)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 5. Display the results in separate windows
    cv2.imshow('Original Image', image)
    cv2.imshow('Grayscale Version', gray_image)

    # 6. Save the processed image back to disk
    output_name = 'output_grayscale.jpg'
    cv2.imwrite(output_name, gray_image)
    print(f"Success: Processed image saved as '{output_name}'")

    # 7. Finalize
    print("Click on an image window and press any key to close.")
    cv2.waitKey(0) # Wait forever for a key press
    cv2.destroyAllWindows() # Close all GUI windows
