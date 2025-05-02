from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

def load_images_in_order(num_years, prefix='Input/'):
    """Load grayscale images and stack them over time"""
    images = []
    for i in range(1, num_years + 1):
        path = f'{prefix}{i}.png'
        img = np.array(Image.open(path).convert('L'))
        images.append(img)
    return np.stack(images, axis=0)  # Shape: (T, H, W)

# === Load all images ===
images = load_images_in_order(19)
threshold = 50

# Convert to binary: (T, H, W)
binary = images > threshold

# Find year of first activation (0 if never lit)
lit_any = np.any(binary, axis=0)
first_lit = np.argmax(binary, axis=0) + 1  # +1 to make years 1-based
first_lit[~lit_any] = 0  # Set unlit areas to 0

# Create RGB image
output = np.zeros((*first_lit.shape, 3), dtype=np.uint8)
cmap = []

for i in range(1, 20):
    mask = first_lit == i
    r = int((1 - i / 19) * 255)
    g = int((i / 19) * 255)
    b = 150
    output[mask] = (r, g, b)
    cmap.append((r / 255, g / 255, b / 255))  # Normalize for matplotlib

# # Save the image without legend
# Image.fromarray(output).save('Output/growth_rate_map.png')

# === Add Legend with Matplotlib ===
# Include one more color for 'never lit' (set to black or transparent)
cmap.insert(0, (0, 0, 0))  # for '0' value
norm = BoundaryNorm(boundaries=np.arange(21), ncolors=20)
legend_img = plt.imshow(first_lit, cmap=ListedColormap(cmap), norm=norm)
plt.colorbar(legend_img, ticks=range(0, 20), label='Year of First Illumination')
plt.axis('off')
plt.title("Nighttime Lights Onset Map")
plt.savefig('Output/_delhi_growth_rate_map_with_legend.png', bbox_inches='tight')
plt.show()

print("Saved: growth_rate_map.png and growth_rate_map_with_legend.png")
