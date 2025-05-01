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
    min_value = 0
    max_value = 63  # Common max value for NTL data
    
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
                
                # Normalize to 0-255 range for grayscale
                grayscale = ((image_data - min_value) / (max_value - min_value) * 255).astype(np.uint8)
                
                # Enhance brightness
                brightness_factor = 1.5  # Adjust this value to increase/decrease brightness
                enhanced = np.clip(grayscale * brightness_factor, 0, 255).astype(np.uint8)
                
                # Create PIL Image (mode='L' for grayscale)
                img = Image.fromarray(enhanced, mode='L')
                
                # Save as PNG
                img.save(output_path)
                print(f"Converted {filename} - Grayscale image with enhanced brightness")

def convert_ghsl_to_png(input_folder, output_folder):
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
                image_data = src.read(1).astype(np.float32)  # Read as float for normalization

                # Find the minimum and maximum values in the image data
                min_value = np.nanmin(image_data)
                max_value = np.nanmax(image_data)

                # Normalize the data to the 0-255 range
                if max_value > min_value:
                    normalized_data = ((image_data - min_value) / (max_value - min_value) * 255).astype(np.uint8)
                else:
                    # If all values are the same, create a uniform image
                    normalized_data = np.full_like(image_data, 0, dtypenp.uint8)

                # Enhance contrast (optional - adjust factor as needed)
                contrast_factor = 1.2
                enhanced_data = np.clip((normalized_data - 127.5) * contrast_factor + 127.5, 0, 255).astype(np.uint8)

                # Create PIL Image (mode='L' for grayscale)
                img = Image.fromarray(enhanced_data, mode='L')

                # Save as PNG
                img.save(output_path)
                print(f"Converted {filename} - Normalized and enhanced grayscale image")


# Create output directories
os.makedirs("../Real_World/Png_Files/GHSL_02", exist_ok=True)
# os.makedirs("../Png_Files/NTL", exist_ok=True)

# Convert files
# print("Converting LULC files...")
# convert_lulc_to_png("../Tiff_files/LULC", "../Png_Files/LULC")
# print("\nConverting NTL files...")
# convert_ntl_to_png("../Tiff_files/NTL", "../Png_Files/NTL")

print("Converting GHSL files...")
convert_ghsl_to_png("../Real_World/Data/GHSL_02_Nashvillie", "../Real_World/Png_Files/GHSL_02")