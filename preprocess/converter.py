import os
import rasterio
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from rasterio.features import geometry_mask
from rasterio.mask import mask
from shapely.geometry import box, mapping

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
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith('.tif'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace('.tif', '.png'))

            with rasterio.open(input_path) as src:
                data = src.read(1)
                mask_data = data != src.nodata if src.nodata is not None else ~np.isnan(data)

                # Get bounding box of valid data
                rows, cols = np.where(mask_data)
                if len(rows) == 0 or len(cols) == 0:
                    print(f"Skipping empty: {filename}")
                    continue

                min_row, max_row = rows.min(), rows.max()
                min_col, max_col = cols.min(), cols.max()

                # Crop to valid data
                cropped = data[min_row:max_row+1, min_col:max_col+1]
                cropped_mask = mask_data[min_row:max_row+1, min_col:max_col+1]

                # Normalize the valid data
                valid_pixels = cropped[cropped_mask]
                min_value = valid_pixels.min()
                max_value = valid_pixels.max()

                if max_value > min_value:
                    norm = (cropped - min_value) / (max_value - min_value)
                    norm[~cropped_mask] = 0  # Set background to black
                    norm = (norm * 255).astype(np.uint8)
                else:
                    norm = np.full_like(cropped, 0, dtype=np.uint8)

                img = Image.fromarray(norm, mode='L')
                img.save(output_path)
                print(f"Converted and saved: {filename}")


# Create output directories
# os.makedirs("../Real_World/Png_Files/GHSL_01", exist_ok=True)
# os.makedirs("../Png_Files/NTL", exist_ok=True)

# Convert files
# print("Converting LULC files...")
# convert_lulc_to_png("../Tiff_files/LULC", "../Png_Files/LULC")
# print("\nConverting NTL files...")
# convert_ntl_to_png("../Tiff_files/NTL", "../Png_Files/NTL")

# print("Converting GHSL files...")
# convert_ghsl_to_png("../Real_World/Data/GHSL_01_Washington", "../Real_World/Png_Files/GHSL_01")

convert_ntl_to_png("../Batch_Loads/Tiff/NTL_03_Delhi", "../Batch_Loads/Png/NTL_03")