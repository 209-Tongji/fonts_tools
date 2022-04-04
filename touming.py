# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
from PIL import Image
def make_transparent(image):
    width, height=image.size
    """grey = im.convert('L')  # 转成灰度
    px = grey.load()  # 获取灰度数组"""
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            alpha_rgb = 1-((1-r*1.0/255)*(1-g*1.0/255)*(1-b*1.0/255))
            if alpha_rgb != 0:
                result.putpixel((x, y), (round(r / alpha_rgb), round(g / alpha_rgb), round(b / alpha_rgb), round(alpha_rgb * 255)))
            else:
                result.putpixel((x, y), (r, g, b, round(alpha_rgb * 255)))
    result.save("result2.png", "PNG")
    result.show()
    return image


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    im = Image.open(r'1.png', 'r')
    im = im.convert("RGB")
    make_transparent(im)


# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助