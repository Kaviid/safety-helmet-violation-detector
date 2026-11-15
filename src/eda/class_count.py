from pathlib import Path
import xml.etree.ElementTree as ET
import os

# Counting IITU Safety Helmet Dataset
print("'IITU_Safety-Helmet_Dataset' Dataset --------------------------------\n")

classes = {}
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
    text = f.read_text()

    for line in text.splitlines():
        if not line.strip():
            continue
        total_boxes += 1
        id = int(line.split()[0])
        if id not in classes:
            classes[id] = 1
        else :
            classes[id] += 1

print(f"Total images : {total_imgs}")
print(f"Label files  : {total_labels}")    
print(f"Empty files : {blank_label_file}")     
print(f"Total boxes : {total_boxes}")

for class_id, count in sorted(classes.items()):
    print(f"{class_id} : {count}")

# Counting Kaggle Dataset

k_total_labels = 0
k_blank_label_file = 0
k_total_boxes = 0
k_total_imgs = 0
k_classes = {}

for f in Path("data/raw/kaggle_hardhat").rglob("*.png"):
    k_total_imgs += 1

for f in Path("data/raw/kaggle_hardhat").rglob("*.xml"):
    tree = ET.parse(f)
    root = tree.getroot()
    objects = root.findall("object")

    if not objects:
        k_blank_label_file += 1
        continue

    k_total_labels += 1

    for obj in objects:
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