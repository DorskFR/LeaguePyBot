from mss import mss
import cv2
import numpy as np
import gc


class Vision:
    def __init__(self, ratio=1):
        self.ratio = ratio
        self.sct = mss()
        self.sct_img = None
        self.width = 0
        self.height = 0

    # Screenshots
    def capture_window(
        self, bounding_box={"top": 0, "left": 0, "width": 1920, "height": 1080}
    ):
        sct_img = self.sct.grab(bounding_box)
        self.width = int(bounding_box["width"] / self.ratio)
        self.height = int(bounding_box["height"] / self.ratio)
        sct_img_resized = cv2.resize(np.array(sct_img), (self.width, self.height))
        del sct_img
        gc.collect()
        self.sct_img = sct_img_resized
        return

    def template_match_square(self, template_img):
        img_gray = cv2.cvtColor(self.sct_img, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template_img, 0)
        # w, h = template.shape[::-1]
        width = int(template.shape[1] / self.ratio)
        height = int(template.shape[0] / self.ratio)
        template = cv2.resize(template, (width, height))

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.80
        loc = np.where(res > threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(
                self.sct_img, pt, (pt[0] + width, pt[1] + height), (0, 255, 255), 1
            )
            # cv2.putText(img_bgr, 'minion', (pt[0], pt[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,255), 2)

        return

    def template_match(self, template_img):
        img_gray = cv2.cvtColor(self.sct_img, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template_img, 0)
        # w, h = template.shape[::-1]
        width = int(template.shape[1] / self.ratio)
        height = int(template.shape[0] / self.ratio)
        template = cv2.resize(template, (width, height))

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.80
        loc = np.where(res > threshold)
        if loc:
            return [pt for pt in zip(*loc[::-1])]

        return

    def draw_grid(self, text=False):
        # prepare variables, c is the side of the cubes
        x = 0
        y = 0
        c = int(10 / self.ratio)

        # draw the squares
        while y < self.height:
            while x <= self.width:
                cv2.rectangle(self.sct_img, (x, y), (x + c, y + c), (0, 255, 255), 1)
                if text:
                    cv2.putText(
                        self.sct_img,
                        f"{x}",
                        (x + 10, y + 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.3,
                        (255, 255, 0),
                        1,
                    )
                    cv2.putText(
                        self.sct_img,
                        f"{y}",
                        (x + 10, y + 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.3,
                        (255, 255, 0),
                        1,
                    )
                x += c
            y += c
            x = 0

        return

    def pcat(self, x, y, channel, threshold, mark_the_spot=False):
        # pcat = pixel_color_above_threshold
        x = int(x / self.ratio)
        y = int(y / self.ratio)
        COLORS = {"blue": 0, "green": 1, "red": 2}
        channel = COLORS[channel.lower()]
        pixel_color = tuple(int(x) for x in self.sct_img[y][x])
        if mark_the_spot:
            circle_color = (0, 0, 255)
            if pixel_color[channel] > threshold:
                circle_color = (0, 255, 0)
            cv2.circle(self.sct_img, (x, y), 10, circle_color, 3)
        return pixel_color[channel] > threshold
