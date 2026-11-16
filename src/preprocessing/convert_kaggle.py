from pathlib import Path
import xml.etree.ElementTree as ET
import shutil
import os

print("YOLO converting start - Dataset Preprocessing...")

person_count = 0
tiny_box_skip = 0
CLASS_MAP = {"helmet": 0, "head": 1}
preprocessed_file_count = 0

base = Path("data/processed/kaggle") #Base folder
for sub in ["images", "labels"]: #Sub folders
    (base / sub).mkdir(parents=True, exist_ok=True)

txt_file_path = Path("data/processed/kaggle/labels")
img_file_path = Path("data/processed/kaggle/images")

for f in Path("data/raw/kaggle_hardhat/annotations").rglob("*.xml"):
    root = ET.parse(f).getroot()
    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)
    objects = root.findall("object")
    lines = []

    for obj in objects:
        if obj.find("name").text == "person":
            person_count += 1
        else :
            bnd = obj.find("bndbox")
            xmin = int(bnd.find("xmin").text)
            ymin = int(bnd.find("ymin").text)
            xmax = int(bnd.find("xmax").text)
            ymax = int(bnd.find("ymax").text)

            box_w = xmax - xmin
            box_h = ymax - ymin
            if box_h < 5 or box_w < 5:
                tiny_box_skip += 1
                continue

            x_center = (xmin + xmax) / 2 / width
            y_center = (ymin + ymax) / 2 / height
            w        = box_w / width
            h        = box_h / height

            try :
                class_id = CLASS_MAP[obj.find("name").text]
            except KeyError :
                print(f"Unknown label found! : {f.name}")
                continue

            #Convert to YOLO .txt
            #class_id  x_center  y_center  width  height
            lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")

    file_name = f.stem + ".txt"
    with Path(txt_file_path/file_name).open("w") as l:
        for box in lines:
            l.write(box + "\n")
    img_file = Path(f.stem + ".png")
    src = Path("data/raw/kaggle_hardhat/images"/img_file)
    dst = Path("data/processed/kaggle/images")
    shutil.copy2(src, dst) # copies into that folder keeps the same name
    preprocessed_file_count += 1
    print(f"Updated [{preprocessed_file_count}] - {f.stem}.png | {f.stem}.txt")

print(f"\n{preprocessed_file_count} files preprocessed!")
print(f"Person label skipped : {person_count}")
print(f"Tiny boxes < 5px skipped : {tiny_box_skip}")