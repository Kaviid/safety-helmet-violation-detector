from pathlib import Path
import random
import shutil

base = Path("data/processed/kaggle_split")
for sub in ["images", "labels"]:
    for split in ["train", "val", "test"]:
        (base / sub / split).mkdir(parents=True, exist_ok=True)

images = sorted(Path("data/processed/kaggle/images").glob("*.png"))

random.seed(42)
random.shuffle(images)

n = len(images)              # 5000
train_end = int(n * 0.7)    # 3500
val_end   = int(n * 0.9)    # 4500

train = images[:train_end]          # 0 → 3499
val   = images[train_end:val_end]   # 3500 → 4499
test  = images[val_end:]            # 4500 → end

splits = {"train": train, "val": val, "test": test}
split_record = {"train": 0, "val": 0, "test": 0}
for split_name, split_file in splits.items():
    dst_img = Path(f"data/processed/kaggle_split/images/{split_name}")
    dst_lab = Path(f"data/processed/kaggle_split/labels/{split_name}")
    for i in split_file:
        shutil.copy2(i, dst_img) # copies into that folder 
        l = Path(f"data/processed/kaggle/labels/{i.stem}.txt")
        shutil.copy2(l,dst_lab)
        split_record[split_name] += 1

for key,count in split_record.items():
    print(f"{key} : {count}")