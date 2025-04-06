# yolo_dataset_builder/prepare_yolo_dataset.py
import os
import cv2
import shutil
import random
from glob import glob

VISIBLE_DIR = "datasets/visible"
INVISIBLE_DIR = "datasets/invisible"
YOLO_DIR = "datasets/yolo"
CLASS_ID = 0
SPLIT_RATIO = 0.8  # 80% train, 20% val

IMAGES_DIR = f"{YOLO_DIR}/images"
LABELS_DIR = f"{YOLO_DIR}/labels"

for subdir in [IMAGES_DIR, LABELS_DIR]:
    for split in ["train", "val"]:
        os.makedirs(f"{subdir}/{split}", exist_ok=True)

temp_visible = []
temp_invisible = []

def convert_and_label(image_path, label_visible):
    img = cv2.imread(image_path)
    if img is None:
        return None

    height, width = img.shape[:2]
    if width == 0 or height == 0:
        print(f"⚠️ PUSTY OBRAZ: {image_path}")
        return None

    base_name = os.path.splitext(os.path.basename(image_path))[0]

    img_out = f"{YOLO_DIR}/images/{base_name}.jpg"
    label_out = f"{YOLO_DIR}/labels/{base_name}.txt"

    cv2.imwrite(img_out, img)

    if label_visible:
        with open(label_out, "w") as f:
            f.write(f"{CLASS_ID} 0.5 0.5 1.0 1.0\n")
        temp_visible.append(img_out)
    else:
        open(label_out, "w").close()
        temp_invisible.append(img_out)

    return base_name

def split_dataset():
    global temp_visible, temp_invisible
    all_images = temp_visible + temp_invisible
    random.shuffle(all_images)

    split_v = int(len(temp_visible) * SPLIT_RATIO)
    split_i = int(len(temp_invisible) * SPLIT_RATIO)

    train_images = temp_visible[:split_v] + temp_invisible[:split_i]
    val_images = temp_visible[split_v:] + temp_invisible[split_i:]

    if val_images == [] and temp_visible:
        moved = temp_visible[0]
        if moved in train_images:
            train_images.remove(moved)
        val_images.append(moved)

    for img_path in train_images:
        base = os.path.basename(img_path)
        if not os.path.exists(img_path):
            continue
        try:
            shutil.move(img_path, f"{IMAGES_DIR}/train/{base}")
            shutil.move(img_path.replace("images", "labels").replace(".jpg", ".txt"),
                        f"{LABELS_DIR}/train/{base.replace('.jpg', '.txt')}")
        except FileNotFoundError:
            continue

    for img_path in val_images:
        base = os.path.basename(img_path)
        if not os.path.exists(img_path):
            continue
        try:
            shutil.move(img_path, f"{IMAGES_DIR}/val/{base}")
            shutil.move(img_path.replace("images", "labels").replace(".jpg", ".txt"),
                        f"{LABELS_DIR}/val/{base.replace('.jpg', '.txt')}")
        except FileNotFoundError:
            continue

def prepare():
    for f in glob(f"{YOLO_DIR}/images/*.jpg") + glob(f"{YOLO_DIR}/labels/*.txt"):
        os.remove(f)

    for img_path in glob(f"{VISIBLE_DIR}/*.png"):
        convert_and_label(img_path, label_visible=True)
    for img_path in glob(f"{INVISIBLE_DIR}/*.png"):
        convert_and_label(img_path, label_visible=False)

    split_dataset()
    print(f"✅ Dataset gotowy do trenowania YOLO \nVisible: {len(temp_visible)}, Invisible: {len(temp_invisible)}")

if __name__ == "__main__":
    prepare()
