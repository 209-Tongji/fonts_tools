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
from flask import Flask,make_response
import jsonlines
from PIL import Image
import math
import os
from ttf2img import ttf2img
import sys
from io import BytesIO
from flask import request, jsonify
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



def main(text, font_path, background_img_path, background_json_path):
    # samples = get_sample_images('samples')

    samples = [ttf2img(font_path, char) for char in text]

    with open(background_json_path, "r+", encoding="utf8") as pos_json:
        positions = list(jsonlines.Reader(pos_json))
        background = Image.open(background_img_path)
        # char = make_transparent(Image.open("test.png"))
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
            _, _, _, a = image.split()
            print(a)
            background.paste(image, (
                pos["x"] - pos["width"] // 2,
                pos["y"] - pos["height"] // 2,
                pos["x"] + math.ceil(pos["width"] / 2),
                pos["y"] + math.ceil(pos["height"] / 2)
            ), mask=a)
        background.show()
        background.save("./result.png")
app = Flask(__name__)
@app.route('/',methods=['POST','GET','PUT'])
def output_data():
        a = request.args.get('str')
        y = request.args.get('fon')
        z = request.args.get('back')
        t = request.args.get('templ')
        b='/sim/ziji/template_fitting/fonts/'+y+'.TTF'
        c='/sim/ziji/template_fitting/backgrounds/'+z+'.jpg'
        d='/sim/ziji/template_fitting/backgrounds/'+t+'.json'      
        main(a,b,c,d)
        img = Image.open('/sim/ziji/template_fitting/result.png')
        f = BytesIO()
        img.save(f, "png")
        resp = make_response(f.getvalue())
        resp.headers["Content-Type"] = "image/jpeg"
        return resp
if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0',port=5080)
    #app.run( 0.0.0.0:5000)

   