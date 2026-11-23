
import cv2  # OpenCV import: Image processing করার জন্য
import matplotlib.pyplot as plt  # Matplotlib import: Image ও graph display করার জন্য
import numpy as np  # NumPy import: Matrix ও kernel তৈরি করার জন্য

img = cv2.imread("./color_image.png")  # Image file read করা

if img is None:  # Image load হয়েছে কি না check করা
    print("Image is not found!")  # Image না পাওয়া গেলে message দেখানো
    exit()  # Program বন্ধ করা

color_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR image কে RGB তে convert করা
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # BGR image কে Grayscale এ convert করা

# Minimum and Maximum Filter
kernel = np.ones((3,3), np.uint8)  # 3x3 kernel matrix তৈরি করা

min_img = cv2.erode(color_img, kernel)  # Erosion: Minimum filter apply করা
max_img = cv2.dilate(color_img, kernel)  # Dilation: Maximum filter apply করা

# Sobel Edge Detection
sobel_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)  # X direction এ edge detect করা
sobel_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)  # Y direction এ edge detect করা
sobel = cv2.magnitude(sobel_x, sobel_y)  # X ও Y gradient combine করে edge magnitude বের করা

# Display Images
plt.figure(figsize=(12,6))  # Figure এর width 12 এবং height 6 নির্ধারণ করা

plt.subplot(3,3,1)  # 3 rows, 3 columns এর 1st position select করা
plt.imshow(color_img)  # Original RGB image display করা
plt.title("Original image")  # Image এর title দেওয়া
plt.axis("off")  # X-axis ও Y-axis hide করা
plt.gca().set_box_aspect(1)  # Plot box square করা

plt.subplot(3,3,2)  # 2nd position select করা
plt.imshow(min_img)  # Minimum filter image display করা
plt.title("Minimum filter image")  # Title দেওয়া
plt.axis("off")  # Axis hide করা
plt.gca().set_box_aspect(1)  # Plot box square করা

plt.subplot(3,3,3)  # 3rd position select করা
plt.imshow(max_img)  # Maximum filter image display করা
plt.title("Maximum filter image")  # Title দেওয়া
plt.axis("off")  # Axis hide করা
plt.gca().set_box_aspect(1)  # Plot box square করা

plt.subplot(3,3,4)  # 4th position select করা
plt.imshow(sobel_x, cmap='gray')  # Sobel X image grayscale এ display করা
plt.title("Sobel X")  # Title দেওয়া
plt.axis("off")  # Axis hide করা
plt.gca().set_box_aspect(1)  # Plot box square করা

plt.subplot(3,3,5)  # 5th position select করা
plt.imshow(sobel_y, cmap='gray')  # Sobel Y image grayscale এ display করা
plt.title("Sobel Y")  # Title দেওয়া
plt.axis("off")  # Axis hide করা
plt.gca().set_box_aspect(1)  # Plot box square করা

plt.subplot(3,3,6)  # 6th position select করা
plt.imshow(sobel, cmap='gray')  # Combined Sobel image display করা
plt.title("Sobel")  # Title দেওয়া
plt.axis("off")  # Axis hide করা
plt.gca().set_box_aspect(1)  # Plot box square করা

# RGB Histogram
plt.subplot(3,3,(7,9))  # নিচের 7, 8 ও 9 নম্বর position একসাথে নেওয়া

colors = ('r', 'g', 'b')  # Red, Green ও Blue channel নির্ধারণ করা

for i, color in enumerate(colors):  # প্রতিটি color channel এর index ও color নেওয়া
    hist = cv2.calcHist([color_img], [i], None, [256], [0, 256])  # প্রতিটি channel এর histogram calculate করা
    plt.plot(hist, color=color)  # Histogram line নির্দিষ্ট color এ আঁকা

plt.xlim(0, 256)  # X-axis এর range 0 থেকে 256 নির্ধারণ করা
plt.title("RGB color to histogram")  # Histogram এর title দেওয়া
plt.xlabel("Pixel Intensity")  # X-axis এর label দেওয়া
plt.ylabel("Frequency")  # Y-axis এর label দেওয়া
plt.grid()  # Graph এ grid line দেখানো
plt.legend(['Red', 'Green', 'Blue'], loc='upper center', frameon=True)  # Color এর নাম ও legend box দেখানো

# Final Output
plt.tight_layout()  # Subplot গুলোর মধ্যে automatic spacing দেওয়া
plt.show()  # সব image ও histogram display করা
