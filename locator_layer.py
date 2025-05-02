import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from geopy.distance import geodesic
from PIL import Image

# ========== PARAMETERS ==========
NUM_GRIDS = 15                         # Number of power grids to be placed
MIN_DISTANCE_KM = 50                   # Minimum distance between two grids (in km)
PERCENTILE = 90                        # Night Light threshold percentile
NTL_IMAGE_PATH = "./Png_Files/LULC/MODIS_LULC_2020.png"
LULC_IMAGE_PATH = "./Png_Files/NTL/NightLights_2020.png"

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

def geo_distance_km(pt1, pt2):
    return geodesic(pt1, pt2).km

# ========== IMAGE LOADING ==========
ntl_image = Image.open(NTL_IMAGE_PATH).convert("L")  # Grayscale Night Lights
lulc_image = Image.open(LULC_IMAGE_PATH).convert("L")  # Binary LULC mask

ntl_array = np.array(ntl_image)
lulc_array = np.array(lulc_image)

if ntl_array.shape != lulc_array.shape:
    raise ValueError("Night Lights and LULC mask dimensions do not match.")

height, width = ntl_array.shape

# ========== INTENSITY THRESHOLDING ==========
plt.figure(figsize=(10, 5))
plt.hist(ntl_array.flatten(), bins=256, range=(0, 255), color='gray', edgecolor='black')
plt.title('Pixel Intensity Histogram (Night Lights)')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

INTENSITY_THRESHOLD = np.percentile(ntl_array, PERCENTILE)
print(f"Using threshold from {PERCENTILE}th percentile: {INTENSITY_THRESHOLD:.2f}")

# ========== BRIGHT PIXEL SELECTION (FILTERED BY LULC) ==========
def get_bright_pixels(ntl_array, threshold, lulc_mask):
    y_indices, x_indices = np.where((ntl_array >= threshold) & (lulc_mask == 255))
    coords = np.column_stack((x_indices, y_indices))
    return coords

bright_pixels = get_bright_pixels(ntl_array, INTENSITY_THRESHOLD, lulc_array)

if bright_pixels.shape[0] < NUM_GRIDS:
    raise ValueError(f"Too few bright pixels ({bright_pixels.shape[0]}) found. Try a lower percentile.")

# ========== CLUSTERING TO FIND INITIAL LOCATIONS ==========
kmeans = KMeans(n_clusters=NUM_GRIDS, random_state=0).fit(bright_pixels)
centers = kmeans.cluster_centers_.astype(int)

# ========== FILTERING LOCATIONS BASED ON MINIMUM DISTANCE ==========
final_centers = []
for (x, y) in centers:
    latlon = pixel_to_geo(x, y, width, height)
    if all(geo_distance_km(latlon, pixel_to_geo(cx, cy, width, height)) >= MIN_DISTANCE_KM for (cx, cy) in final_centers):
        final_centers.append((x, y))

# Optionally retry clustering with more clusters if < NUM_GRIDS
if len(final_centers) < NUM_GRIDS:
    print(f"Only {len(final_centers)} locations satisfy the distance constraint.")

# ========== VISUALIZATION ==========
plt.figure(figsize=(12, 8))
plt.imshow(ntl_array, cmap='gray')
for (x, y) in final_centers:
    plt.scatter(x, y, color='red', s=50, edgecolors='black')
plt.title("Suggested Power Grid Locations (Filtered by LULC)")
plt.axis('off')
plt.savefig("Suggested_Power_Grids_Layer.png", bbox_inches="tight")
plt.show()
