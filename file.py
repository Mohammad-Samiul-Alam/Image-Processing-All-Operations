
import cv2  # Image processing
import matplotlib.pyplot as plt  # Image display and plotting
import numpy as np  # Array and matrix operations

# Read Image
img = cv2.imread("./color_image.png")

# Check whether the image is loaded successfully
if img is None:
    print("Image not found!")
    exit()

# Convert BGR image to RGB and Grayscale
color_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Create a 3x3 kernel (matrix) for filtering
kernel = np.ones((3, 3), np.uint8)

# Minimum Filter (Erosion)
min_img = cv2.erode(color_img, kernel)

# Maximum Filter (Dilation)
max_img = cv2.dilate(color_img, kernel)

# Sobel Edge Detection in X direction
sobel_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)

# Sobel Edge Detection in Y direction
sobel_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)

# Combine Sobel X and Y using Magnitude
sobel = cv2.magnitude(sobel_x, sobel_y)

# Convert Sobel results into 8-bit images for display
sobel_x = cv2.convertScaleAbs(sobel_x)
sobel_y = cv2.convertScaleAbs(sobel_y)
sobel = cv2.convertScaleAbs(sobel)

# Store images, titles and color maps in a list
panels = [
    (1, color_img, "Original Image", None),
    (2, min_img, "Minimum Filter Image", None),
    (3, max_img, "Maximum Filter Image", None),
    (4, sobel_x, "Sobel X", "gray"),
    (5, sobel_y, "Sobel Y", "gray"),
    (6, sobel, "Sobel", "gray")
]

# Create a figure with 12x6 size
plt.figure(figsize=(12, 6))

# Display all six images using a loop
for n, image, title, cmap in panels:

    # Create subplot in a 3x3 grid
    plt.subplot(3, 3, n)

    # Display image
    plt.imshow(image, cmap=cmap)

    # Set image title
    plt.title(title)

    # Hide X-axis and Y-axis
    plt.axis("off")

    # Make subplot square
    plt.gca().set_box_aspect(1)


# RGB Histogram
# Use the last row (7, 8, 9) for histogram
plt.subplot(3, 3, (7, 9))

# Define RGB colors
colors = ('r', 'g', 'b')

# Calculate and plot RGB histograms
for i, color in enumerate(colors):

    # Calculate histogram for each RGB channel
    hist = cv2.calcHist([color_img], [i], None, [256], [0, 256])

    # Plot histogram using corresponding color
    plt.plot(hist, color=color)

# Set histogram X-axis range
plt.xlim(0, 256)

# Set histogram title and axis labels
plt.title("RGB Histogram")
plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")

# Display grid
plt.grid()

# Display legend
plt.legend(['Red', 'Green', 'Blue'],
           loc="upper center",
           frameon=True)

# Adjust spacing between subplots
plt.tight_layout()

# Display all images and histogram
plt.show()
