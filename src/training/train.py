from ultralytics import YOLO

EXPERIMENTS = {"baseline_yolo26n" : {"model" : "yolo26s.pt", "data" : "configs/kaggle_v1.yaml","epochs" : 50,
                                     "imgsz" : 640, "batch" : 16, "device" : 0, "seed" : 42, "project" : "runs",
                                     "name" : "baseline_yolo26n"}}

def main():
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