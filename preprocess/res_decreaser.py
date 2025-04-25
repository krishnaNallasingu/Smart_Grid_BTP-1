import os
from PIL import Image

# Input and output folder paths
input_folder = '../Batch_Loads/Png/NTL_02'
output_folder = '../Batch_Loads/Low_Png/NTL_02'
os.makedirs(output_folder, exist_ok=True)

# Resize factor
scale_factor = 0.5

# Loop through all PNG files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith('.png'):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        # Open image
        with Image.open(input_path) as img:
            # Calculate new size
            new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
            # Resize image using high-quality resampling
            resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
            # Save resized image
            resized_img.save(output_path)

print("All images resized and saved to:", output_folder)