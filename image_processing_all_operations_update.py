
import cv2  # Import OpenCV for image processing
import matplotlib.pyplot as plt  # Import Matplotlib for displaying images and graphs
import numpy as np  # Import NumPy for creating matrix and kernel

# Read Image
img = cv2.imread("./color_image.png")  # Read image from file

if img is None:  # Check whether image is loaded or not
    print("Image is not found!")  # Print error message if image is missing
    exit()  # Stop the program

# Color Conversion
color_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR image to RGB
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert BGR image to Grayscale

# Minimum and Maximum Filter
kernel = np.ones((3,3), np.uint8)  # Create a 3x3 kernel matrix
min_img = cv2.erode(color_img, kernel)  # Apply Erosion (Minimum filter)
max_img = cv2.dilate(color_img, kernel)  # Apply Dilation (Maximum filter)

# Sobel Edge Detection
sobel_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)  # Detect horizontal intensity changes
sobel_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)  # Detect vertical intensity changes
sobel = cv2.magnitude(sobel_x, sobel_y)  # Combine X and Y gradients to get edge magnitude

# Display Images
plt.figure(figsize=(12,6))  # Create figure with width 12 and height 6

# Store image position, image data, color map and title in a list
panels = [
    (1, color_img, None, "Original image"),  # Position 1: Original RGB image
    (2, min_img, None, "Minimum filter image"),  # Position 2: Minimum filter image
    (3, max_img, None, "Maximum filter image"),  # Position 3: Maximum filter image
    (4, sobel_x, "gray", "Sobel X"),  # Position 4: Sobel X grayscale image
    (5, sobel_y, "gray", "Sobel Y"),  # Position 5: Sobel Y grayscale image
    (6, sobel, "gray", "Sobel"),  # Position 6: Combined Sobel image
]

# Display all images using a loop
for pos, image, cmap, title in panels:  # Get position, image, color map and title
    plt.subplot(3,3,pos)  # Select subplot position in 3x3 grid
    plt.imshow(image, cmap=cmap)  # Display image with selected color map
    plt.title(title)  # Set image title
    plt.axis("off")  # Hide X-axis and Y-axis
    plt.gca().set_box_aspect(1)  # Make subplot box square

# RGB Histogram
plt.subplot(3,3,(7,9))  # Select positions 7, 8 and 9 together

# Calculate and display RGB histogram
for i, color in enumerate(('r','g','b')):  # Loop through Red, Green and Blue channels
    hist = cv2.calcHist([color_img], [i], None, [256], [0,256])  # Calculate histogram for each channel
    plt.plot(hist, color=color)  # Draw histogram using the corresponding color

# Histogram Settings
plt.xlim(0, 256)  # Set X-axis range from 0 to 256
plt.title("RGB color to histogram")  # Set histogram title
plt.xlabel("Pixel Intensity")  # Set X-axis label
plt.ylabel("Frequency")  # Set Y-axis label
plt.grid()  # Display grid lines
plt.legend(['Red','Green','Blue'], loc='upper center', frameon=True)  # Display color labels with a border

# Final Output
plt.tight_layout()  # Automatically adjust spacing between subplots
plt.show()  # Display all images and histogram
