import numpy as np
from pathlib import Path
import xml.etree.ElementTree as ET

print("Broken boxes checking...")

problems = []
for f in Path("data/raw/kaggle_hardhat").rglob("*.xml"): 
    tree = ET.parse(f)
    root = tree.getroot()
    width = int(root.find("size").find("width").text)
    height = int(root.find("size").find("height").text)
    objects = root.findall("object")
    
    for obj in objects:
        if obj.find("name").text != "person":
            bnd = obj.find("bndbox")
            xmin = int(bnd.find("xmin").text)
            xmax = int(bnd.find("xmax").text)
            ymin = int(bnd.find("ymin").text)
            ymax = int(bnd.find("ymax").text)

            def add_problems(reason):
                problems.append((f.name, obj.find("name").text, xmin, ymin, xmax, ymax, reason))

            if xmin == xmax or ymin == ymax :
                add_problems("0 pixels wide")
                continue
            if xmin > xmax :
                add_problems("bad width")
                continue
            if ymin > ymax :
                add_problems("bad height")
                continue
            if xmin < 0 or ymin < 0 :
                add_problems("starts outside the image")
                continue
            if xmax > width or ymax > height :
                add_problems("ends outside the image")
                continue

print(f"{len(problems)}\n")
#for i in problems: #Use test file in my pc > document
#    print(i)

print("Box sizes analyzing...")

area_list = []
for f in Path("data/raw/kaggle_hardhat").rglob("*.xml"):
    tree = ET.parse(f)
    root = tree.getroot()
    objects = root.findall("object")
    for obj in objects :
        if obj.find("name").text != "person":
            bnd = obj.find("bndbox")
            xmin = int(bnd.find("xmin").text)
            xmax = int(bnd.find("xmax").text)
            ymin = int(bnd.find("ymin").text)
            ymax = int(bnd.find("ymax").text)       

            box_w = xmax - xmin
            box_h = ymax - ymin
            area = box_w * box_h
            area_list.append((f.name , area))

print(f"{len(area_list)}") #Must equal to 24,751

#for i in area_list[:10]: #For sample show of list
#    print(f"{i[0]} : {i[1]}")

print(f"Min : {min(area_list, key=lambda p: p[1])}")
print(f"Max : {max(area_list, key=lambda p: p[1])}")
total = 0
for i in area_list:
    total += i[1]
print(f"Avg : {total/len(area_list)}")