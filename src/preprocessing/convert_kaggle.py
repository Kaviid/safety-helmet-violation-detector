from pathlib import Path
import xml.etree.ElementTree as ET

person_count = 0
tiny_box_skip = 0

for f in Path("data/raw/kaggle_hardhat/annotations").rglob("*.xml"):
    root = ET.parse(f).getroot()
    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)
    objects = root.findall("object")

    for obj in objects:
        if obj.find("person").text == "person":
            person_count += 1
        else :
            bnd = obj.find("bndbox")
            xmin = int(bnd.find("xmin"))
            ymin = int(bnd.find("ymin"))
            xmax = int(bnd.find("xmax"))
            ymax = int(bnd.find("ymax"))

            box_w = xmax - xmin
            box_h = ymax - ymin
            if box_h < 5 or box_w < 5:
                tiny_box_skip += 1
                continue

            x_center = (xmin + xmax) / 2 / width
            y_center = (ymin + ymax) / 2 / height
            w        = box_w / width
            h        = box_h / height

            class_id = 0
            if obj.find("name").text == "head":
                class_id = 1

            #Convert to YOLO .txt
            #class_id  x_center  y_center  width  height