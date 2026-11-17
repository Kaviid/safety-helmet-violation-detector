# Training

## What happens during training?
For each batch of images:

1. **Forward pass:** The model looks at an image and makes its guess.
   - Example: "There's a head at (100, 50), and I think it's a helmet."
   - It's called "forward" because the image goes forward through the layers, from input to output.

2. **Loss:** The model's guess is compared with the actual answer (the label).
   - The loss is one number that says how wrong the guess was.
   - Box a bit off + wrong class → big loss
   - Box almost perfect + right class → small loss
   - **The goal of training is to make the loss as small as possible.**

3. **Backpropagation:** Find out what caused the mistake.
   - The model has millions of weights (filter numbers). Which ones caused the wrong answer?
   - Backpropagation goes backwards through the layers (output → input) and works out, for each weight: "If I change you a little, does the loss go up or down, and by how much?"
   - This "which direction + how much" for each weight is called its **gradient**.

4. **Gradient descent:** Change each weight a tiny bit in the direction that lowers the loss.
   - The **learning rate** controls how big each step is. Too big → it jumps around. Too small → training is very slow.

*Repeat thousands of times → the predictions get better.*

## Training settings (baseline)

| Setting | Meaning | My value | Why |
|---|---|---|---|
| epochs | How many times the model sees the whole training set | 50 | Enough for a first result (default is 100) |
| imgsz | Image size used in training | 640 | Decided in model selection |
| batch | Number of images processed together before one weight update | 16 | Fits in 6 GB with a nano model |
| data | Path to the dataset config | `configs/kaggle_v1.yaml` | Tells YOLO where the data is |
| device | Where to train | 0 (GPU) | Much faster than CPU |
| seed | Fixes randomness | 42 | Makes results reproducible |
| project / name | Where results are saved | `runs` / `baseline_yolo26n` | Gives each experiment a clear name |

- 3,500 train images ÷ batch 16 ≈ 219 weight updates per epoch.
- 219 × 50 epochs ≈ 11,000 updates in total.
- Learning rate and augmentation stay at YOLO's defaults for the baseline. I will tune them later.

## Baseline results (YOLO26n, 50 epochs, 640)
Run: `python src/training/train.py baseline_yolo26n`
Results folder: `runs/baseline_yolo26n`

| Class | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| all | 0.923 | 0.922 | 0.953 | 0.632 |
| helmet | 0.941 | 0.928 | 0.965 | 0.639 |
| no_helmet | 0.905 | 0.917 | 0.941 | 0.625 |

- Training time: about 40 minutes on RTX 4050 6GB.
- GPU memory: about 2.5 GB at batch 16.
- Model size: 5.5 MB.
- Inference time: 2.1 ms per image, far above the 15 FPS target.
- Train and val losses both go down until the last epoch, so the model is not overfitting.
- mAP50 stops improving after about epoch 30. mAP50-95 is still rising slightly, so more epochs may help a little.
- Confusion matrix: 98% of helmets and 97% of no_helmet heads are found correctly.
- Most dangerous error: 2% of no_helmet heads are predicted as helmet, and 2% are not found.
- Some false alarms on the background (73% of them predicted as helmet, 27% as no_helmet). Possible causes: unlabelled heads, mirrored image edges, or very low-confidence boxes. To check with a confidence threshold in evaluation.

## YOLO26s results (50 epochs, 640)
Run: `python src/training/train.py yolo26s_640`
Results folder: `runs/yolo26s_640`

| Class | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| all | 0.928 | 0.929 | 0.960 | 0.641 |
| helmet | 0.942 | 0.942 | 0.972 | 0.650 |
| no_helmet | 0.914 | 0.916 | 0.948 | 0.633 |

- Training time: about 58 minutes on RTX 4050 6GB.
- GPU memory: about 5.0 GB at batch 16, close to the 6 GB limit.
- Model size: 20.3 MB (4 times bigger than YOLO26n).
- Inference time: 4.2 ms per image (2 times slower than YOLO26n, but still far above 15 FPS).
- Train and val losses both go down until the last epoch, so the model is not overfitting.
- mAP50 stops improving after about epoch 40. mAP50-95 is still rising slightly.
- Confusion matrix: 98.1% of helmets (3,628 of 3,697) and 97.0% of no_helmet heads (1,115 of 1,150) are found correctly.
- Most dangerous error: 20 no_helmet heads (1.7%) are predicted as helmet, and 15 are not found. In total, 35 of 1,150 unsafe workers are missed (3%).
- The background counts are high (6,710 helmet, 2,491 no_helmet), but these include very low-confidence boxes. Precision of 0.928 shows that real false alarms are much lower. To check with a confidence threshold in evaluation.
- Compared with the baseline, YOLO26s is slightly better on most scores (under 1 point).
- no_helmet recall is the same as the baseline (0.916 vs 0.917).
- A bigger model did not help much. More no_helmet data (especially top-view) is likely a better improvement.