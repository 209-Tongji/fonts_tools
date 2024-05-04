 #encoding: utf-8
import os
import cv2
import json

char = '我'



chn_dec = json.load(open("./chn_decompose.json"))
uid_c = {}
pll=[]
unicode_val = hex(ord(char))
unicode_val =unicode_val[2:].upper()
for c, decs in chn_dec.items():
    if unicode_val==c:
        res=decs
    if len(decs) > 1:
        continue
    else:
        pll.append([decs[0],chr(int(c, 16))])

result=[]
for i in res:
    for j in pll:
        if i==j[0]:
            result.append(j[1])
print(result)
