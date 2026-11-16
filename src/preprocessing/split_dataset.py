from pathlib import Path
import xml.etree.ElementTree as ET
import random

base = Path("data/processed/kaggle_split")
for sub in ["images", "labels"]:
    for split in ["train", "val", "test"]:
        (base / sub / split).mkdir(parents=True, exist_ok=True)

images = []
images = sorted(Path("data/processed/kaggle/images").glob("*.png"))

random.seed(42)
random.shuffle(images)

n = len(images)              # 5000
train_end = int(n * 0.7)    # 3500
val_end   = int(n * 0.9)    # 4500

train = images[:train_end]          # 0 → 3499
val   = images[train_end:val_end]   # 3500 → 4499
test  = images[val_end:]            # 4500 → end