

from PIL import Image, ImageDraw, ImageFont
import os
def make_transparent(image):
    width, height = image.size
    for x in range(width):
        for y in range(height):
            r, g, b= image.getpixel((x, y))
#            r, g, b,_ = image.getpixel((x, y))# rgba
            if r == 255 and g == 255 and b == 255:
                image.putpixel((x, y), (255, 255, 255, 0))
    return image

def edge(image):
    width, height = image.size
    a=[]
    xmin=999
    xmax=0
    ymin=999
    ymax=0
    for x in range(width):
        for y in range(height):
            r, g, b= image.getpixel((x, y))
#            r, g, b,_ = image.getpixel((x, y))# rgba
            if (r == 255 and g == 255 and b == 255)and(x<xmin):
                xmin=x
            if (r == 255 and g == 255 and b == 255) and (x > xmax):
                xmax = x
            if (r == 255 and g == 255 and b == 255) and (y < ymin):
                ymin = y
            if (r == 255 and g == 255 and b == 255) and (y > ymax):
                ymax = y
    a.append(xmin)
    a.append(xmax)
    a.append(ymin)
    a.append(ymax)
    return a

def ttf2img1(font_path, char, font_size=256):
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = font.getsize(char)
    image = Image.new(mode='RGB', size=(text_width, text_height),color="white")#mode=rgba white->透明
#    image = Image.new(mode='RGB', size=(256,256), color="white")  # 背景色#mode=rgba white->透明
    draw_table = ImageDraw.Draw(im=image)
    draw_table.text(xy=(0, 0), text=char, fill="red", font=font)


    #image=make_transparent(image)
    return image

def ttf2img(font_path, char, font_size=256):
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = font.getsize(char)
    image = Image.new(mode='RGB', size=(text_width, text_height),color="red")#背景色#mode=rgba white->透明
#    image = Image.new(mode='RGB', size=(400, 400), color="red")  # 背景色#mode=rgba white->透明
    draw_table = ImageDraw.Draw(im=image)
    draw_table.text(xy=(0, 0), text=char, fill="white", font=font)#汉字色
    a=edge(image)
    image=image.crop((a[0], a[2], a[1], a[3]))
#    image.show()
    #image = make_transparent(image)
    return image
# if __name__ == "__main__":
#     print('开始运行:')
#     for name in os.listdir('./font'):
#         try:
#             name = name.split('.')[0]
#             image = ttf2img(name,"同")
#             image.show()  # 直接显示图片
#             # image.save('./font_img/' + font_path + '-'+ char + '.png', 'PNG')  # 保存在当前路径下，格式为PNG
#             # image.close()
#         except Exception as e:
#             print(name, ' ERR: ', e)
#             continue
