from ultralytics import YOLO
from pathlib import Path

MODELS = {"yolo26n": "runs/baseline_yolo26n/weights/best.pt",
          "yolo26s": "runs/yolo26s_640/weights/best.pt"}


def main():
    for model_name, weights in MODELS.items():
        print(f"\nTesting {model_name} ...")

        model = YOLO(weights) # load that trained model in runs folder
        model.val(data="configs/kaggle_v1.yaml",
                  split="test",               # use the 500 test images, not val
                  imgsz=640,
                  batch=16,
                  conf=0.25,
                  device=0,
                  project=str(Path.cwd() / "runs"),
                  name=f"test_{model_name}")  # ex - runs/test_yolo26n

    print("\nTesting finished!")
    
if __name__ == "__main__":
    main()
