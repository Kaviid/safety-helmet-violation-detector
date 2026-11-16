## Decision: Drop the top-view dataset for v1 (Version 1)

I will not use the IITU top-view dataset to train the first model.

**Why:**
- It only has helmet labels (6,471 boxes) and no no_helmet labels. This makes the class imbalance worse (4.4 : 1 instead of 3.3 : 1).
- Some helmets are labelled even when workers hold them in their hands, not wear them.
- Some bare heads have no label, so the model would learn that bare heads are background.

**What I lose:**
- Top-view (CCTV angle) images and night images.

**Plan:**
- Train v1 on the Kaggle dataset only.
- Test v1 on top-view CCTV video in evaluation.
- If v1 struggles from above, add a cleaned top-view subset or new top-view no_helmet data in v2.
- The files stay in `data/raw/` and are not deleted.

## Kaggle: Image Sizes and Boxes per Image
Run : `python src/eda/images_size_analyze.py`
### Image sizes

| Size | Images |
|---|---|
| 416×416 | 2,192 |
| 416×415 | 2,461 |
| 415×416 | 324 |
| 415×415 | 23 |

- All images are about 416×416. The 415 sizes are only 1 pixel off, so it does not matter.
- The images are small. Training at a bigger size (like 640) will scale them up but will not add real detail.

### Boxes per image (helmet + head only)

| Item | Value |
|---|---|
| Min | 1 |
| Max | 68 |
| Average | 4.95 |
| Total | 24,751 |

- Every image has at least one helmet or head box, so there are no empty images to remove.
- Most images have about 5 heads.
- Some images are very crowded (up to 68 heads). Small, packed heads are harder for the model to detect.

### Boxes per image histogram

![Boxes per image](../outputs/eda/boxes_per_image.png)

- About 61% of images have only 1 to 4 heads.
- Very few images have more than 14 heads.
- The data is right-skewed: most images have few heads, and a small number are very crowded.
- The model may find crowded scenes harder because it sees fewer of them.

## Kaggle: Box Sizes and Outliers
Run : `python src/eda/box_stats.py`

### Broken boxes

- I checked every helmet and head box for impossible corners (zero size, backwards, or outside the image).
- Broken boxes found: 0

### Box sizes (area in pixels)

| Item | Value |
|---|---|
| Q1 | 420 (about 20×20 px) |
| Q3 | 2,080 (about 45×45 px) |
| IQR | 1,660 |
| Lower fence | -2,070 |
| Upper fence | 4,570 (about 68×68 px) |

- The middle 50% of heads are about 20 to 45 px wide.
- The lower fence is negative, so IQR finds no small outliers. This happens because the data is right-skewed.

### Big outliers

- I drew the 5 biggest boxes. They are real close-up portraits of workers.
- Decision: keep them.

### Tiny boxes

- I drew the 5 smallest boxes. Some images have mirrored edges, and the boxes were copied into those areas. This creates tiny slivers of upside-down heads and helmets.
- IQR did not catch these tiny boxes.

| Rule | Boxes | % |
|---|---|---|
| Width or height < 5 px | 39 | 0.16% |
| Width or height < 8 px | 285 | 1.15% |

- Decision: remove boxes with width or height under 5 px during preprocessing.
- I keep boxes from 5 to 8 px because some may be real far-away heads.

### Lesson learned

- I first deleted whole images and XML files from `data/raw/`. This removed about 365 good boxes along with the 39 tiny ones.
- I restored the dataset from the original download.
- Rule: never change `data/raw/`. Remove bad boxes in preprocessing, one box at a time.