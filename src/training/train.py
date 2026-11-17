from ultralytics import YOLO
import sys
from pathlib import Path

def main():
    
    EXPERIMENTS = {"baseline_yolo26n" : {"model" : "yolo26n.pt", "data" : "configs/kaggle_v1.yaml","epochs" : 50,
                                        "imgsz" : 640, "batch" : 16, "device" : 0, "seed" : 42, "project" : f"{Path.cwd()}/runs",
                                        "name" : "baseline_yolo26n"},

                    "yolo26s_640" : {"model" : "yolo26s.pt", "data" : "configs/kaggle_v1.yaml","epochs" : 50,
                                    "imgsz" : 640, "batch" : 16, "workers" : 4, "device" : 0, "seed" : 42, 
                                    "project" : f"{Path.cwd()}/runs", "name" : "yolo26s_640"}}

    experiment_model = sys.argv[0] #Get model as CLI parameter
    
    model = YOLO("yolo26s.pt") # Load YOLO26n pretrained model

    # Call the model’s train method and give it your settings as keyword arguments
    results = model.train(data="configs/kaggle_v1.yaml", 
                        epochs=50, 
                        imgsz=640,
                        batch = 16,
                        device = 0,
                        seed = 42,
                        project="runs",
                        name = "baseline_yolo26n")
    print("Training finished!")

if __name__ == "__main__":
    main()