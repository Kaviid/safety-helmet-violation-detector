from pathlib import Path
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt


print("Kaggle hardhat dataset size analyzing...\n")

sizes = {}
boxes_per_img = []

for f in Path("data/raw/kaggle_hardhat").rglob("*.xml"):
    root = ET.parse(f).getroot()
    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)
    #print(width * height)

    key = f"{width}x{height}"
    if key in sizes:
        sizes[key] += 1
    else : 
        sizes[key] = 1

    objects = root.findall("object")
    #boxes_per_img.append(len(objects))
    count = 0
    for obj in objects:
        if obj.find("name").text != "person":
            count += 1
    boxes_per_img.append(count)

for key, value in sizes.items():
    print(f"{key} : {value}")

#print(boxes_per_img)
print("\nBoxes per image analyzing...\n")
print(f"Min : {min(boxes_per_img)}")
print(f"Max : {max(boxes_per_img)}")
print(f"Avg : {sum(boxes_per_img)/len(boxes_per_img)}")