from sklearn.model_selection import train_test_split
import os
import shutil

# Define your data directory
data_dir = r'C:\Users\adirn\Desktop\fy project fish\train'  # Original data directory
train_dir = r'C:\Users\adirn\Desktop\fy project fish\train_split'  # Directory for training data
val_dir = r'C:\Users\adirn\Desktop\fy project fish\val_split'      # Directory for validation data

# Create folders if they don't exist
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# Split the images
for category in ['fresh', 'not_fresh']:
    category_dir = os.path.join(data_dir, category)
    print(f"Looking for images in {category_dir}...")  # Debugging line

    # Check if the directory exists
    if not os.path.exists(category_dir):
        print(f"Directory not found: {category_dir}")
        continue

    images = os.listdir(category_dir)
    print(f"Found {len(images)} images in {category} category.")  # Debugging line

    # Check if there are any images
    if len(images) == 0:
        print(f"No images found in {category_dir}. Please add images.")
        continue

    train_images, val_images = train_test_split(images, test_size=0.2, random_state=42)

    os.makedirs(os.path.join(train_dir, category), exist_ok=True)
    os.makedirs(os.path.join(val_dir, category), exist_ok=True)

    # Move images to train and val folders
    for img in train_images:
        shutil.copy(os.path.join(category_dir, img), os.path.join(train_dir, category))
    for img in val_images:
        shutil.copy(os.path.join(category_dir, img), os.path.join(val_dir, category))

print("Data split complete. Check your train_split and val_split folders.")
