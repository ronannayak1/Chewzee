import os
import shutil
import random
import pandas as pd

# config
seed = 42  # change for a different shuffle
num_samples = 500
source_dir = "/Users/ronannayak/Food/test-westwood-images-local/restaurant_images"
dest_dir = "/Users/ronannayak/Food/vlm_nutrition/usda_embeddings/restaurant_images"
csv_out = "/Users/ronannayak/Food/vlm_nutrition/usda_embeddings/arya_images_seed42.csv"

# make sure output directory exists
os.makedirs(dest_dir, exist_ok=True)

# set seed and load image list
random.seed(seed)
image_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# exclude already sampled files if applicable
if os.path.exists(csv_out):
    existing = pd.read_csv(csv_out)["filename"].tolist()
    image_files = [f for f in image_files if f not in existing]

# sample and copy
sampled_files = random.sample(image_files, min(num_samples, len(image_files)))

for file in sampled_files:
    shutil.copy(os.path.join(source_dir, file), os.path.join(dest_dir, file))

# csv log
df = pd.DataFrame({"filename": sampled_files})
df.to_csv(csv_out, index=False)

print(f"Copied {len(sampled_files)} images and saved to:\n{csv_out}")
