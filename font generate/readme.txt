python char_gen.py

可选参数：
chinese_dir = '请在此输入字体名字(不带ttf)，并把ttf文件放入fonts文件夹' #e.g. chinese_dir = 'FZChuSLKSJW'
crop_flag=False #如果是True，则裁剪模式打开（有些字体生成的字符不是正方形，若自动生成的是正方形可选择False）
component_flag=True #如果是True，则生成lffont中拆分部件的集合，反之，生成代码第31行unicode列表里的所有字符
font_size=256#生成字符图片的长，宽
背景色和汉字颜色 #第46行