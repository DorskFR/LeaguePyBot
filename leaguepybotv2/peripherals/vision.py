import gc

import cv2
import numpy as np
from mss import mss
from PIL import Image, ImageDraw

from ..common.models import Template
from ..logger import get_logger

logger = get_logger("LPBv2.Vision")


class Vision:
    def __init__(self):
        self.sct = mss()
        self.sct_original = None
        self.sct_img = None
        self.FPS = float()
        self.templates = dict()

    async def load_champion_template(self, championName: str):
        img = cv2.imread(f"leaguepybotv2/patterns/champion_2/{championName}.png", 0)
        self.templates[championName] = Template(name=championName, img=img)

    def shot_window(
        self, bounding_box={"top": 0, "left": 0, "width": 1920, "height": 1080}
    ):
        self.sct_original = np.asarray(self.sct.grab(bounding_box))
        self.sct_img = cv2.cvtColor(self.sct_original, cv2.COLOR_BGRA2GRAY)

    def clear_templates(self):
        del self.templates
        gc.collect()
        self.templates = dict()

    async def minimap_match(self):
        for template in self.templates.values():
            w, h = template.img.shape[::-1]
            match = cv2.matchTemplate(self.sct_img, template.img, cv2.TM_CCOEFF_NORMED)
            loc = np.where(match > 0.80)
            for pt in zip(*loc[::-1]):
                template.x = pt[0] + int(w / 2)
                template.y = pt[1] + int(h / 2)

    def mark_the_spot(self):
        for template in self.templates.values():
            if template.x and template.y:
                cv2.circle(
                    self.sct_original, (template.x, template.y), 15, (0, 255, 255), 2
                )
                cv2.putText(
                    self.sct_original,
                    template.name,
                    (template.x, template.y - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 255),
                    1,
                )

    def pcat(self, x, y, channel, threshold, mark_the_spot=False):
        # pcat = pixel_color_above_threshold
        COLORS = {"blue": 0, "green": 1, "red": 2}
        channel = COLORS[channel.lower()]
        pixel_color = tuple(int(x) for x in self.sct_img[y][x])
        if mark_the_spot:
            circle_color = (0, 0, 255)
            if pixel_color[channel] > threshold:
                circle_color = (0, 255, 0)
            cv2.circle(self.sct_img, (x, y), 10, circle_color, 3)
        return pixel_color[channel] > threshold
