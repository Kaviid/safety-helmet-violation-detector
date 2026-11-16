# Model Selection

There are 5 decisions when choosing a model.

## 1. Classifier or detector?
A classifier gives one label for the whole image, so it can't say which worker has no helmet in a crowded image.
I use a detector, because a CCTV frame has many workers and I need to know which one is not wearing a helmet.

**Choice:** `Detector`

## 2. Which detector family?
I use the YOLO family (You Only Look Once).
- The image goes through a CNN, which builds the features I learned about in the feature engineering phase.
- Duplicate boxes on the same head are cleaned up, so I get one box per head.
- It finds every object in one pass through the network. That's why it's fast enough for live video.

I use the YOLO26 version.

**Choice:** `YOLO26`

## 3. Train from zero or use transfer learning?
Transfer learning means starting from a model that is already trained on a huge dataset (COCO: hundreds of thousands of everyday images, 80 classes like person, car and dog), and then fine-tuning it on my helmet data.

Why it works: the early and middle layers already know edges, shapes and textures. These are useful for any image. I only need to teach the model the last step: "this shape = helmet, this shape = bare head".

**Choice:** `Transfer learning`

## 4. Which size?
YOLO26 comes in five sizes: Nano (n), Small (s), Medium (m), Large (l) and Extra Large (x). They balance speed, size and accuracy.

Bigger models are more accurate but slower and need more GPU memory. My limits are an RTX 4050 (6 GB) and at least 15 FPS.

**Choice:** `Train YOLO26n and YOLO26s, compare them, and pick the better one`

## 5. Training image size?
From EDA, the images are 416×416 and most heads are 20 to 45 px wide.
Upscaling does not add detail, but it gives the deep layers more pixels to work with. This often helps with small objects.

**Choice:** `Baseline at 640 (YOLO's default), then test 416 later in tuning`

## My baseline
My first training run: YOLO26n, pretrained, image size 640, default settings.