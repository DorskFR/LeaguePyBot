from PIL import Image

import os
from pathlib import Path


def crop_square(file):
    img = Image.open(file)
    left = 18
    top = 18
    right = 18 + 84
    bottom = 18 + 84
    img_res = img.crop((left, top, right, bottom))
    img_res.save(file)


pwd = str(Path(__file__).parent.absolute())
path = pwd + "/champion"
files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]

for file in files:
    crop_square(os.path.join(path, file))
    print(f"Cropped {file}")
