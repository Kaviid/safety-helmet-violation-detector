from pathlib import Path
import xml.etree.ElementTree as ET
import random
import cv2

# make output folders (exist_ok=True : means no error if they already exist. because sometime can file doesn't exist.)
Path("outputs/eda/topview").mkdir(parents=True, exist_ok=True)
Path("outputs/eda/kaggle").mkdir(parents=True, exist_ok=True)


# IITU top-view dataset -------------------------------------

iitu_files = []

for f in Path("data/raw/IITU_Safety-Helmet_Dataset").rglob("*.txt"):
    iitu_files.append(f) # we store full path

ten_files = random.sample(iitu_files, 10)

for label_path in ten_files:
    # find the matching image: .../annotations/x.txt -> .../images/x.jpg
    img_path = label_path.parent.parent / "images" / (label_path.stem + ".jpg")

    img = cv2.imread(str(img_path))
    if img is None:
        print("Image not found:", img_path)
        continue

    h, w = img.shape[:2]

    for line in label_path.read_text().splitlines():
        if not line.strip():
            continue

        parts = line.split()
        class_id = parts[0]
        xc = float(parts[1])
        yc = float(parts[2])
        bw = float(parts[3])
        bh = float(parts[4])

        # YOLO (0-1, centre) -> pixel corners
        x1 = int((xc - bw / 2) * w)
        y1 = int((yc - bh / 2) * h)
        x2 = int((xc + bw / 2) * w)
        y2 = int((yc + bh / 2) * h)

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, class_id, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imwrite(str(Path("outputs/eda/topview") / img_path.name), img)

print("Top-view done")


# Kaggle dataset -------------------------------------

kaggle_files = []

for f in Path("data/raw/kaggle_hardhat").rglob("*.xml"):
    kaggle_files.append(f)

ten_files = random.sample(kaggle_files, 10)

# a colour for each class (B, G, R)
colours = {
    "helmet": (0, 255, 0),      # green
    "head":   (0, 0, 255),      # red
    "person": (255, 0, 0),      # blue
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

    cv2.imwrite(str(Path("outputs/eda/kaggle") / img_name), img)

print("Kaggle done")