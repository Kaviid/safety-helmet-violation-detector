from pathlib import Path
import random
import cv2

# make output folders (exist_ok=True : means no error if they already exist. because sometime can file doesn't exist.)
Path("outputs/verify").mkdir(parents=True, exist_ok=True)

files = []

for f in Path("data/processed/kaggle_split/labels/train").rglob("*.txt"):
    files.append(f) # we store full path

ten_files = random.sample(files, 10)
COLOURS = {"0": (0, 255, 0), "1": (0, 0, 255)}    
NAMES   = {"0": "helmet",    "1": "no_helmet"}

for label_path in ten_files:
    # find the matching image: .../annotations/x.txt -> .../images/x.jpg
    img_path = Path("data/processed/kaggle_split/images/train") / (label_path.stem + ".png")
    img = cv2.imread(str(img_path))
    if img is None:
        print("Image not found:", img_path)
        continue

    h, w = img.shape[:2]

    for line in label_path.read_text().splitlines():
        if not line.strip():
            continue

        parts = line.split()
        class_id = parts[0]
        xc = float(parts[1])
        yc = float(parts[2])
        bw = float(parts[3])
        bh = float(parts[4])

        # YOLO (0-1, centre) -> pixel corners
        x1 = int((xc - bw / 2) * w)
        y1 = int((yc - bh / 2) * h)
        x2 = int((xc + bw / 2) * w)
        y2 = int((yc + bh / 2) * h)

        colour = COLOURS[class_id]
        cv2.rectangle(img, (x1, y1), (x2, y2), colour, 1)
        cv2.putText(img, NAMES[class_id], (x1, y1 - 3),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, colour, 1)
        
    cv2.imwrite(str(Path("outputs/verify") / img_path.name), img)

print("Verify boxes draw done!")