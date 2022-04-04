import jsonlines
from PIL import Image
import math
import os
from ttf2img import ttf2img
import sys
import cv2
import numpy as np
# 本文件为本地生成汉字模块
# 需要系统传参
# 在此修改需要的文件存放目录

# Font_Document_Path 字体文件所存放路径 eg：
Font_Document_Path = 'C:/Users/simba/Desktop/template_fitting/fonts'

# Background_Document_Path 本文件存放路径 eg：
Background_Document_Path = 'C:/Users/simba/Desktop/template_fitting/backgrounds'

# Background_Json_Document_Path Json文件存放路径 eg:
Background_Json_Document_Path = 'C:/Users/simba/Desktop/template_fitting/backgrounds'

'''
模板融合模块说明：
back_fill.py：源文件，用于将字按模板要求融合到背景图像上
template.json：模板文件，以json格式记录每一个字的位置和大小
    json格式说明·：
        x：单字中心的横坐标，定义图像最左侧横坐标为0
        y：单字中心的纵坐标，定义图像最顶部纵坐标为0
        width：单字图像的宽度，单位为像素
        height：单字图像的高度，单位为像素
background.png：资源文件，背景图片
hanzi.png：资源文件，字体图像，应注意格式需为png且带有alpha通道，并将背景处理为透明图像
***************************************************************************************
本模块仅用于演示如何根据模板要求调整字体大小并填充到背景图像上，因此使用的都是同一个汉字
若需要在不同位置填充不同的汉字，请自行修改处理逻辑
***************************************************************************************
请务必注意模板应与背景的匹配
'''

# # 把图像背景变成透明（还可以优化）
# def make_transparent(image):
#     width, height = image.size
#     for x in range(width):
#         for y in range(height):
#             r, g, b, _ = image.getpixel((x, y))
#             if r == 255 and g == 255 and b == 255:
#                 image.putpixel((x, y), (255, 255, 255, 0))
#     return image

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
# 图片旋转 来自墙外某网站
# def rotate_bound(img, angle):
#     # grab the dimensions of the image and then determine the
#     # center
#     (h, w) = img.shape[:2]
#     (cX, cY) = (w // 2, h // 2)
#
#     # grab the rotation matrix (applying the negative of the
#     # angle to rotate clockwise), then grab the sine and cosine
#     # (i.e., the rotation components of the matrix)
#     M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
#     cos = np.abs(M[0, 0])
#     sin = np.abs(M[0, 1])
#
#     # compute the new bounding dimensions of the image
#     nW = int((h * sin) + (w * cos))
#     nH = int((h * cos) + (w * sin))
#
#     # adjust the rotation matrix to take into account translation
#     M[0, 2] += (nW / 2) - cX
#     M[1, 2] += (nH / 2) - cY
#
#     # perform the actual rotation and return the image
#     return cv2.warpAffine(img, M, (nW, nH))

# text 为传入参数，即想转换和汉字（字符串）
# font_path, background_img_path, background_json_path 为选择的字体，背景图，json文件类型
def main(text, font_path, background_img_path, background_json_path):
    # samples = get_sample_images('samples')

    samples = [ttf2img(font_path, char) for char in text]

    with open(background_json_path, "r+", encoding="utf8") as pos_json:
        # 读取json脚本中的内容
        positions = list(jsonlines.Reader(pos_json))

        # 打开背景图片
        background = Image.open(background_img_path)

        # char = make_transparent(Image.open("test.png"))
        # print("background shape:", background.size)
        index = 0
        s = len(text)
        _sum = 0
        # 读取json文件中的每一个{}里的数据
        for pos in positions:
            _sum += 1
            if _sum > s:
                break

            # resize : 通过读取的json参数调整输出单字的大小
            # pos[] 在json文件里取"XXX"中的关键字
            # image = (samples[index % (len(samples))].resize((pos["width"], pos["height"]))).transpose(Image.ROTATE_180)
            image = samples[index % (len(samples))].resize((pos["width"], pos["height"]))
            # 保存原来image图片大小
            box_cut = (000, 000, pos["width"], pos["height"])
            # 设置旋转角度
            rad = 10
            ex_height = int(math.sin(rad) * 10)  # 设置多与高度，防止剪切时部分丢失
            box_cut_rotate = (000, 000, pos["width"]+10, pos["height"])
            # 设置缩放倍数
            multi = 1.4 * abs(math.sin(rad))
            # if multi < 1:
            #     multi = 1.5
            # 缩小一定倍数，倍数可通过后期旋转角度自行调整，现用multy代替
            image = image.resize((int(pos["width"]//multi), int(pos["height"]//multi)))

            # 旋转
            # image = image.transpose(Image.ROTATE_270)

            # 设定顺逆时针
            shen_shi_zhen = 0
            ni_shi_zhen = 1
            rotate_mode = 0  # 此处调整顺逆时针
            if rotate_mode == 1:
                image = image.rotate(rad)
            else:
                image = image.rotate(rad+2*(180-rad))

            # 剪切
            image = image.crop(box_cut_rotate)

            # 还原
            image = image.resize((int(pos["width"]*multi), int(pos["height"]*multi)))
            image = image.crop(box_cut)

            # 上式中mul替ti 可能会使用函数来传入，用旋转角度来实现，现用multy代
            index += 1
            # print("width:%d, height:%d, x:%d, y:%d" % (pos["width"], pos["height"], pos["x"], pos['y']))
            # a用于保证输出的颜色
            _, _, _, a = image.split()
            print(a)
            # 在指定位置粘贴已经准备好的图像
            # 存放坐标的列表_box
            _box = (
                # // ：在一维坐标轴上向左取整
                # math.ceil : 在一维坐标轴上向右取整
                # 对x与y进行修改时，要保证 x的两个参数变化一直，y铜
                # 可通过对x，y的加减实现平移
                (pos["x"] - pos["width"] // 2),
                (pos["y"] - pos["height"] // 2),
                (pos["x"] + math.ceil(pos["width"] / 2)),
                (pos["y"] + math.ceil(pos["height"] / 2))
            )

            background.paste(image, _box, mask=a)

        # 弹出显示
        background.show()
        # 保存图片
        background.save("./result.png")
        # 关闭文件
        pos_json.close()


if __name__ == "__main__":
    print("传入的参数为")
    print(sys.argv)
    if len(sys.argv) != 5:
        print(f'参数个数错误,实际参数个数为{len(sys.argv)}，需要参数个数为5')
    else:
        main(sys.argv[1], f'{Font_Document_Path}/{sys.argv[2]}.ttf',
             f'{Background_Document_Path}/{sys.argv[3]}.jpg',
             f'{Background_Json_Document_Path}/{sys.argv[4]}.json')
