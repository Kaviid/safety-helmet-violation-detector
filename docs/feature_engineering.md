# Feature Engineering (CNN)

In normal ML, I choose the features myself (like attendance or study hours). With images, the CNN finds the features by itself during training.

## 1. Why I can't pick features by hand
An image is just a big grid of numbers (pixels). A 416×416 colour image has over 500,000 numbers. No single pixel means "helmet". A helmet is a pattern made of many pixels: a round shape, a smooth surface, a brim. I can't write rules for all of that by hand, so the CNN learns the patterns from my labelled images.

## 2. Filters and feature maps
- A filter is a small grid of numbers (for example 3×3).
- It slides over the image and checks how well each area matches its pattern.
- The result is a feature map. It shows where in the image that pattern appears.
- I don't choose the filter numbers. They start random, and training adjusts them until they find useful patterns.

## 3. Early layers vs deep layers
- Early layers find simple things like edges, lines and colours.
- Middle layers combine those into shapes and textures.
- Deep layers combine shapes into object parts, like a helmet or a bare head.
- Each layer builds on the one before it. This is why it is called "deep" learning.

## 4. Why small heads are hard
- The CNN shrinks the feature maps between layers to work faster.
- Each time it shrinks, some detail is lost.
- A far-away head that is only a few pixels wide can almost disappear in the deep layers.
- This is why image size matters, and why small, far-away workers are harder to detect.

## What I already did that counts as feature engineering
- Chose the classes (helmet and no_helmet).
- Cleaned the labels (dropped person boxes and tiny boxes).
- Augmentation (flips, brightness, blur) comes later in training.