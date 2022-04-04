

from PIL import Image, ImageDraw, ImageFont
import os


def ttf2img(font_path, char, font_size=256):
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = font.getsize(char)
    image = Image.new(mode='RGBA', size=(text_width, text_height))
    draw_table = ImageDraw.Draw(im=image)
    draw_table.text(xy=(0, 0), text=char, fill='#000000', font=font)
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
