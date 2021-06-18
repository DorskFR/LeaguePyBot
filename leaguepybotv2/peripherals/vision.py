import gc
from pathlib import Path

import cv2
import numpy as np
from mss import mss

from ..common.models import Template, Match
from ..logger import get_logger

logger = get_logger("LPBv2.Vision")


class Vision:
    def __init__(self):
        self.sct = mss()
        self.sct_original = None
        self.sct_img = None
        self.templates = list()
        self.matches = list()

    async def load_game_templates(self):
        names = ["minion", "champion", "building"]
        for name in names:
            await self.load_template(folder="units/", name=name)

    async def load_champion_template(self, championName: str):
        await self.load_template(folder="champion/", name=championName)

    async def load_template(self, folder: str, name: str):
        path = str(Path(__file__).parent.absolute()) + "/patterns/"
        img = cv2.imread(f"{path}{folder}{name}.png", 0)
        self.templates[name] = Template(name=name, img=img)

    async def shot_window(
        self, bounding_box={"top": 0, "left": 0, "width": 1920, "height": 1080}
    ):
        self.sct_original = np.asarray(self.sct.grab(bounding_box))
        self.sct_img = cv2.cvtColor(self.sct_original, cv2.COLOR_BGRA2GRAY)

    async def get_match(self, name):
        for match in self.matches:
            if match.name == name:
                return match

    async def clear_templates(self):
        del self.templates
        gc.collect()
        self.templates = list()

    async def clear_matches(self):
        del self.matches
        gc.collect()
        self.matches = list()

    async def minimap_match(self):
        self.clear_matches()
        for template in self.templates:
            w, h = template.img.shape[::-1]
            match = cv2.matchTemplate(self.sct_img, template.img, cv2.TM_CCOEFF_NORMED)
            loc = np.where(match > 0.80)
            for pt in zip(*loc[::-1]):
                self.matches.append(
                    Match(
                        name=template.name,
                        x=pt[0] + int(w / 2),
                        y=pt[1] + int(h / 2),
                    )
                )

    async def mark_the_spot(self):
        for template in self.templates:
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

    async def pcat(self, x, y, channel, threshold, mark_the_spot=False):
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
