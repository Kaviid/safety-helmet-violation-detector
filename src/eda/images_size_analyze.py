from pathlib import Path
import cv2
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt


print("Kaggle hardhat dataset size analyzing...")

for f in Path("data/raw/kaggle_hardhat").rglob("*.xml"):
    size = ET.parse(f).getroot().find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)
    #print(width * height)