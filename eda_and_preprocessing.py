import torch.nn as nn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

from pathlib import Path

from PIL import Image
import os

from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision.models import resnet18, ResNet18_Weights

from collections import Counter
import hashlib

def file_hash(path):

    with open(path, "rb") as f:
        return hashlib.md5(
            f.read()
        ).hexdigest()

def collect_image_hashes(root_folder, dataset_name):
    records = []

    for path in Path(root_folder).rglob("*"):
        if path.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:

            records.append({
                "dataset": dataset_name,
                "class": path.parent.name,
                "filename": path.name,
                "path": str(path),
                "hash": file_hash(path)
            })

    return records

weights = ResNet18_Weights.DEFAULT
transform = weights.transforms()

train_dataset = ImageFolder("images/training", transform=transform)
test_dataset = ImageFolder("images/testing", transform=transform)

train_records = collect_image_hashes(
    "images/training",
    "training"
)

test_records = collect_image_hashes(
    "images/testing",
    "testing"
)

hash_df = pd.DataFrame(train_records + test_records)

train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True
)

test_loader = DataLoader(
    test_dataset,
    batch_size=32,
    shuffle=False
)

print(Counter(train_dataset.targets))
print(train_dataset.class_to_idx)
# It is, largely, equally balanced with flip and notflip images (1162:1230)

records = []

for cls in ["flip", "notflip"]:
    folder = f"images/training/{cls}"

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)

        try:
            img = Image.open(path)

            records.append({"class": cls,
                "filename": filename,
                "width": img.width,
                "height": img.height,
                "mode": img.mode})

        except Exception:
            print("Could not open:", path)

df = pd.DataFrame(records)

# Both width and height have a standard deviation of 0 for flip and notflip, so
# it is consistent throughout. 

print(df.head())

print(df[["width", "height"]].describe())
print(df.groupby("class")[["width", "height"]].describe())

df["aspect_ratio"] = df["width"] / df["height"]

print(df.groupby("class")["aspect_ratio"].describe())

print(df["mode"].value_counts())

fig, axes = plt.subplots(2, 5, figsize=(15, 6))

for row, cls in enumerate(["flip", "notflip"]):

    folder = f"images/training/{cls}"
    files = random.sample(os.listdir(folder), 5)

    for col, filename in enumerate(files):

        img = Image.open(
            os.path.join(folder, filename)
        ).convert("RGB")

        axes[row, col].imshow(img)
        axes[row, col].set_title(cls)
        axes[row, col].axis("off")

plt.tight_layout()
plt.show()

# After running several times, the images are very similar in set up.

duplicates = hash_df[
    hash_df.duplicated("hash", keep=False)
].sort_values("hash")

print("These are the duplicates", duplicates)
# There are no duplicates.


train_hashes = set(
    hash_df.loc[
        hash_df["dataset"] == "training",
        "hash"
    ]
)

test_hashes = set(
    hash_df.loc[
        hash_df["dataset"] == "testing",
        "hash"
    ]
)

overlap = train_hashes.intersection(test_hashes)

print("Number of exact duplicates between train and test:", len(overlap))


train_test_duplicates = hash_df[
    hash_df["hash"].isin(overlap)
].sort_values("hash")

print(train_test_duplicates[
    ["dataset", "class", "filename", "path", "hash"]
])



### Model building