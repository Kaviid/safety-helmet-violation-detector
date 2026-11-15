from pathlib import Path
import cv2
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt


print("Kaggle hardhat dataset size analyzing...")

sizes = {}

for f in Path("data/raw/kaggle_hardhat").rglob("*.xml"):
    size = ET.parse(f).getroot().find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)
    #print(width * height)

    key = f"{width}x{height}"
    if key in sizes:
        sizes[key] += 1
    else : 
        sizes[key] = 1

for key, value in sizes.items():
    print(f"{key} : {value}")