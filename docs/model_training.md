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