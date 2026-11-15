# EDA Notes

## IITU Safety Helmet Dataset: Class Count

I wrote a script (`src/eda/class_count.py`) to count the labels automatically. The goal is to check the dataset before using it to train the model.

### Results

| Item | Count |
|---|---|
| Total images | 1,664 |
| Label files with boxes | 1,657 |
| Empty label files | 7 |
| Total boxes | 6,471 |

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
- 7 label files are empty. These images have no boxes, so I need to decide whether to keep or remove them in preprocessing.

### What this means for the project

- I will merge all 5 colour classes into one class: **helmet**.
- This dataset cannot teach the model what **no_helmet** looks like. The no_helmet examples must come from other datasets.

### Next steps

- Visually check a few images for each class ID to confirm the colour meanings.
- Check the 7 empty label files.