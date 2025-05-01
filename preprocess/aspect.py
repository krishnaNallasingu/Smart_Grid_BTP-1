# 243/155

import os
from PIL import Image

def crop_to_aspect(image, target_ratio):
    width, height = image.size
    current_ratio = width / height

    if current_ratio > target_ratio:
        # Image is too wide, crop width
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        right = left + new_width
        top = 0
        bottom = height
    else:
        # Image is too tall, crop height
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        bottom = top + new_height
        left = 0
        right = width

    return image.crop((left, top, right, bottom))

def batch_crop_images(folder_path, output_folder, aspect_width, aspect_height):
    target_ratio = aspect_width / aspect_height

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.png'):
            image_path = os.path.join(folder_path, filename)
            with Image.open(image_path) as img:
                cropped = crop_to_aspect(img, target_ratio)
                output_path = os.path.join(output_folder, filename)
                cropped.save(output_path)
                print(f"Cropped and saved: {output_path}")

# Example usage
input_folder = '../Real_World/Png_Files/GHSL_01'          # replace with your folder
output_folder = '../Real_World/Croped_Pngs/GHSL_01'
aspect_width = 243
aspect_height = 155

batch_crop_images(input_folder, output_folder, aspect_width, aspect_height)
