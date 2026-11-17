from ultralytics import YOLO
from pathlib import Path

MODELS = {"yolo26n": "runs/baseline_yolo26n/weights/best.pt",
          "yolo26s": "runs/yolo26s_640/weights/best.pt"}

if __name__ == "__main__":
    main()
