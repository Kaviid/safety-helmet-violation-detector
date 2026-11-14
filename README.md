# 🦺 Safety Helmet Detection from CCTV Video

A deep learning project that detects construction workers who are **not wearing safety helmets** in CCTV footage. The model finds each worker in a video frame, checks for a helmet, and raises an alert when someone isn't wearing one.

> 🚧 **Status:** In progress. I'm building this step by step to learn the full machine learning pipeline.

---

## 📌 Problem

Head injuries are one of the most common accidents on construction sites. Supervisors can't watch every camera all day, so workers without helmets often go unnoticed.

This project builds a supervised object detection model that:
- Finds every worker in a CCTV frame
- Classifies each one as **helmet** or **no helmet**
- Flags violations so the site can act quickly

**Goal:** High recall on the `no_helmet` class. Missing an unsafe worker is worse than a false alarm.

---

## 🧠 Approach

I'm following the full machine learning pipeline:

1. **Problem Definition**: define the goal, classes and success targets
2. **Data Collection**: public helmet datasets plus CCTV-style video frames
3. **Exploratory Data Analysis**: class balance, box sizes, image quality
4. **Data Preprocessing**: cleaning, relabelling, outlier removal, splitting, augmentation
5. **Feature Engineering**: the CNN learns its own features from images
6. **Model Selection**: YOLO object detection with transfer learning
7. **Training & Tuning**: hyperparameter tuning and model comparison
8. **Evaluation**: precision, recall, F1, mAP, confusion matrix, error analysis
9. **Deployment**: real-time video detection with alerts
10. **Monitoring**: handling new sites, cameras and conditions

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Main language |
| PyTorch | Deep learning framework |
| Ultralytics YOLO | Object detection model |
| OpenCV | Video processing and drawing results |
| pandas, NumPy | Data handling |
| Matplotlib, Seaborn | Data visualization |

**Hardware:** NVIDIA GeForce RTX 4050 Laptop GPU (6 GB)

---

## 📁 Project Structure

```
helmet-detection/
├── data/              ← ignored by Git (too big)
│   ├── raw/           ← original downloaded datasets
│   ├── videos/        ← CCTV videos
│   ├── frames/        ← frames extracted from videos
│   └── processed/     ← cleaned train/val/test data
├── notebooks/         ← EDA and experiments
├── src/               ← Python scripts
├── models/            ← trained model weights (ignored by Git)
├── outputs/           ← plots, predictions, demo results
├── .gitignore
├── requirements.txt
└── README.md
```
