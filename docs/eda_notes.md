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