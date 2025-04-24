import os
import rasterio
import numpy as np
from PIL import Image

def convert_lulc_to_png(input_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Process each TIFF file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.tif'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace('.tif', '.png'))
            
            # Read TIFF file
            with rasterio.open(input_path) as src:
                # Read the single band data
                image_data = src.read(1)  # Read first band
                
                # Create a colored image based on LULC values (0-17)
                # Normalize to 0-255 range and create a gradient
                normalized = (image_data * (255 // 17)).astype(np.uint8)
                
                # Create PIL Image from numpy array
                img = Image.fromarray(normalized)
                
                # Save as PNG
                img.save(output_path)
                print(f"Converted {filename} - Value range: {image_data.min()} to {image_data.max()}")

def convert_ntl_to_png(input_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Process each TIFF file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.tif'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace('.tif', '.png'))
            
            # Read TIFF file
            with rasterio.open(input_path) as src:
                # Read the single band data
                image_data = src.read(1)
                
                # Normalize to 0-255 range
                normalized = ((image_data - image_data.min()) * 255.0 / 
                            (image_data.max() - image_data.min()))
                
                # Enhance brightness
                enhanced = np.clip(normalized * 2, 0, 255)  # Increased brightness multiplier
                
                # Create PIL Image
                img = Image.fromarray(enhanced.astype(np.uint8))
                
                # Save as PNG
                img.save(output_path)
                print(f"Converted {filename} - Value range: {image_data.min()} to {image_data.max()}")

# Create output directories
os.makedirs("../Png_Files/LULC", exist_ok=True)
os.makedirs("../Png_Files/NTL", exist_ok=True)

# Convert files
print("Converting LULC files...")
convert_lulc_to_png("../Tiff_files/LULC", "../Png_Files/LULC")
print("\nConverting NTL files...")
convert_ntl_to_png("../Tiff_files/NTL", "../Png_Files/NTL")