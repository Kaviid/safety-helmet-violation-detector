import numpy as np
from pathlib import Path
import xml.etree.ElementTree as ET
import cv2

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

#print(f"{len(problems)}\n")
#for i in problems: #Use test file in my pc > document
#    print(i)

print("Box sizes analyzing...")

tiny_boxes_5 = [] # For count tiny boxes size and store that file
tiny_boxes_8 = []
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

            if box_w < 5 or box_h < 5:
                tiny_boxes_5.append(f.name)
            if box_w < 8 or box_h < 8:
                tiny_boxes_8.append(f.name)          


#print(f"{len(area_list)}") #Must equal to 24,751

#for i in area_list[:10]: #For sample show of list
#    print(f"{i[0]} : {i[1]}")

print("IQR outliers on area analyzing...\n")

nums = []
for i in area_list:
    nums.append(i[1])

q1 = np.percentile(nums, 25) # %25
q3 = np.percentile(nums, 75) # %75

#Results....

print(f"Total boxes checked : {len(area_list)}")
print(f"Broken boxes : {len(problems)}")
print(f"Min : {min(area_list, key=lambda p: p[1])}")
print(f"Max : {max(area_list, key=lambda p: p[1])}")

total = 0
for i in area_list:
    total += i[1]
print(f"Avg : {total/len(area_list)}")
print(f"Area q1 : {q1}")
print(f"Area q3 : {q3}")

iqr = q3 - q1
lower_f = q1 - 1.5 * iqr
higher_f = q3 + 1.5 * iqr

print(f"IQR : {iqr}")
print(f"Lower fence : {lower_f}")
print(f"Upper fence : {higher_f}")

outliers = []
for i in area_list:
    if i[1] < lower_f:
        outliers.append((i[0], i[1], "small outlier"))
        continue
    if i[1] > higher_f:
        outliers.append((i[0], i[1], "big outlier"))

outliers.sort(key=lambda p: p[1], reverse=True) #Sort the pairs by area biggest ones come to first
print(f"Top 5 biggest : {outliers[:5]}")

outliers.sort(key=lambda p: p[1]) #Sort again smallest one come to first
print(f"Top 5 smallest : {outliers[:5]}")

print(f"\nTiny boxes < 5 : {len(tiny_boxes_5)}")
print(f"Tiny boxes < 8 : {len(tiny_boxes_8)}")

#I got 5 biggest and 5 smallest area so we must find are those what? 
#So let's again visualize these...

Path("outputs/eda/kaggle_outlier").mkdir(parents=True, exist_ok=True)

kaggle_files = []

for f in Path("data/raw/kaggle_hardhat").rglob("*.xml"):
    kaggle_files.append(f)

#Got file names from top 5 biggest and smallest area...
ten_files = ["data/raw/kaggle_hardhat/annotations/hard_hat_workers2944.xml", "data/raw/kaggle_hardhat/annotations/hard_hat_workers2437.xml", 
             "data/raw/kaggle_hardhat/annotations/hard_hat_workers4302.xml" , "data/raw/kaggle_hardhat/annotations/hard_hat_workers554.xml", 
             "data/raw/kaggle_hardhat/annotations/hard_hat_workers2900.xml", "data/raw/kaggle_hardhat/annotations/hard_hat_workers3255.xml", 
             "data/raw/kaggle_hardhat/annotations/hard_hat_workers4396.xml", "data/raw/kaggle_hardhat/annotations/hard_hat_workers2280.xml", 
             "data/raw/kaggle_hardhat/annotations/hard_hat_workers1501.xml", "data/raw/kaggle_hardhat/annotations/hard_hat_workers308.xml"]

colours = {
    "helmet": (0, 255, 0),      # green
    "head":   (0, 0, 255),      # red
}

for xml_path in ten_files:
    root = ET.parse(xml_path).getroot()

    # the XML tells us the image name
    img_name = root.find("filename").text
    img_path = Path("data/raw/kaggle_hardhat/images") / img_name

    img = cv2.imread(str(img_path))
    if img is None:
        print("Image not found:", img_path)
        continue

    for obj in root.findall("object"):
        name = obj.find("name").text
        box = obj.find("bndbox")

        # XML already has pixel corners, no conversion needed
        x1 = int(box.find("xmin").text)
        y1 = int(box.find("ymin").text)
        x2 = int(box.find("xmax").text)
        y2 = int(box.find("ymax").text)

        colour = colours[name]
        cv2.rectangle(img, (x1, y1), (x2, y2), colour, 1)
        cv2.putText(img, name, (x1, y1 - 3),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, colour, 1)

    cv2.imwrite(str(Path("outputs/eda/kaggle_outlier") / img_name), img)

print("Kaggle outlier box draw done")