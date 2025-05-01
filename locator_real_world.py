import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from geopy.distance import geodesic
from PIL import Image

# ========== PARAMETERS ==========
NUM_GRIDS = 15                         # Number of power grids to be placed
MIN_DISTANCE_KM = 50                   # Minimum distance between two grids (in km)
INTENSITY_THRESHOLD = 20              # Brightness threshold to select pixels
# IMAGE_PATH = "./Real_World/Png_Files/GHSL_01/GHSL_2020.png"
# IMAGE_PATH = "./Batch_Loads/Png/NTL_02/NTL_2022.png"
IMAGE_PATH = "./Real_World/Croped_Pngs/GHSL_01/GHSL_2015_destretched.png"


# Coordinates of the image corners (top-left, bottom-left, bottom-right, top-right)
COORDINATES = [
    [-79.6104828125, 42.1057705066091],
    [-79.6104828125, 36.588415552450094],
    [-71.0850921875, 36.588415552450094],
    [-71.0850921875, 42.1057705066091]
]

# ========== GEO MAPPING ==========
lat_top = COORDINATES[0][1]
lat_bottom = COORDINATES[1][1]
lon_left = COORDINATES[0][0]
lon_right = COORDINATES[2][0]

def pixel_to_geo(x, y, width, height):
    lon = lon_left + (x / width) * (lon_right - lon_left)
    lat = lat_top - (y / height) * (lat_top - lat_bottom)
    return (lat, lon)

# ========== IMAGE LOADING ==========
image = Image.open(IMAGE_PATH).convert("L")  # Grayscale
image_array = np.array(image)
height, width = image_array.shape

# ========== PROCESSING ==========

# ========== PROCESSING ==========

# Step 1: Plot histogram to choose good percentile threshold
plt.figure(figsize=(10, 5))
plt.hist(image_array.flatten(), bins=256, range=(0, 255), color='gray', edgecolor='black')
plt.title('Pixel Intensity Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Step 2: Choose threshold using percentile
PERCENTILE = 90  # Try values like 85, 90, 95 to tune
INTENSITY_THRESHOLD = np.percentile(image_array, PERCENTILE)
print(f"Using threshold from {PERCENTILE}th percentile: {INTENSITY_THRESHOLD:.2f}")

# Step 3: Extract bright pixels using dynamic threshold
def get_bright_pixels(image_array, threshold):
    y_indices, x_indices = np.where(image_array >= threshold)
    coords = np.column_stack((x_indices, y_indices))
    return coords

bright_pixels = get_bright_pixels(image_array, INTENSITY_THRESHOLD)

# If too few bright pixels are selected, lower the percentile and re-run
if bright_pixels.shape[0] < NUM_GRIDS:
    raise ValueError(f"Too few bright pixels ({bright_pixels.shape[0]}) found at threshold {INTENSITY_THRESHOLD:.2f}. Try a lower percentile.")


# ========== VISUALIZATION ==========
plt.figure(figsize=(12, 8))
plt.imshow(image_array, cmap='gray')
for (x, y) in final_centers:
    plt.scatter(x, y, color='red', s=50, edgecolors='black')
plt.title("Suggested Power Grid Locations")
plt.axis('off')
plt.savefig("Suggested_Power_Grids2.png", bbox_inches="tight")
plt.show()