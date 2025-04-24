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

def convert_ntl_to_png(input_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Define a fixed range for normalization (based on typical NTL values)
    # These values can be adjusted based on your specific needs
    min_value = 0
    max_value = 63  # Common max value for NTL data
    
    # Create colormap
    colormap = plt.cm.viridis  # Using viridis colormap which is perceptually uniform
    
    # Process each TIFF file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.tif'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace('.tif', '.png'))
            
            # Read TIFF file
            with rasterio.open(input_path) as src:
                # Read the single band data
                image_data = src.read(1)
                
                # Clip values to our fixed range
                image_data = np.clip(image_data, min_value, max_value)
                
                # Normalize to 0-1 range using fixed min/max values
                normalized = (image_data - min_value) / (max_value - min_value)
                
                # Apply colormap
                colored = (colormap(normalized) * 255).astype(np.uint8)
                
                # Extract RGB channels (removing alpha channel)
                rgb_image = colored[:, :, :3]
                
                # Enhance brightness
                brightness_factor = 1.5  # Adjust this value to increase/decrease brightness
                enhanced = np.clip(rgb_image * brightness_factor, 0, 255).astype(np.uint8)
                
                # Create PIL Image
                img = Image.fromarray(enhanced)
                
                # Save as PNG
                img.save(output_path)
                print(f"Converted {filename} - Using consistent colormap with enhanced brightness")

# Create output directories
os.makedirs("../Png_Files/LULC", exist_ok=True)
os.makedirs("../Png_Files/NTL", exist_ok=True)

# Convert files
print("Converting LULC files...")
convert_lulc_to_png("../Tiff_files/LULC", "../Png_Files/LULC")
print("\nConverting NTL files...")
convert_ntl_to_png("../Tiff_files/NTL", "../Png_Files/NTL")