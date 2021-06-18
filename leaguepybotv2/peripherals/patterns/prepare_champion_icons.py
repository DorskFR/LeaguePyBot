from PIL import Image

import os
import cv2
from pathlib import Path


def get_files(path):
    files = [
        file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))
    ]
    files = [file for file in files if file.endswith(".png")]
    return files


def crop_square(path, file):
    img = Image.open(os.path.join(path, file))
    left = 18
    top = 18
    right = 18 + 84
    bottom = 18 + 84
    img_res = img.crop((left, top, right, bottom))
    img_res.save(os.path.join(path, file))


def rename_file(path, file):
    os.rename(os.path.join(path, file.lower()), os.path.join(path, file))


def resize_img(path, file):
    img = cv2.imread(os.path.join(path, file))
    img_res = cv2.resize(img, (22, 22), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(os.path.join(path, file), img_res)


def main():
    pwd = str(Path(__file__).parent.absolute())
    path = pwd + "/champion"
    files = get_files(path)
    print(f"Found {len(files)}")

    for file in files:
        crop_square(path, file)
        resize_img(path, file)
        # rename_file(path, file)
        print(f"Processed {file}")


if __name__ == "__main__":
    main()
