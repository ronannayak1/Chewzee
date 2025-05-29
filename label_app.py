import streamlit as st
import os
from PIL import Image
import json
import pandas as pd
import random

# path -- update to local image path
image_folder = "/Users/ronannayak/Food/test-westwood-images-local/restaurant_images"
label_file = "image_labels.json"
csv_file = "image_labels.csv"
flattened_csv_file = "flattened_labels.csv"

# load images in order
#image_paths = sorted([
 #   os.path.join(image_folder, fname)
  #  for fname in os.listdir(image_folder)
   # if fname.lower().endswith(('.jpg', '.jpeg', '.png'))
#])
# load random images
image_paths = sorted([
    os.path.join(image_folder, fname)
    for fname in os.listdir(image_folder)
    if fname.lower().endswith(('.jpg', '.jpeg', '.png'))
])
random.seed(42)
random.shuffle(image_paths)

# load existing labels if available
if os.path.exists(label_file):
    with open(label_file, "r") as f:
        labels = json.load(f)
else:
    labels = {}

# define labeling categories
cuisines = [
    "asian", "thai", "mexican", "italian", "japanese", "korean", "chinese",
    "american", "indian", "mediterranean", "middle eastern", "other"
]

dish_types = [
    "noodle", "soup", "rice dish", "sandwich", "salad", "burger", "pizza", "pasta",
    "seafood", "meat", "sushi", "dessert", "appetizer", "drink", "vegetarian", "side", "bowl", "baked good"
]

attributes = [
    "spicy", "sweet", "sour", "savory", "creamy", "crispy",
    "healthy", "high protein", "low carb", "vegan", "gluten free",
    "comfort food", "refreshing", "light meal", "hearty", "small dish", "to share"
]

# track current index
if "index" not in st.session_state:
    st.session_state.index = 0

# get unlabeled images
relative_image_paths = [os.path.relpath(p, image_folder) for p in image_paths]
unlabeled = [p for p in relative_image_paths if p not in labels]

if not unlabeled:
    st.success("All images labeled!")
    st.stop()

# ensure index is within bounds
st.session_state.index = max(0, min(st.session_state.index, len(unlabeled) - 1))

# show current image
relative_path = unlabeled[st.session_state.index]
img_path = os.path.join(image_folder, relative_path)
st.image(Image.open(img_path), caption=relative_path, use_column_width=True)

# inputs for labels
selected_cuisines = st.multiselect("Select cuisine(s):", cuisines)
selected_dish_types = st.multiselect("Select dish type(s):", dish_types)
selected_attrs = st.multiselect("Select attributes:", attributes)

def save_all_labels():
    # save wide-format CSV
    wide_rows = []
    for path, data in labels.items():
        wide_rows.append({
            "image_path": path,
            "cuisine": ", ".join(data.get("cuisine", [])),
            "dish_type": ", ".join(data.get("dish_type", [])),
            "attributes": ", ".join(data.get("attributes", []))
        })
    pd.DataFrame(wide_rows).to_csv(csv_file, index=False)

    # save flattened CSV
    flat_rows = []
    for path, data in labels.items():
        for cat in data.get("cuisine", []):
            flat_rows.append({"image_path": path, "tag_type": "cuisine", "tag": cat})
        for cat in data.get("dish_type", []):
            flat_rows.append({"image_path": path, "tag_type": "dish_type", "tag": cat})
        for cat in data.get("attributes", []):
            flat_rows.append({"image_path": path, "tag_type": "attributes", "tag": cat})
    pd.DataFrame(flat_rows).to_csv(flattened_csv_file, index=False)

if st.button("Save label"):
    labels[relative_path] = {
        "cuisine": selected_cuisines,
        "dish_type": selected_dish_types,
        "attributes": selected_attrs
    }
    with open(label_file, "w") as f:
        json.dump(labels, f, indent=2)
    save_all_labels()
    st.session_state.index += 1
    st.rerun()

if st.button("Skip"):
    labels[relative_path] = {
        "cuisine": [],
        "dish_type": [],
        "attributes": []
    }
    with open(label_file, "w") as f:
        json.dump(labels, f, indent=2)
    save_all_labels()
    st.session_state.index += 1
    st.rerun()

if st.button("Go Back"):
    st.session_state.index = max(0, st.session_state.index - 1)
    st.rerun()