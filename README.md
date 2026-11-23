# Min/Max Filter, Sobel Edge ও RGB Histogram — ডকুমেন্টেশন
<a href="https://mohammad-samiul-alam.github.io/Image-Processing-All-Operations/Documentation.html" target="_blank">
    Click here
</a>

> প্রতিটি অংশে প্রথমে বাংলা, তারপর **EN:** দিয়ে English দেওয়া আছে।

## সূচিপত্র / Contents

1. [পরিচিতি / Overview](#১-পরিচিতি--overview)
2. [লাইব্রেরি / Libraries](#২-লাইব্রেরি--libraries)
3. [ইমেজ লোড ও কনভার্ট / Load & Convert](#৩-ইমেজ-লোড-ও-কনভার্ট--load--convert)
4. [Min / Max ফিল্টার](#৪-min--max-ফিল্টার)
5. [Sobel Edge Detection](#৫-sobel-edge-detection)
6. [RGB Histogram](#৬-rgb-histogram)
7. [ডিসপ্লে লেআউট / Display Layout](#৭-ডিসপ্লে-লেআউট--display-layout)
8. [সম্পূর্ণ কোড / Full Code](#৮-সম্পূর্ণ-কোড--full-code)
9. [Viva প্রশ্ন-উত্তর / Viva Q&A](#৯-viva-প্রশ্ন-উত্তর--viva-qa)

---

## ১. পরিচিতি / Overview

এই প্রোগ্রাম Python (OpenCV, NumPy, Matplotlib) দিয়ে একটি রঙিন ছবি পড়ে, Minimum ও Maximum ফিল্টার প্রয়োগ করে, Sobel দিয়ে edge বের করে, RGB histogram আঁকে এবং সব ফলাফল একটি 3×3 figure-এ দেখায়।

**EN:** The program reads a colour image, applies minimum and maximum filters, detects edges with Sobel, plots the RGB histogram, and shows everything in one 3×3 figure.

**আউটপুট / Output:** Original, Minimum filter, Maximum filter, Sobel X, Sobel Y, Sobel, এবং নিচের সারিতে RGB Histogram।

## ২. লাইব্রেরি / Libraries

| লাইব্রেরি | কাজ | EN |
|---|---|---|
| `cv2` | ছবি পড়া, রঙ কনভার্ট, ফিল্টার, Sobel, histogram | Image I/O, colour conversion, filters, Sobel, histogram |
| `numpy` | Kernel matrix তৈরি | Create the kernel matrix |
| `matplotlib.pyplot` | ছবি ও গ্রাফ দেখানো | Display images and graphs |

```bash
pip install opencv-python numpy matplotlib
```

## ৩. ইমেজ লোড ও কনভার্ট / Load & Convert

`cv2.imread()` ফাইল না পেলে `None` দেয় (exception নয়), তাই আগে check করা হয়। OpenCV ছবি **BGR** ক্রমে রাখে, কিন্তু Matplotlib **RGB** চায়; তাই display-এর জন্য RGB কপি বানানো হয়। Sobel-এর জন্য Grayscale কপি লাগে, কারণ edge মানে উজ্জ্বলতার পরিবর্তন।

**EN:** `imread` returns `None` if the file is missing. OpenCV uses BGR while Matplotlib expects RGB, so the image is converted. Sobel works on a single grayscale intensity channel.

```python
img = cv2.imread("./color_image.png")
if img is None:
    print("Image is not found!")
    exit()
color_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray_img  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

## ৪. Min / Max ফিল্টার

৩×৩ kernel প্রতিটি pixel-এর আশপাশ নির্ধারণ করে।

- **Erosion (Minimum):** আশপাশের সর্বনিম্ন মান নেয় → ছবি গাঢ় হয়, ছোট উজ্জ্বল noise সরে।
- **Dilation (Maximum):** আশপাশের সর্বোচ্চ মান নেয় → ছবি উজ্জ্বল হয়, ছোট কালো দাগ সরে।

**EN:** Erosion takes the neighbourhood minimum (darkens), dilation takes the maximum (brightens).

```python
kernel  = np.ones((3,3), np.uint8)
min_img = cv2.erode(color_img, kernel)    # Minimum filter
max_img = cv2.dilate(color_img, kernel)   # Maximum filter
```

## ৫. Sobel Edge Detection

Sobel intensity-র gradient বের করে। **Sobel X** (dx=1) উল্লম্ব edge, **Sobel Y** (dy=1) আনুভূমিক edge ধরে। চূড়ান্ত edge শক্তি: **G = √(Gx² + Gy²)**। `CV_64F` ব্যবহার হয় যাতে ঋণাত্মক gradient `uint8`-এ কেটে না যায়।

**EN:** Sobel X finds vertical edges, Sobel Y finds horizontal edges; the magnitude combines both. `CV_64F` preserves negative gradients.

```python
sobel_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)
sobel   = cv2.magnitude(sobel_x, sobel_y)
```

## ৬. RGB Histogram

প্রতিটি channel (R, G, B)-এর জন্য ০–২৫৫ প্রতিটি intensity-র pixel সংখ্যা গুনে একটি রেখা আঁকা হয়। ডানে peak = উজ্জ্বল pixel বেশি; বামে peak = গাঢ় pixel বেশি।

**EN:** For each channel, count pixels per intensity (0–255) and plot a line.

```python
for i, color in enumerate(('r','g','b')):
    hist = cv2.calcHist([color_img], [i], None, [256], [0,256])
    plt.plot(hist, color=color)
```

## ৭. ডিসপ্লে লেআউট / Display Layout

`plt.subplot(3,3,n)` figure-কে ৩ সারি ও ৩ কলামে ভাগ করে। `(7,9)` শেষ সারির তিনটি ঘর জুড়ে histogram দেখায়।

| ঘর | বিষয় |
|---|---|
| 1 | Original image |
| 2 | Minimum filter |
| 3 | Maximum filter |
| 4 | Sobel X |
| 5 | Sobel Y |
| 6 | Sobel |
| 7–9 | RGB Histogram |

## ৮. সম্পূর্ণ কোড / Full Code

`color_image.png` ছবিটি স্ক্রিপ্টের পাশে রেখে রান করুন। (লাইন-বাই-লাইন কমেন্ট সংক্ষিপ্ত করা হয়েছে; লজিক একই।)

```python
import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread("./color_image.png")
if img is None:
    print("Image is not found!")
    exit()

color_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray_img  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Minimum and Maximum Filter
kernel  = np.ones((3,3), np.uint8)
min_img = cv2.erode(color_img, kernel)
max_img = cv2.dilate(color_img, kernel)

# Sobel Edge Detection
sobel_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)
sobel   = cv2.magnitude(sobel_x, sobel_y)

# Display Images
plt.figure(figsize=(12,6))

panels = [
    (1, color_img, None,   "Original image"),
    (2, min_img,   None,   "Minimum filter image"),
    (3, max_img,   None,   "Maximum filter image"),
    (4, sobel_x,   "gray", "Sobel X"),
    (5, sobel_y,   "gray", "Sobel Y"),
    (6, sobel,     "gray", "Sobel"),
]
for pos, image, cmap, title in panels:
    plt.subplot(3,3,pos)
    plt.imshow(image, cmap=cmap)
    plt.title(title)
    plt.axis("off")
    plt.gca().set_box_aspect(1)

# RGB Histogram
plt.subplot(3,3,(7,9))
for i, color in enumerate(('r','g','b')):
    hist = cv2.calcHist([color_img], [i], None, [256], [0,256])
    plt.plot(hist, color=color)

plt.xlim(0, 256)
plt.title("RGB color to histogram")
plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")
plt.grid()
plt.legend(['Red','Green','Blue'], loc='upper center', frameon=True)

plt.tight_layout()
plt.show()
```

## ৯. Viva প্রশ্ন-উত্তর / Viva Q&A

### ১. Minimum ও Maximum ফিল্টার কী? কোন ফাংশনে হয়?
প্রতিটি pixel-কে আশপাশের সবচেয়ে ছোট (Min) বা বড় (Max) মান দিয়ে বদলানো হয়। OpenCV-তে `cv2.erode` ও `cv2.dilate`।
**EN:** Replace each pixel with the neighbourhood min / max — `cv2.erode` / `cv2.dilate`.
```python
min_img = cv2.erode(color_img, kernel)
max_img = cv2.dilate(color_img, kernel)
```

### ২. Kernel হিসেবে `np.ones((3,3), np.uint8)` কেন?
এটি ৩×৩ বর্গাকার আশপাশ নির্ধারণ করে যেখানে ৯টি pixel-ই গণ্য হয়; `uint8` OpenCV-র প্রত্যাশিত type।
**EN:** Defines a 3×3 square neighbourhood; `uint8` is the type OpenCV expects.
```python
kernel = np.ones((3,3), np.uint8)
```

### ৩. BGR থেকে RGB কনভার্ট কেন?
`imread` BGR ক্রমে লোড করে, `imshow` RGB ধরে নেয়। না করলে লাল ↔ নীল উল্টে যাবে।
**EN:** `imread` gives BGR, `imshow` assumes RGB; otherwise red and blue swap.
```python
color_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

### ৪. Sobel operator কী? Sobel X ও Y কী দেখায়?
Sobel একটি first-derivative edge detector। X উল্লম্ব edge, Y আনুভূমিক edge ধরে।
**EN:** A first-derivative edge detector; X → vertical edges, Y → horizontal edges.
```python
sobel_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)
```

### ৫. Sobel-এ `cv2.CV_64F` কেন?
Gradient ঋণাত্মক হতে পারে; `uint8` ঋণাত্মক মান ০ করে ফেলে, ফলে অর্ধেক edge হারায়।
**EN:** `uint8` clips negative gradients to 0, losing edges; 64-bit float keeps them.

### ৬. চূড়ান্ত Sobel ছবি কীভাবে তৈরি হয়?
Magnitude দিয়ে: **G = √(Gx² + Gy²)**।
**EN:** By the gradient magnitude.
```python
sobel = cv2.magnitude(sobel_x, sobel_y)
```

### ৭. Sobel-এ Grayscale কেন?
Edge মানে উজ্জ্বলতার পরিবর্তন; একটি channel-ই যথেষ্ট এবং দ্রুত।
**EN:** Edges are brightness changes, so one channel is enough and faster.
```python
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

### ৮. Histogram কী এবং `cv2.calcHist`-এর প্যারামিটার?
প্রতিটি intensity-র pixel সংখ্যা। `calcHist(images, channels, mask, histSize, ranges)`।
**EN:** Pixel count per intensity value.
```python
hist = cv2.calcHist([color_img], [i], None, [256], [0, 256])
```

### ৯. `plt.subplot(3,3,(7,9))` মানে কী?
৩×৩ grid-এর ৭ থেকে ৯ নম্বর ঘর জুড়ে, অর্থাৎ পুরো নিচের সারি।
**EN:** Spans cells 7–9, the entire bottom row.
```python
plt.subplot(3,3,(7,9))
```

### ১০. ছবি না পাওয়া গেলে কী হয়?
`imread` `None` দেয়; প্রোগ্রাম check করে message দেখিয়ে বন্ধ হয়।
**EN:** `imread` returns `None`; the program prints a message and exits.
```python
if img is None:
    print("Image is not found!")
    exit()
```

### ১১. Erosion ও Dilation-এর পার্থক্য?
Erosion ছবি গাঢ় করে ও উজ্জ্বল noise সরায়; Dilation উজ্জ্বল করে ও কালো দাগ সরায়।
**EN:** Erosion darkens and removes bright noise; dilation brightens and removes dark specks.

### ১২. `tight_layout()` ও `set_box_aspect(1)` কী করে?
`tight_layout()` ফাঁকা ঠিক করে যাতে লেখা/plot overlap না করে; `set_box_aspect(1)` plot box বর্গাকার করে।
**EN:** Fixes spacing; makes each plot box square.
```python
plt.gca().set_box_aspect(1)
plt.tight_layout()
```
