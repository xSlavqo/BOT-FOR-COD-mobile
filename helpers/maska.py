# utils/helpers/static_mask_builder.py
import cv2
import numpy as np
import os
import random

def extract_static_elements(output_name="masked_output.png"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "screens")

    files = sorted([
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.endswith(".png")
    ])

    if len(files) < 2:
        print("❌ Potrzeba co najmniej 2 obrazów w folderze 'screens'.")
        return

    imgs = [cv2.imread(f) for f in files]
    base_shape = imgs[0].shape

    if any(img.shape != base_shape for img in imgs):
        print("❌ Wszystkie obrazy muszą mieć ten sam rozmiar.")
        return

    static_mask = np.ones_like(imgs[0], dtype=bool)
    for img in imgs[1:]:
        static_mask &= (img == imgs[0])

    base = random.choice(imgs)
    output = np.zeros((base.shape[0], base.shape[1], 4), dtype=np.uint8)

    output[..., :3] = base
    output[..., 3] = np.where(static_mask[..., 0], 255, 0)

    out_path = os.path.join(current_dir, output_name)
    cv2.imwrite(out_path, output)
    print(f"✅ Zapisano maskowany obraz jako {out_path}")

if __name__ == "__main__":
    extract_static_elements()
