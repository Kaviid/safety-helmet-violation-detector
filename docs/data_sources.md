# EDA Notes

I wrote a script (`src/eda/class_count.py`) to count the labels in both datasets automatically. The goal is to check the data before using it to train the model.

---

## 1. IITU Safety Helmet Dataset (top-view)

### Results

| Item | Count |
|---|---|
| Total images | 1,664 |
| Label files with boxes | 1,657 |
| Empty label files | 7 |
| Total boxes | 6,471 |

Every image has a label file (1,657 + 7 = 1,664).

### Boxes per class

| Class ID | Boxes | Likely meaning |
|---|---|---|
| 0 | 1,359 | Blue helmet |
| 1 | 1,133 | Green helmet |
| 2 | 1,216 | Red helmet |
| 3 | 1,401 | White helmet |
| 4 | 1,362 | Yellow helmet |

### What I found

- The dataset has no class file, so I had to work out the classes myself.
- Only class IDs 0 to 4 exist. They look like 5 helmet colours (based on checking one sample image).
- The 5 classes are fairly balanced (1,133 to 1,401 boxes each).
- There are no boxes for workers without helmets. This dataset only shows workers wearing helmets.
- 7 label files are empty. I need to decide whether to keep or remove these images in preprocessing.

---

## 2. Kaggle Hard Hat Dataset

### Results

| Item | Count |
|---|---|
| Total images | 5,000 |
| Label files with boxes | 5,000 |
| Empty label files | 0 |
| Total boxes | 25,502 |

Every image has a label file, and none of them are empty.

### Boxes per class

| Class name | Boxes | My class |
|---|---|---|
| helmet | 18,966 | helmet |
| head | 5,785 | no_helmet |
| person | 751 | dropped |

### What I found

- `head` means a worker without a helmet, so I will rename it to **no_helmet**.
- `person` has only 751 boxes, but almost every image has people in it. Most people are not labelled, so this class is not reliable. I will drop it.
- This is the only dataset with no_helmet examples, and they are all eye-level photos.

---

## 3. Combined Class Balance

| Class | Kaggle | Top-view | Total |
|---|---|---|---|
| helmet | 18,966 | 6,471 | **25,437** |
| no_helmet | 5,785 | 0 | **5,785** |

- There are about **4.4 helmet boxes for every 1 no_helmet box**. The data is imbalanced.
- This can make the model favour "helmet" and miss workers without helmets, which hurts recall on no_helmet (my most important target).
- There are no top-view no_helmet examples at all. The model may struggle to spot bare heads from a high CCTV angle.

---

## What this means for the project

- Merge all 5 top-view colour classes into one class: **helmet**.
- Rename Kaggle `head` to **no_helmet** and drop `person`.
- Add more no_helmet data later, especially from a top-down angle (the 348 mixed images and some of the 7,000 unlabelled images).
- Watch no_helmet recall closely during evaluation.

