## Train / Val / Test Split
Run : `python src/preprocessing/split_dataset.py`

- Random split with seed 42 (70 / 20 / 10).

| Split | Images | helmet | no_helmet | Ratio |
|---|---|---|---|---|
| train | 3,500 | 13,406 | 4,051 | 3.31 |
| val | 1,000 | 3,697 | 1,150 | 3.21 |
| test | 500 | 1,828 | 580 | 3.15 |

- All splits have a similar helmet : no_helmet ratio, so the split is balanced.