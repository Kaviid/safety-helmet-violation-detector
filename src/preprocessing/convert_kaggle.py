from pathlib import Path
import xml.etree.ElementTree as ET

for f in Path("data/raw/kaggle_hardhat/annotations").rglob("*.xml"):
    root = ET.parse(f).getroot()
    width = int(root.find("width").text)
    height = int(root.find("height").text)