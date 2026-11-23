# OpenCV Image Processing — ডকুমেন্টেশন

[পরিচিতি](#intro) [লাইব্রেরি](#libs) [ইমেজ লোড ও কনভার্ট](#load) [Min / Max ফিল্টার](#minmax) [Sobel Edge Detection](#sobel) [RGB Histogram](#hist) [ডিসপ্লে লেআউট](#show) [ফাংশন তালিকা](#func) [সম্পূর্ণ কোড](#code) [Viva প্রশ্ন-উত্তর](#viva)

## Min/Max ফিল্টার, Sobel Edge ও RGB Histogram

এই প্রোগ্রামটি Python (OpenCV, NumPy, Matplotlib) দিয়ে একটি রঙিন ছবি পড়ে, তাতে Minimum ও Maximum ফিল্টার প্রয়োগ করে, Sobel দিয়ে edge বের করে, RGB histogram আঁকে এবং সব ফলাফল একটি 3×3 figure-এ দেখায়।

### আউটপুটে যা যা দেখা যায়

- Original image, Minimum filter image, Maximum filter image
- Sobel X, Sobel Y এবং সম্মিলিত Sobel
- RGB histogram (নিচের সারির ৩টি ঘর একসাথে)

## ব্যবহৃত লাইব্রেরি

| লাইব্রেরি | কাজ |
| --- | --- |
| `cv2` | ছবি পড়া, রঙ কনভার্ট, ফিল্টার, Sobel, histogram গণনা |
| `numpy` | Kernel matrix তৈরি করা |
| `matplotlib.pyplot` | ছবি ও histogram গ্রাফ দেখানো |

ইনস্টল: `pip install opencv-python numpy matplotlib`

## ইমেজ লোড ও কালার কনভার্সন

cv2.imread() ফাইল না পেলে `None` দেয়। তাই প্রোগ্রাম আগে সেটি check করে, ছবি না পেলে message দেখিয়ে বন্ধ হয়।

OpenCV ছবি **BGR** ক্রমে রাখে, কিন্তু Matplotlib **RGB** আশা করে। তাই display-এর জন্য RGB-তে কনভার্ট করা হয়। Sobel-এর জন্য Grayscale কপি বানানো হয়, কারণ edge detection একটি intensity channel-এর উপর কাজ করে।

python

```
img = cv2.imread("./color_image.png")
if img is None:
    print("Image is not found!")
    exit()
color_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray_img  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

## Minimum ও Maximum ফিল্টার

৩×৩ kernel (সব মান ১) প্রতিটি pixel-এর আশপাশ নির্ধারণ করে। **Erosion** ওই আশপাশের সর্বনিম্ন মান নেয় (কালো অংশ বড় হয়, উজ্জ্বল ছোট অংশ মুছে যায়)। **Dilation** সর্বোচ্চ মান নেয় (উজ্জ্বল অংশ বড় হয়, কালো ছোট অংশ মুছে যায়)।

python

```
kernel  = np.ones((3,3), np.uint8)
min_img = cv2.erode(color_img, kernel)    # Minimum filter
max_img = cv2.dilate(color_img, kernel)   # Maximum filter
```

## Sobel Edge Detection

Sobel intensity-এর gradient বের করে। **Sobel X** (dx=1) উল্লম্ব edge, **Sobel Y** (dy=1) আনুভূমিক edge ফুটিয়ে তোলে। চূড়ান্ত edge শক্তি হলো magnitude: **√(Gx² + Gy²)**।

python

```
sobel_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)
sobel   = cv2.magnitude(sobel_x, sobel_y)
```

CV_64F ব্যবহার করা হয় যাতে ঋণাত্মক gradient মান uint8-এর মতো কেটে না যায়।

## RGB Histogram

প্রতিটি channel (R, G, B)-এর জন্য ০ থেকে ২৫৫ পর্যন্ত প্রতিটি intensity-র pixel সংখ্যা গোনা হয় এবং প্রতি channel-এর জন্য একটি রেখা আঁকা হয়। ডানে peak মানে অনেক উজ্জ্বল pixel, বামে peak মানে অনেক গাঢ় pixel।

python

```
for i, color in enumerate(('r','g','b')):
    hist = cv2.calcHist([color_img], [i], None, [256], [0,256])
    plt.plot(hist, color=color)
```

## ডিসপ্লে লেআউট

plt.subplot(3,3,n) figure-কে ৩ সারি ও ৩ কলামে ভাগ করে। ১–৬ নম্বর ঘরে ছবি বসে; `(7,9)` শেষ তিনটি ঘর জুড়ে histogram দেখায়। set_box_aspect(1) প্রতিটি ছবির box বর্গাকার রাখে এবং tight_layout() ফাঁকা জায়গা ঠিক করে।

| ঘর | বিষয় |
| --- | --- |
| 1 | Original image |
| 2 | Minimum filter |
| 3 | Maximum filter |
| 4 | Sobel X |
| 5 | Sobel Y |
| 6 | Sobel |
| 7–9 | RGB Histogram |

## ফাংশন তালিকা

| Function | কাজ |
| --- | --- |
| `cv2.imread` | ছবি ফাইল পড়া |
| `cv2.cvtColor` | Color space পরিবর্তন |
| `cv2.erode` | Minimum ফিল্টার |
| `cv2.dilate` | Maximum ফিল্টার |
| `cv2.Sobel` | X বা Y দিকে gradient |
| `cv2.magnitude` | Gx ও Gy মিলিয়ে magnitude |
| `cv2.calcHist` | Histogram গণনা |
| `plt.subplot / imshow` | Grid-এ ঘর নির্বাচন / ছবি দেখানো |

## সম্পূর্ণ কোড

ছবিটি `color_image.png` নামে স্ক্রিপ্টের পাশে রেখে রান করুন। (লাইন-বাই-লাইন কমেন্ট সংক্ষিপ্ত করা হয়েছে; লজিক হুবহু একই।)

color_filter_sobel.py

```

