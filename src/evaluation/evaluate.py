from ultralytics import YOLO
from pathlib import Path

MODELS = {"yolo26n": "runs/baseline_yolo26n/weights/best.pt",
          "yolo26s": "runs/yolo26s_640/weights/best.pt"}


def main():
    for model_name, weights in MODELS.items():
        print(f"\nTesting {model_name} ...")

        model = YOLO(weights) # load that trained model in runs folder

    
if __name__ == "__main__":
    main()
