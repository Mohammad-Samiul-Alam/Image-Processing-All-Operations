
import cv2  # OpenCV: Used for image processing
import matplotlib.pyplot as plt  # Used to display images and graphs
import numpy as np  # Used for creating arrays and matrices

# 1. Read Image
img = cv2.imread("./color_image.png")  # Reads image in BGR format

# Check whether the image exists
if img is None:
    print("Image not found!")
    exit()

# 2. Convert Image
color_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Converts BGR to RGB for correct color display
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Converts color image to grayscale

# 3. Create Kernel
kernel = np.ones((3, 3), np.uint8)  # Creates a 3x3 matrix filled with 1s

# 4. Minimum Filter (Erosion)
min_img = cv2.erode(color_img, kernel)  # Selects minimum pixel values from the neighborhood

# 5. Maximum Filter (Dilation)
max_img = cv2.dilate(color_img, kernel)  # Selects maximum pixel values from the neighborhood

# 6. Sobel Edge Detection - X Direction
sobel_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
# CV_64F = 64-bit floating-point output
# 1 = Detects changes in X direction
# 0 = No derivative in Y direction
# ksize=3 = Uses a 3x3 Sobel kernel

# 7. Sobel Edge Detection - Y Direction
sobel_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)
# 0 = No derivative in X direction
# 1 = Detects changes in Y direction
# ksize=3 = Uses a 3x3 Sobel kernel

# 8. Combine Sobel X and Y
sobel = cv2.magnitude(sobel_x, sobel_y)
# Calculates total edge strength using sqrt(X² + Y²)

# 9. Convert Sobel Images for Display
sobel_x = cv2.convertScaleAbs(sobel_x)  # Converts negative and positive values to 8-bit absolute values
sobel_y = cv2.convertScaleAbs(sobel_y)  # Converts Sobel Y into 8-bit image
sobel = cv2.convertScaleAbs(sobel)  # Converts combined Sobel into 8-bit image

# 10. Store Images in a List
panels = [
    (1, color_img, "Original Image", None),
    (2, min_img, "Minimum Filter Image", None),
    (3, max_img, "Maximum Filter Image", None),
    (4, sobel_x, "Sobel X", "gray"),
    (5, sobel_y, "Sobel Y", "gray"),
    (6, sobel, "Sobel", "gray")
]

# 11. Create Figure
plt.figure(figsize=(12, 6))  # Sets figure width=12 inches and height=6 inches

# 12. Display Images Using Loop
for n, image, title, cmap in panels:

    plt.subplot(3, 3, n)  # Creates a subplot in a 3x3 grid
    plt.imshow(image, cmap=cmap)  # Displays image with the selected color map
    plt.title(title)  # Sets image title
    plt.axis("off")  # Hides X and Y axes
    plt.gca().set_box_aspect(1)  # Makes the subplot box square

# 13. RGB Histogram
plt.subplot(3, 3, (7, 9))  # Uses the last row (columns 1 to 3)

colors = ('r', 'g', 'b')  # Defines Red, Green and Blue colors

# Calculate and Display RGB Histogram
for i, color in enumerate(colors):

    hist = cv2.calcHist([color_img], [i], None, [256], [0, 256])
    # [color_img] = Input image
    # [i] = Channel index (0=Red, 1=Green, 2=Blue)
    # None = No mask (uses the entire image)
    # [256] = Number of histogram bins
    # [0, 256] = Pixel intensity range

    plt.plot(hist, color=color)  # Draws histogram using RGB colors

# 14. Histogram Settings
plt.xlim(0, 256)  # Sets X-axis range from 0 to 256
plt.title("RGB Histogram")  # Sets histogram title
plt.xlabel("Pixel Intensity")  # X-axis represents pixel intensity
plt.ylabel("Frequency")  # Y-axis represents pixel frequency
plt.grid()  # Displays grid lines

plt.legend(
    ['Red', 'Green', 'Blue'],
    loc="upper center",
    frameon=True
)  # Displays color labels

# 15. Final Display
plt.tight_layout()  # Automatically adjusts subplot spacing
plt.show()  # Displays all images and histogram
