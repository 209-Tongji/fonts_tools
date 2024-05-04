import svgwrite
import xml.etree.ElementTree as ET
import re
from random import randint
from itertools import groupby
import math
import cv2
# sentence=input("请输入生成汉字：")
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from PIL import Image
import random

def is_num(string):
    try:
        float(string)
        return True
    except ValueError:
        if string.startswith('-'):
            try:
                float(string[1:])
                return True
            except ValueError:
                pass
        elif string.startswith('.'):
            try:
                float('0' + string)
                return True
            except ValueError:
                pass
        return False

def extract_middle(image_path, output_path):
    # 打开原始图像
    image = Image.open(image_path)

    # 计算中心区域的范围
    width, height = image.size
    left = (width - 256) // 2
    top = (height - 256) // 2
    right = left + 256
    bottom = top + 256

    # 提取中心区域
    cropped_image = image.crop((left, top, right, bottom))

    # 保存提取的图像
    cropped_image.save(output_path)

#----------------------------------------
a=0#随机变化的坐标
b=100
angle=30#倾斜的角度
sentence="杜"#生成的内容
speed=10#书写速度，越大越快
stop_time=0.04#每笔的停顿时间
dis = 1200 #字之间的间隔
scale=0.3 #整体大小
lianbi=True
#----------------------------------------
import os

def get_all_filenames(folder_path):
    # 获取文件夹中的所有文件和文件夹
    all_items = os.listdir(folder_path)

    # 过滤出所有文件的名称
    file_names = [item for item in all_items if os.path.isfile(os.path.join(folder_path, item))]

    return file_names

# 使用示例
folder_path = "./svgs/"
filenames = get_all_filenames(folder_path)

for filename in filenames:

    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    # 创建SVG根元素并添加xmlns属性
    root_base = ET.Element(
        '{http://www.w3.org/2000/svg}svg',
        attrib={
            'xmlns': 'http://www.w3.org/2000/svg',
            'version': '1.1',
            'viewBox': '0 0 1024 1024'
        }
    )
    # 清除命名空间
    for elem in root_base.iter():
        if not hasattr(elem.tag, 'find'): continue
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i + 1:]
    # 创建g_base
    g_base = ET.Element('g')
    g_base.set("transform", "scale(" + str(scale) + ", -" + str(scale) + ") translate(1300, -2000)")

    root_base.append(g_base)

    # 创建style
    style_elem = ET.Element('style', attrib={'type': 'text/css'})
    style_elem.text = "1"
    g_base.append(style_elem)

    char_num = 0
    sum_clippath = 0
    sum_keyframes = 0
    style_elem.text = ""
    sum_time = 0
    path_char = filename
    svg_file = ET.parse(folder_path+path_char)
    root = svg_file.getroot()
    keyframes = []


    clippaths = svg_file.findall('.//{http://www.w3.org/2000/svg}clipPath')
    g = ET.Element('g')

    y=str(-1*dis*char_num)
    scale1=0.8
    g.set("transform", "scale(" + str(scale1) + ", " + str(scale1) + ") translate(0,"+y+")")


    paths = svg_file.findall('.//{http://www.w3.org/2000/svg}path')
    path_num=0
    path_flag=False
    for path in paths:
        # 修改clippath的id"


        fill=path.get('fill')
        if fill=="lightgray":
            continue
        try:
            id=path.get('id')
            flag= "animation" in id
        except:
            continue
        path.set("stroke","#000")
        path.set("stroke-width", "12")
        del path.attrib["clip-path"]
        g.append(path)
        line=path.get('d')
        ret = [''.join(list(g)) for k, g in groupby(line, key=is_num)]
        path2=ret[1]
        path3 =ret[3]


        random_integer = random.randint(1, 10)
        if path_flag and lianbi:
            path_element = ET.Element("path")
            path_data="M "+str(path0)+" "+str(path1)+" Q "+str(path2)+" "+str(path1)+" "+str(path2)+" "+str(path3)
            path_element.set("stroke", "black")
            path_element.set("stroke-width", "12")
            path_element.set("stroke-linecap", "round")
            path_element.set("fill", "none")
            path_element.set("d", path_data)  # 设置路径数据
            g.append(path_element)
        path_flag=True
        path0=ret[-3]
        path1 =ret[-1]
    g_base.append(g)
    char_num+=1
    tree_base = ET.ElementTree(root_base)
    for elem in tree_base.iter():
        if not hasattr(elem.tag, 'find'): continue
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i+1:]
    tree_base.write('output1.svg', encoding='utf-8', xml_declaration=True)
    drawing = svg2rlg("output1.svg")
    renderPM.drawToFile(drawing, "re.png", fmt="PNG")
    # 使用示例
    original_image_path = "re.png"
    idd=filename.replace(".svg","")
    output_image_path =  "output/"+idd+".png"
    if lianbi:
        output_image_path = "output3/" + idd + ".png"
    extract_middle(original_image_path, output_image_path)
