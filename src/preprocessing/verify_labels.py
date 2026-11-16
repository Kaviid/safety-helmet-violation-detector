import os
from pathlib import Path

#Check converting all good!
"""
Recount the new labels. I already have YOLO counting code from the top-view part of class_count.py. 
Point it at data/processed/kaggle/labels and run it. Expected: 

    Total boxes: 24,712 (24,751 − 39 tiny)
    Class 0 + class 1 = 24,712
    Only IDs 0 and 1, no others

I run that code in here...
"""
print("\nChecking YOLO labels accuracy...")

classes = {}
total_labels = 0
blank_label_file = 0
total_boxes = 0
total_imgs = 0

for f in Path("data/processed/kaggle/images").rglob("*.png"):
    total_imgs += 1

for f in Path("data/processed/kaggle/labels").rglob("*.txt"):
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


