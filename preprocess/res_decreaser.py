import os
from PIL import Image

# Input and output folder paths
input_folder = '../Batch_Loads/Png/NTL_03'
output_folder = '../Batch_Loads/Low_Png/NTL_03'
os.makedirs(output_folder, exist_ok=True)

# Target resolution
target_size = (317, 229)

# Loop through all image files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        # Open and resize the image
        with Image.open(input_path) as img:
            resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
            resized_img.save(output_path)

print("All images resized to", target_size, "and saved to:", output_folder)
