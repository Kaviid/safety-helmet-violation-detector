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