import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from geopy.distance import geodesic
from PIL import Image

# ========== PARAMETERS ==========
NUM_GRIDS = 15                         # Number of power grids to be placed
MIN_DISTANCE_KM = 50                   # Minimum distance between two grids (in km)
INTENSITY_THRESHOLD = 200              # Brightness threshold to select pixels
IMAGE_PATH = "./Png_Files/NTL/NightLights_2022.png"

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
def get_bright_pixels(image_array, threshold):
    y_indices, x_indices = np.where(image_array >= threshold)
    coords = np.column_stack((x_indices, y_indices))
    return coords

def filter_by_distance(coords, min_dist_km, width, height):
    selected = []
    for coord in coords:
        latlon = pixel_to_geo(coord[0], coord[1], width, height)
        if all(geodesic(latlon, pixel_to_geo(s[0], s[1], width, height)).km >= min_dist_km for s in selected):
            selected.append(coord)
        if len(selected) >= NUM_GRIDS:
            break
    return np.array(selected)

# Extract bright pixels
bright_pixels = get_bright_pixels(image_array, INTENSITY_THRESHOLD)

# Use KMeans clustering to find candidate locations
kmeans = KMeans(n_clusters=NUM_GRIDS*3, random_state=42).fit(bright_pixels)
cluster_centers = np.round(kmeans.cluster_centers_).astype(int)

# Filter based on spatial constraint
final_centers = filter_by_distance(cluster_centers, MIN_DISTANCE_KM, width, height)

# ========== VISUALIZATION ==========
plt.figure(figsize=(12, 8))
plt.imshow(image_array, cmap='gray')
for (x, y) in final_centers:
    plt.scatter(x, y, color='red', s=50, edgecolors='black')
plt.title("Suggested Power Grid Locations")
plt.axis('off')
plt.show()
