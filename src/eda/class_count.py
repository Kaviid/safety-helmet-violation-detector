from pathlib import Path
import xml.etree.ElementTree as ET
import os

# Counting IITU Safety Helmet Dataset
print("'IITU_Safety-Helmet_Dataset' Dataset --------------------------------\n")

classes = [0,0,0,0,0,0]
total_labels = 0
blank_label_file = 0
total_boxes = 0
total_imgs = 0

for f in Path("data/raw/IITU_Safety-Helmet_Dataset").rglob("*.jpg"):
    total_imgs += 1

for f in Path("data/raw/IITU_Safety-Helmet_Dataset").rglob("*.txt"):
    if os.path.getsize(f) == 0:
        blank_label_file += 1
        continue

    total_labels += 1

    with open(f) as file:
        text = file.read()
        s = text.splitlines()
        for line in s:
            total_boxes += 1
            id = int(line.split()[0])
            classes[id] += 1

print(f"Total images : {total_imgs}")
print(f"Label files  : {total_labels}")    
print(f"Empty files : {blank_label_file}")     
print(f"Total boxes : {total_boxes}")

k = 0
while k < len(classes) and classes[k] != 0:
    print(f"{k} : {classes[k]}")
    k += 1

# Counting Kaggle Dataset

k_total_labels = 0
k_blank_label_file = 0
k_total_boxes = 0
k_total_imgs = 0
k_classes = {}

for f in Path("data/raw/kaggle_hardhat").rglob("*.png"):
    k_total_imgs += 1

for f in Path("data/raw/kaggle_hardhat").rglob("*.xml"):
    if os.path.getsize(f) == 0:
        k_blank_label_file += 1
        continue

    k_total_labels += 1

    tree = ET.parse(f)
    root = tree.getroot()

    for obj in root.findall("object"):
        k_total_boxes += 1
        class_name = obj.find("name").text
        if class_name not in k_classes:
            k_classes[class_name] = 1
        else:
            k_classes[class_name] += 1

print("\n'Kaggle_hardhat' Dataset --------------------------------\n")
print(f"Total images : {k_total_imgs}")
print(f"Label files  : {k_total_labels}")    
print(f"Empty files : {k_blank_label_file}")     
print(f"Total boxes : {k_total_boxes}")
print(k_classes)