 #encoding: utf-8
import os
import pygame
import cv2
from PIL import Image as ImagePIL
from PIL import Image
import fontTools
from fontTools.ttLib import TTFont
import json


import json
chinese_dir = '请在此输入字体名字(不带ttf)，并把ttf文件放入fonts文件夹'#例chinese_dir = 'FZChuSLKSJW'
chinese_dir = 'FZChuSLKSJW'
crop_flag=True #如果是True，则需要裁剪为256*256
component_flag=True #如果是True，则生成lffont中拆分部件的集合
font_size=256#生成字符图片的长，宽
ttf_dir='./fonts/'+chinese_dir+".ttf"
if not os.path.exists(chinese_dir):
    os.mkdir(chinese_dir)

chn_dec = json.load(open("./chn_decompose.json"))
uid_c = {}
pll=[]
if component_flag:
    for c, decs in chn_dec.items():
        if len(decs) > 1:
            continue
        else:
            pll.append(chr(int(c, 16)))
else:
    for i in range(0x4E00, 0x9FFF):#生成unicode的范围
        pll.append(chr(int(i)))
pygame.init()
list= {}
num=0
font1 = TTFont(ttf_dir)
background = Image.open('./background.jpg')
background=background.resize((int(1.1*font_size),int(1.1*font_size)))
uniMap = font1['cmap'].tables[0].ttFont.getBestCmap()
font = pygame.font.Font(ttf_dir, font_size)
for word in pll:
    if not(ord(word) in uniMap.keys()):continue
    list.update({ord(word):word})
    num=num+1
    rtext = font.render(word, True, (0, 0, 0), (255, 255, 255))#背景色和汉字颜色
    if crop_flag:
        pygame.image.save(rtext, os.path.join(chinese_dir, str(ord(word)) + "-" + ".jpg"))
        file = "./" + chinese_dir + "/" + str(ord(word)) + "-" + ".jpg"
        img = Image.open(file)
        img_width=img.size[0]
        img_height=img.size[1]
        background.paste(img, (
            font_size// 2-img_width//2,
            font_size// 2-img_height//2
        ))
        background=background.resize((font_size,font_size), Image.ANTIALIAS)
        background = background.convert('RGB')
        background.save(file)
        img = cv2.imread(file)
        cv2.imencode('.jpg', img)[1].tofile("./"+chinese_dir+"/"+str(ord(word))+"-"+word+".jpg")
        os.remove(file)
        # pygame.image.save(rtext, os.path.join(chinese_dir, str(ord(word)) + "-" + ".jpg"))
        # file = "./" + chinese_dir + "/" + str(ord(word)) + "-" + ".jpg"
        # img = cv2.imread(file)
        # cropped = img[10:font_size+4, 0:font_size-6]  # 裁剪坐标为[y0:y1, x0:x1] 这里要根据fontsize自己调整
        # newpic = cv2.resize(cropped, (font_size,font_size), Image.ANTIALIAS)
        # cv2.imencode('.jpg', newpic)[1].tofile("./"+chinese_dir+"/"+str(ord(word))+"-"+word+".jpg")
        # os.remove(file)
    else:
        pygame.image.save(rtext, os.path.join(chinese_dir, str(ord(word)) + "-" + word + ".jpg"))
data=json.dumps(list,ensure_ascii=False)
ff = ""+chinese_dir+"/gen_list.json"
print("共生成"+str(num)+"字")
with open(ff,"w") as f:
    f.write(data)
f.close()
