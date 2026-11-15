from pathlib import Path
import os

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

