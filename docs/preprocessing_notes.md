## Convert XML to YOLO
Run : `python src/preprocessing/convert_kaggle.py`

- Converted all 5,000 Kaggle XML files to YOLO .txt format.
- Class mapping: helmet → 0, head → 1 (no_helmet).
- Skipped 751 person boxes and 39 tiny boxes (width or height under 5 px).
- Result: 24,712 boxes (18,931 helmet, 5,781 no_helmet).
- Output: `data/processed/kaggle/` (images + labels). `data/raw/` is not changed.

## Train / Val / Test Split
Run : `python src/preprocessing/split_dataset.py`

- Random split with seed 42 (70 / 20 / 10).

| Split | Images | helmet | no_helmet | Ratio |
|---|---|---|---|---|
| train | 3,500 | 13,406 | 4,051 | 3.31 |
| val | 1,000 | 3,697 | 1,150 | 3.21 |
| test | 500 | 1,828 | 580 | 3.15 |

- All splits have a similar helmet : no_helmet ratio, so the split is balanced.

## Dataset Config (data.yaml)
Run : `python src/preprocessing/make_data_yaml.py`

- Creates `configs/kaggle_v1.yaml`, which tells YOLO where the train, val and test images are and what each class ID means.
- The script finds the dataset path on the current computer, so it works after cloning to any folder.
- YOLO finds the labels by itself by swapping `images` for `labels` in each image path.
  
## Verify YOLO Labels
Run : `python src/preprocessing/verify_labels.py`

- I drew the converted YOLO labels back onto random train images.
- Boxes sit correctly on the heads for both classes (helmet = green, no_helmet = red).
- The XML to YOLO conversion is correct.
- Known limitation: some images have mirrored edges with upside-down heads. Boxes there are bigger than 5 px, so they were kept. This is mild noise and I accept it for v1.