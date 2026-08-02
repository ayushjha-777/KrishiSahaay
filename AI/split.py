import os
import random
import shutil
from pathlib import Path

# Reproducible random split
random.seed(42)

# Dataset path (current structure)
SOURCE_DIR = Path("dataset")

# Output folders
TRAIN_DIR = SOURCE_DIR / "train"
VAL_DIR = SOURCE_DIR / "validation"
TEST_DIR = SOURCE_DIR / "test"

# Split ratio
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

# Remove old split folders if they already exist
for folder in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
    if folder.exists():
        shutil.rmtree(folder)

# Original classes
CLASSES = [
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Pest",
    "Bacteria",
]

for class_name in CLASSES:

    source = SOURCE_DIR / class_name

    images = [
        img for img in source.iterdir()
        if img.is_file()
    ]

    random.shuffle(images)

    total = len(images)

    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    train_imgs = images[:train_end]
    val_imgs = images[train_end:val_end]
    test_imgs = images[val_end:]

    for folder in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        (folder / class_name).mkdir(parents=True, exist_ok=True)

    for img in train_imgs:
        shutil.copy(img, TRAIN_DIR / class_name / img.name)

    for img in val_imgs:
        shutil.copy(img, VAL_DIR / class_name / img.name)

    for img in test_imgs:
        shutil.copy(img, TEST_DIR / class_name / img.name)

    print(f"{class_name}")
    print(f"Train: {len(train_imgs)}")
    print(f"Validation: {len(val_imgs)}")
    print(f"Test: {len(test_imgs)}")
    print("-" * 30)

print("Dataset split completed successfully.")