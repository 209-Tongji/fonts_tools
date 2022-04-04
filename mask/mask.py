

import jsonlines
from PIL import Image
import math
import os
import sys
import time

def main(mask,background_img_path,background_json_path):
        with open(background_json_path, "r+", encoding="utf8") as pos_json:
            positions = list(jsonlines.Reader(pos_json))
            background = Image.open(background_img_path)
            index = 0
            for pos in positions:
                image = Image.open(mask)
                index += 1
                _, _, _ = image.split()
                image = image.resize((pos["width"], pos["height"]))
                background.paste(image, (
                    pos["x"] - pos["width"] // 2,
                    pos["y"] - pos["height"] // 2
                ))# rgba,mask=a
            background.show()
            background.save("./result.png")

if __name__ == "__main__":
    mask='./mask.jpg'
    background='./backgrounds/0.jpg'
    layout='./backgrounds/0.json'
    main(mask,background,layout)