```

## Viva প্রশ্ন-উত্তর

১. Minimum ও Maximum ফিল্টার কী? OpenCV-তে কোন ফাংশন দিয়ে করা হয়?

Minimum ফিল্টার প্রতিটি pixel-কে তার আশপাশের সবচেয়ে ছোট মান দিয়ে, Maximum ফিল্টার সবচেয়ে বড় মান দিয়ে প্রতিস্থাপন করে। OpenCV-তে এগুলো `cv2.erode` ও `cv2.dilate`।

python

```
min_img = cv2.erode(color_img, kernel)
max_img = cv2.dilate(color_img, kernel)
```

২. Kernel হিসেবে np.ones((3,3), np.uint8) কেন?

এটি ৩×৩ বর্গাকার আশপাশ নির্ধারণ করে যেখানে ৯টি pixel-ই গণ্য হয়। uint8 হলো structuring element-এর জন্য OpenCV-র প্রত্যাশিত data type।

python

```
kernel = np.ones((3,3), np.uint8)
```

৩. BGR থেকে RGB কনভার্ট কেন করা হয়?

cv2.imread চ্যানেল Blue-Green-Red ক্রমে লোড করে, আর plt.imshow ধরে নেয় Red-Green-Blue। কনভার্ট না করলে রঙ উল্টো (লাল ↔ নীল) দেখাবে।

python

```
color_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

৪. Sobel operator কী? Sobel X ও Y কী দেখায়?

Sobel একটি first-derivative edge detector, যা ৩×৩ kernel দিয়ে intensity-র পরিবর্তন মাপে। Sobel X উল্লম্ব edge (x-দিকে পরিবর্তন), Sobel Y আনুভূমিক edge (y-দিকে পরিবর্তন) ধরে।

python

```
sobel_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)
```

৫. Sobel-এ cv2.CV_64F কেন ব্যবহার হয়?

Gradient ঋণাত্মক হতে পারে (গাঢ় থেকে উজ্জ্বল বনাম উজ্জ্বল থেকে গাঢ়)। uint8 ঋণাত্মক মান রাখতে পারে না, ০ করে ফেলে, ফলে অর্ধেক edge হারায়। 64-bit float আসল মান ধরে রাখে।

৬. চূড়ান্ত Sobel ছবি কীভাবে তৈরি হয়?

Gradient magnitude দিয়ে: **G = √(Gx² + Gy²)**, যা দুই দিকের edge একসাথে করে।

python

```
sobel = cv2.magnitude(sobel_x, sobel_y)
```

৭. Sobel-এ Grayscale ছবি কেন?

Edge মানে উজ্জ্বলতার পরিবর্তন, তাই একটি intensity channel-ই যথেষ্ট এবং তিনটি রঙিন channel আলাদা প্রসেস করার চেয়ে দ্রুত।

python

```
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

৮. Histogram কী এবং cv2.calcHist কী কী প্যারামিটার নেয়?

Histogram দেখায় প্রতিটি intensity-র কতগুলো pixel আছে। calcHist(images, channels, mask, histSize, ranges): ছবির তালিকা, channel index, ঐচ্ছিক mask, bin সংখ্যা (256) এবং মানের পরিসর \[0, 256\]।

python

```
hist = cv2.calcHist([color_img], [i], None, [256], [0, 256])
```

৯. plt.subplot(3,3,(7,9)) এর অর্থ কী?

৩×৩ grid-এর ৭ থেকে ৯ নম্বর ঘর জুড়ে, অর্থাৎ পুরো নিচের সারি, যাতে histogram চওড়া জায়গা পায়।

python

```
plt.subplot(3,3,(7,9))
```

১০. ছবি না পাওয়া গেলে কী হয়?

cv2.imread `None` ফেরত দেয় (exception দেয় না)। প্রোগ্রাম None check করে message দেখিয়ে বন্ধ হয়, ফলে পরবর্তী ধাপে error হয় না।

python

```
if img is None:
    print("Image is not found!")
    exit()
```

১১. Erosion ও Dilation-এর ফলাফলে পার্থক্য কী?

Erosion (minimum) ছবি গাঢ় করে ও ছোট উজ্জ্বল noise সরায়। Dilation (maximum) ছবি উজ্জ্বল করে ও ছোট কালো দাগ সরায়। দুটোই সূক্ষ্ম বিস্তারিত অংশ ঝাপসা করে।

১২. tight_layout() ও set_box_aspect(1) কী করে?

tight_layout() ফাঁকা ঠিক করে যাতে title ও plot একটির উপর আরেকটি না পড়ে। set_box_aspect(1) প্রতিটি plot box বর্গাকার করে।

python

```
plt.gca().set_box_aspect(1)
plt.tight_layout()
```
