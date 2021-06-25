import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def resizer(img_to_resize, percent=100):
    scale_percent = percent  # percent of original size
    width = int(img_to_resize.shape[1] * scale_percent / 100)
    height = int(img_to_resize.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv.resize(img_to_resize, dim, interpolation=cv.INTER_AREA)
    return resized


img = cv.imread("minimap3.png", 0)
# img = resizer(img, 100)

img2 = img.copy()


template = cv.imread("Renekton_small.png", 0)
# template = resizer(tmp, 26)

w, h = template.shape[::-1]
# All the 6 methods for comparison in a list
methods = [
    "cv.TM_CCOEFF",
    "cv.TM_CCOEFF_NORMED",
    "cv.TM_CCORR",
    "cv.TM_CCORR_NORMED",
    "cv.TM_SQDIFF",
    "cv.TM_SQDIFF_NORMED",
]
for meth in methods:
    img = img2.copy()
    method = eval(meth)
    # Apply template Matching
    res = cv.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img, top_left, bottom_right, 255, 2)
    plt.subplot(121), plt.imshow(res, cmap="gray")
    plt.title("Matching Result"), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(img, cmap="gray")
    plt.title("Detected Point"), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()
