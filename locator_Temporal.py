import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from geopy.distance import geodesic
from PIL import Image

# ========== PARAMETERS ==========
NUM_GRIDS = 15                         # Number of power grids to be placed
MIN_DISTANCE_KM = 50                   # Minimum distance between two grids (in km)
PERCENTILE = 90                        # Percentile for threshold
INPUT_FOLDER = "./comparision/Input"              # Folder containing yearly PNGs

# Coordinates of the image corners (top-left, bottom-left, bottom-right, top-right)
COORDINATES = [
    [-79.6104828125, 42.1057705066091],
    [-79.6104828125, 36.588415552450094],
    [-71.0850921875, 36.588415552450094],
    [-71.0850921875, 42.1057705066091]
]

lat_top = COORDINATES[0][1]
lat_bottom = COORDINATES[1][1]
lon_left = COORDINATES[0][0]
lon_right = COORDINATES[2][0]

def pixel_to_geo(x, y, width, height):
    lon = lon_left + (x / width) * (lon_right - lon_left)
    lat = lat_top - (y / height) * (lat_top - lat_bottom)
    return (lat, lon)

# ========== LOAD MULTIPLE IMAGES ==========
image_list = []
file_names = sorted([f for f in os.listdir(INPUT_FOLDER) if f.endswith(".png")])

for file in file_names:
    path = os.path.join(INPUT_FOLDER, file)
    img = Image.open(path).convert("L")
    image_array = np.array(img)
    image_list.append(image_array)

image_stack = np.stack(image_list, axis=0)  # Shape: (years, height, width)
height, width = image_stack.shape[1:]

# ========== AGGREGATE BRIGHTNESS ACROSS YEARS ==========
aggregated_image = np.mean(image_stack, axis=0)  # You can also try np.max or np.sum

# ========== HISTOGRAM ==========
plt.figure(figsize=(10, 5))
plt.hist(aggregated_image.flatten(), bins=256, range=(0, 255), color='gray', edgecolor='black')
plt.title('Aggregated Pixel Intensity Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# ========== THRESHOLDING ==========
INTENSITY_THRESHOLD = np.percentile(aggregated_image, PERCENTILE)
print(f"Using threshold from {PERCENTILE}th percentile: {INTENSITY_THRESHOLD:.2f}")

def get_bright_pixels(image_array, threshold):
    y_indices, x_indices = np.where(image_array >= threshold)
    coords = np.column_stack((x_indices, y_indices))
    return coords

bright_pixels = get_bright_pixels(aggregated_image, INTENSITY_THRESHOLD)
if bright_pixels.shape[0] < NUM_GRIDS:
    raise ValueError(f"Too few bright pixels ({bright_pixels.shape[0]}) found at threshold {INTENSITY_THRESHOLD:.2f}. Try a lower percentile.")

# ========== K-MEANS CLUSTERING ==========
kmeans = KMeans(n_clusters=NUM_GRIDS, random_state=42).fit(bright_pixels)
final_centers = kmeans.cluster_centers_

# ========== DISTANCE FILTERING ==========
filtered_centers = []
for center in final_centers:
    latlon = pixel_to_geo(center[0], center[1], width, height)
    too_close = False
    for existing in filtered_centers:
        dist = geodesic(latlon, existing).km
        if dist < MIN_DISTANCE_KM:
            too_close = True
            break
    if not too_close:
        filtered_centers.append(latlon)

# ========== VISUALIZATION ==========
plt.figure(figsize=(12, 8))
plt.imshow(aggregated_image, cmap='gray')
for lat, lon in filtered_centers:
    # Convert back to pixel for plotting
    x = int((lon - lon_left) / (lon_right - lon_left) * width)
    y = int((lat_top - lat) / (lat_top - lat_bottom) * height)
    plt.scatter(x, y, color='red', s=50, edgecolors='black')
plt.title("Suggested Power Grid Locations (Temporal Analysis)")
plt.axis('off')
plt.savefig("Suggested_Temporal_Power_Grids_Temporal.png", bbox_inches="tight")
plt.show()
