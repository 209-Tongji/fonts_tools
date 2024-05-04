import svgwrite
import xml.etree.ElementTree as ET
import re
from random import randint
from itertools import groupby
import math
# sentence=input("请输入生成汉字：")

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







def change_d(line,a,b):
    ret = [''.join(list(g)) for k, g in groupby(line, key=is_num)]
    flag=0
    result=""
    sum=0
    for i in ret:
        if i.isnumeric():
            if flag % 2 ==0:
                if ret[sum-1]==" -":
                    ret[sum] = str(int(ret[sum])*(-1) + randint(a,b))
                else:
                    ret[sum]=str(int(ret[sum])+ randint(a,b))
            else:
                if ret[sum-1]==" -":
                    ret[sum] = str(int(ret[sum])*(-1) -  randint(a,b))
                else:
                    ret[sum] = str(int(ret[sum]) - randint(a,b))
            flag=flag+1
        if ret[sum]!=" -":
            result = result + ret[sum]
        else:
            result = result + " "
        sum=sum+1

    return(result)

def xie_d(line,angle):
    ret = [''.join(list(g)) for k, g in groupby(line, key=is_num)]
    flag=0
    result=""
    sum=0
    tan= math.tan((-1)*angle*math.pi/180)
    for i in ret:
        if i.isnumeric():
            if flag % 2 ==0:
                if ret[sum-1]==" -":
                    ret[sum] = str(int(ret[sum])*(-1) -int(ret[sum+2])*tan)
                else:
                    ret[sum]=str(int(ret[sum])-int(ret[sum+2])*tan)
            else:
                if ret[sum-1]==" -":
                    ret[sum] = str(int(ret[sum])*(-1))
                else:
                    ret[sum] = ret[sum]
            flag=flag+1
        if ret[sum]!=" -":
            result = result + ret[sum]
        else:
            result = result + " "
        sum=sum+1

    return(result)


#----------------------------------------
a=0#随机变化的坐标
b=0
angle=5#倾斜的角度
sentence="仰望星空脚踏实地"#生成的内容
speed=4#书写速度，越大越快
stop_time=0.15#每笔的停顿时间
dis = 1200 #字之间的间隔
scale=0.1 #整体大小
#----------------------------------------
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
#清除命名空间
for elem in root_base.iter():
    if not hasattr(elem.tag, 'find'): continue
    i = elem.tag.find('}')
    if i >= 0:
        elem.tag = elem.tag[i+1:]
p_base = ET.Element('image')
p_base.set("href", "0.jpg")
root_base.append(p_base)

#创建g_base

g_base = ET.Element('g')
g_base.set("transform", "scale("+str(scale)+", -" +str(scale)+") translate(8000, -900)")

root_base.append(g_base)

#创建style
style_elem = ET.Element('style', attrib={'type': 'text/css'})
style_elem.text = "1"
g_base.append(style_elem)

char_num=0
sum_clippath=0
sum_keyframes=0
style_elem.text=""
sum_time=0

for char in sentence:
    path_char="./svgs/"+str(ord(char))+".svg"
    svg_file = ET.parse(path_char)
    root = svg_file.getroot()
    keyframes = []
    for style in root.findall('.//{http://www.w3.org/2000/svg}style'):
        for line in style.text.split('\n'):
            ret = [''.join(list(g)) for k, g in groupby(line, key=lambda x: x.isdigit())]
            if "keyframes" in line or "make-me-a-hanzi-animation" in line:#改数字角标
                line=line.replace(ret[1],str(round(sum_keyframes//3)),1)
                sum_keyframes +=1
            if "animation: keyframes" in line:#改持续时间
                random_time=randint(-100,300)/250
                line = line.replace(ret[3]+ret[4]+ret[5], str((float(ret[3]+ret[4]+ret[5])+random_time) / speed), 1)
                sum_time=sum_time+(float(ret[3]+ret[4]+ret[5])   +random_time  ) / speed+stop_time
            if "animation-delay" in line:#改开始时间
                if (len(ret)<4):#无小数
                    line = line.replace(ret[1],str(sum_time), 1)
                else:
                    line = line.replace(ret[1] + ret[2] + ret[3], str(sum_time), 1)

            line=line.replace("blue","black")
            style_elem.text = style_elem.text+line+"\n"



    clippaths = svg_file.findall('.//{http://www.w3.org/2000/svg}clipPath')
    g = ET.Element('g')
    dis=dis+randint(-40,80)
    x=str(randint(-30,30))
    y=str(-1*dis*char_num)
    scale=0.8
    g.set("transform", "scale(" + str(scale) + ", " + str(scale) + ") translate("+x+","+y+")")


    paths = svg_file.findall('.//{http://www.w3.org/2000/svg}path')
    path_num=0

    for clip_path in clippaths:
        # 修改clippath的id"
        g_clip = ET.Element('g')
        g_clip.set("transform", "scale(0.8,0.8) translate(0,0)")

        clip_path.set('id', f'make-me-a-hanzi-clip-{str(sum_clippath)}')
        path_element = clip_path.findall('.//{http://www.w3.org/2000/svg}path')
        d_value = change_d(path_element[0].get('d'),a,b)#变化范围
        d_value = xie_d(d_value, angle)  # 倾斜角度
        path_element[0].set('d', d_value)
        g.append(clip_path)
        paths[len(clippaths)+1+2*path_num].set('clip-path', f'url(#make-me-a-hanzi-clip-{str(sum_clippath)})')
        paths[len(clippaths)+1+2*path_num].set('id', f'make-me-a-hanzi-animation-{str(sum_clippath)}')
        d2_value=xie_d(paths[len(clippaths)+1+2*path_num].get('d'), angle)
        paths[len(clippaths)+1+2*path_num].set('d', d2_value)
        g.append(paths[len(clippaths)+1+2*path_num])
        sum_clippath+=1
        path_num+=1
    g_base.append(g)
    char_num+=1



tree_base = ET.ElementTree(root_base)
for elem in tree_base.iter():
    if not hasattr(elem.tag, 'find'): continue
    i = elem.tag.find('}')
    if i >= 0:
        elem.tag = elem.tag[i+1:]
tree_base.write('output.svg', encoding='utf-8', xml_declaration=True)
