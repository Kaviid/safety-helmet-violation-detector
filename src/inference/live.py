from ultralytics import YOLO
from pathlib import Path
import sys
import time
import cv2

MODEL_PATH = "models/helmet_v1_yolo26s.pt"

CONF = 0.25  # model only shows a box if it’s at least 25% sure


def main():
    #source - "0" = webcam, or a video path like data/videos/test/site1.mp4
    #print(len(sys.argv))
    if len(sys.argv) < 2 or len(sys.argv) > 2: #Issue
        print("Usage: python src/inference/live.py <0 for webcam | video path>")
        sys.exit(1)

    source = sys.argv[1]
    if source.isdigit():
        source = int(source)
    elif not Path(source).exists(): #For video path...
        print(f"Video not found: {source}")
        sys.exit(1)

    model = YOLO(MODEL_PATH)
    cap = cv2.VideoCapture(source)
    video_fps = cap.get(cv2.CAP_PROP_FPS) or 30 #the video's real speed 
    delay = int(1000 / video_fps) #if vid has 30 frames per second, one frame take atleast 1,000 ÷ 30 = 33 ms
    if not cap.isOpened():
        print("Could not open the camera or video.")
        sys.exit(1)

    while True:
        ok, frame = cap.read() # read one frame and Ok store True or False - False mean end of video
        if not ok:                        
            break

        start = time.time()
        results = model.predict(frame, conf=CONF, verbose=True) #Model check one frame
        fps = 1 / (time.time() - start)

        result = results[0]
        drawn = result.plot() #Give a copy of frame with box drawed

        # TODO : count each class in this frame
        helmet = 0
        no_helmet = 0
        for cls in result.boxes.cls.tolist():
            if int(cls) == 0:
                helmet += 1
            else:
                no_helmet += 1

        #info txt
        cv2.putText(drawn, f"FPS: {fps:.0f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(drawn, f"Helmet: {helmet}  No helmet: {no_helmet}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        #red warning for no helmet
        if no_helmet > 0:
            cv2.putText(drawn, "WARNING: NO HELMET!", (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

        cv2.imshow("Safety Helmet Detector (press q to quit)", drawn)
        if cv2.waitKey(delay) & 0xFF == ord("q"):  # press q to stop
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()