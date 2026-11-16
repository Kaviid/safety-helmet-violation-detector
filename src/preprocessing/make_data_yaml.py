from pathlib import Path

# full path to the split dataset, on whatever computer runs this
dataset_path = (Path.cwd() / "data/processed/kaggle_split").as_posix()

# create 'configs' folder
config_dir = Path.cwd() / "configs"
config_dir.mkdir(parents=True, exist_ok=True)

# yaml content 
text = f"""path: {dataset_path}
train: images/train
val: images/val
test: images/test

names:
  0: helmet
  1: no_helmet
"""

(config_dir / "kaggle_v1.yaml").write_text(text)
print(f"Created: {config_dir / 'kaggle_v1.yaml'}")