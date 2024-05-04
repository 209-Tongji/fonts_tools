import fontforge
import os
# 指定输入的TTF字体文件路径
import glob

def get_ttf_filenames_without_extension(folder_path):
    ttf_files = glob.glob(os.path.join(folder_path, '*.ttf'))
    ttf_filenames = [os.path.splitext(os.path.basename(file))[0] for file in ttf_files]
    return ttf_filenames

folder_path = 'D:/fonts1/'
ttf_filenames = get_ttf_filenames_without_extension(folder_path)

a=0
for i in ttf_filenames:
    ttf_name=i
    if not os.path.exists('D:/ttfsvg1/'+ttf_name):
        os.makedirs('D:/ttfsvg1/'+ttf_name)
    else:
        a=a+1
        continue
    print(ttf_name)
    print(a)
    input_font_file = 'D:/fonts1/'+ttf_name+'.ttf'
    # 创建FontForge字体对象
    try:
        font = fontforge.open(input_font_file)
    except:
        aa=1

    # 遍历每个字符并保存为SVG文件
    for glyph in font.glyphs():
        # 获取字符的Unicode编码
        unicode_codepoint = str(glyph.unicode)


        svg_filename = 'D:/ttfsvg1/'+ttf_name+"/"+str(unicode_codepoint)+'.svg'

        # 保存字符为SVG文件
        glyph.export(svg_filename, size=(1000, 1000))  # 调整大小以适应您的需求

    # 关闭字体文件
    font.close()
