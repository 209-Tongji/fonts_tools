

import jsonlines
from PIL import Image
import math
import os
from ttf2img import ttf2img,ttf2img1,edge
import sys
import time
# 把图像背景变成透明（还可以优化）
def make_transparent(image):
    width, height = image.size
    for x in range(width):
        for y in range(height):
            r, g, b,_= image.getpixel((x, y))
            if r == 255 and g == 255 and b == 255:
                image.putpixel((x, y), (255, 255, 255, 0))
    return image

# # 按照crop ratio给定的比例进行图像切分
# def cropped_image(
#     image,
#     left_crop_ratio, right_crop_ratio,
#     top_crop_ratio, bottom_crop_ratio):
#     width, height = image.size
#     return image.crop((
#         width * left_crop_ratio, height * top_crop_ratio,
#         width * right_crop_ratio, height * bottom_crop_ratio
#     ))

# # 获取 sample_dir 目录里的所有图像，把他们crop以及transparent后返回list
# def get_sample_images(sample_dir):
#     images = []
#     for file in os.listdir(sample_dir):
#         if not file.endswith(".png") and not file.endswith(".jpg"):
#             continue
#         image = Image.open(os.path.join(sample_dir, file))
#         image = image.convert('RGBA')
#         image = cropped_image(image, 0, 0.5, 0, 1)
#         image = make_transparent(image)
#         images.append(image)
#     return images

def main(text,text1,font_path, font1_path,background_img_path, background_json_path,background_json_path_1):
    # samples = get_sample_images('samples')
    start = time.time()
    for i in range(1,2):
        samples = [ttf2img(font_path, char) for char in text]
        samples1=[ttf2img1(font1_path, char) for char in text1]
        with open(background_json_path, "r+", encoding="utf8") as pos_json:
            positions = list(jsonlines.Reader(pos_json))
            background = Image.open(background_img_path)
            # print("background shape:", background.size)
            index = 0
            s=len(text)
            sum=0
            for pos in positions:
                sum=sum+1
                if (sum>s):
                    break
                image = samples[index % len(samples)].resize((pos["width"], pos["height"]))
                index += 1
                # print("width:%d, height:%d, x:%d, y:%d" % (pos["width"], pos["height"], pos["x"], pos['y']))
                _, _, _ = image.split()
#                _, _, _,a = image.split()  # rgba
                background.paste(image, (
                    pos["x"] - pos["width"] // 2,
                    pos["y"] - pos["height"] // 2,
                    pos["x"] + math.ceil(pos["width"] / 2),
                    pos["y"] + math.ceil(pos["height"] / 2)
                ))# rgba,mask=a
            with open(background_json_path_1, "r+", encoding="utf8") as pos_json_1:
                positions_1 = list(jsonlines.Reader(pos_json_1))
                index = 0
                s = len(text1)
                sum = 0
                for pos in positions_1:
                    sum = sum + 1
                    if (sum > s):
                        break
                    image = samples1[index % len(samples)].resize((pos["width"], pos["height"]))
                    index += 1
                    _, _, _ = image.split()
#                    _, _, _, a = image.split()
                    background.paste(image, (
                        pos["x"] - pos["width"] // 2,
                        pos["y"] - pos["height"] // 2,
                        pos["x"] + math.ceil(pos["width"] / 2),
                        pos["y"] + math.ceil(pos["height"] / 2)
                    ))
            #background = background.convert('RGBA')
            #background=make_transparent(background)
            background.show()
            background.save("./result.png")
    end = time.time()
    #print((end - start))


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 6:
        print('Incorrect number of arguments')
    else:
        main(sys.argv[1],sys.argv[2], f'./fonts/{sys.argv[3]}',#系统参数1是周围几个字的排布，2是中间两个字，3是周围字使用的字体，4是中间字使用的字体，5是模板选择
             f'./fonts/{sys.argv[4]}',
             f'./backgrounds/{sys.argv[5]}.jpg',
             f'./backgrounds/{sys.argv[5]}.json',f'./backgrounds/{sys.argv[5]}-1.json')
