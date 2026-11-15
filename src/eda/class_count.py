from pathlib import Path

count1 = 0
count2 = 0

for f in Path("data/raw/IITU_Safety-Helmet_Dataset").rglob("*.jpg"):
    count1 += 1

for f in Path("data/raw/kaggle_hardhat").rglob("*.png"):
    count2 += 1

print(f"IITU Dataset : {count1}") #Top view dataset
print(f"Kaggle Dataset : {count2}") #Kaggle dataset