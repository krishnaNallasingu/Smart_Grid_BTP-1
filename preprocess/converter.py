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
                # Read all bands
                image_data = src.read()
                
                # Create binary image (black and white)
                binary_image = np.zeros_like(image_data[0])
                
                # Set pixels where band 13 has data to white (255)
                # Note: bands are 0-indexed in the array
                binary_image[image_data[12] > 0] = 255
                
                # Create PIL Image from numpy array
                img = Image.fromarray(binary_image.astype(np.uint8))
                
                # Save as PNG
                img.save(output_path)

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
                # Read the data
                image_data = src.read(1)  # Read first band
                
                # Normalize and enhance brightness
                # Scale to 0-255 range
                image_data = ((image_data - image_data.min()) * 255.0 / 
                            (image_data.max() - image_data.min()))
                
                # Enhance brightness by increasing values
                enhanced_data = np.clip(image_data * 1.5, 0, 255)
                
                # Create PIL Image
                img = Image.fromarray(enhanced_data.astype(np.uint8))
                
                # Save as PNG
                img.save(output_path)

# Create output directories
os.makedirs("./Png_Files/LULC", exist_ok=True)
os.makedirs("./Png_Files/NTL", exist_ok=True)

# Convert files
convert_lulc_to_png("./Tiff_files/LULC", "./Png_Files/LULC")
convert_ntl_to_png("./Tiff_files/NTL", "./Png_Files/NTL")