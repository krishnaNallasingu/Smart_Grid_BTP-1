import os
import rasterio
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

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
                
                # Create binary image: 255 (white) for value 13, 0 (black) for others
                binary = np.where(image_data == 13, 255, 0).astype(np.uint8)
                
                # Create PIL Image from numpy array
                img = Image.fromarray(binary)
                
                # Save as PNG
                img.save(output_path)
                print(f"Converted {filename} - Binary image with value 13 highlighted")

def get_global_min_max(input_folder):
    global_min = float('inf')
    global_max = float('-inf')
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.tif'):
            input_path = os.path.join(input_folder, filename)
            with rasterio.open(input_path) as src:
                image_data = src.read(1)
                global_min = min(global_min, np.nanmin(image_data))
                global_max = max(global_max, np.nanmax(image_data))
    
    return global_min, global_max

def convert_ntl_to_png(input_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Get global min and max values across all images
    global_min, global_max = get_global_min_max(input_folder)
    print(f"Global value range: {global_min} to {global_max}")
    
    # Create a colormap (yellow to bright white)
    colors = plt.cm.YlOrRd(np.linspace(0, 1, 256))
    colors = (colors[:, :3] * 255).astype(np.uint8)
    
    # Process each TIFF file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.tif'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace('.tif', '.png'))
            
            # Read TIFF file
            with rasterio.open(input_path) as src:
                image_data = src.read(1)
                
                # Normalize using global min-max
                normalized = np.clip((image_data - global_min) * 255.0 / (global_max - global_min), 0, 255)
                
                # Convert to uint8
                normalized = normalized.astype(np.uint8)
                
                # Apply colormap
                colored = colors[normalized]
                
                # Create PIL Image
                img = Image.fromarray(colored)
                
                # Save as PNG
                img.save(output_path)
                print(f"Converted {filename}")

# Create output directories
os.makedirs("../Png_Files/LULC", exist_ok=True)
os.makedirs("../Png_Files/NTL", exist_ok=True)

# Convert files
print("Converting LULC files...")
convert_lulc_to_png("../Tiff_files/LULC", "../Png_Files/LULC")
print("\nConverting NTL files...")
convert_ntl_to_png("../Tiff_files/NTL", "../Png_Files/NTL")