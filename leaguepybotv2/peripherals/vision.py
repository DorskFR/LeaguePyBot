import gc

import cv2
import numpy as np
from mss import mss
from PIL import Image, ImageDraw

from ..common.models import Template
from ..logger import get_logger

logger = get_logger("LPBv2.Vision")


class Vision:
    def __init__(self, ratio=1):
        self.ratio = ratio
        self.sct = mss()
        self.sct_original = None
        self.sct_img = None
        self.width = 0
        self.height = 0
        self.FPS = float()
        self.templates = dict()

    async def load_champion_template(self, championName: str):
        img = self.resize(
            cv2.imread(
                f"leaguepybotv2/patterns/champion/{championName.lower()}.png", 0
            ),
            25,
        )
        self.templates[championName] = Template(name=championName, img=img)

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

    def shot_window(
        self, bounding_box={"top": 0, "left": 0, "width": 1920, "height": 1080}
    ):
        self.sct_original = np.asarray(self.sct.grab(bounding_box))
        self.sct_img = cv2.cvtColor(self.sct_original, cv2.COLOR_BGRA2GRAY)

    def clear_templates(self):
        del self.templates
        gc.collect()
        self.templates = dict()

    def save(self):
        try:
            filename = "screenshot.png"
            self.sct.save(mon=0, output=filename)
            logger.info(f"Saved {filename}")
        except:
            logger.error(f"Could not save {filename}")

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

    def template_match_old(self, template_img):
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

    # Matching template to the screenshot taken
    def template_match(self, template_img):
        img_gray = cv2.cvtColor(self.sct_img, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template_img, 0)
        name = template_img.split("/")[-1].split(".")[0]
        width = int(template.shape[1] / self.ratio)
        height = int(template.shape[0] / self.ratio)
        # template = cv2.resize(template, (width,height))
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.90
        if name == "minion":
            threshold = 0.99
        if "tower" in name:
            threshold = 0.85
        # if 'shop' in template_img: threshold = 0.95
        if "inventory" in template_img:
            threshold = 0.85
        if name == "start" or name == "ward" or name == "luden":
            threshold = 0.80
        loc = np.where(res > threshold)
        x = 0
        y = 0
        for pt in zip(*loc[::-1]):
            x += pt[0]
            y += pt[1]
            break
        if x != 0 and y != 0:
            x += width * self.ratio / 2
            y += height * self.ratio / 2
        del img_gray
        del template
        del res
        gc.collect()

        return int(x), int(y), name, loc, width, height

    def resize(self, img_to_resize, percent=100):
        scale_percent = percent  # percent of original size
        width = int(img_to_resize.shape[1] * scale_percent / 100)
        height = int(img_to_resize.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img_to_resize, dim, interpolation=cv2.INTER_AREA)
        return resized

    async def minimap_match(self):
        try:
            for template in self.templates.values():
                w, h = template.img.shape[::-1]
                match = cv2.matchTemplate(
                    self.sct_img, template.img, cv2.TM_CCOEFF_NORMED
                )
                # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
                # template.x = max_loc[0] + int(w / 2)
                # template.y = max_loc[1] + int(h / 2)

                x = None
                y = None

                loc = np.where(match > 0.80)
                for pt in zip(*loc[::-1]):
                    x = template.x = pt[0] + int(w / 2)
                    y = template.y = pt[1] + int(h / 2)

                if x and y:
                    cv2.circle(
                        self.sct_original,
                        (x, y),
                        15,
                        (0, 255, 255),
                        2,
                    )
                    cv2.putText(
                        self.sct_original,
                        template.name,
                        (x, y - 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 0, 255),
                        1,
                    )

        except Exception as e:
            logger.error(e)

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
