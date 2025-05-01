import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def load_images_in_order(num_years, prefix='Input/'):
    """Load grayscale images and stack them over time"""
    images = []
    for i in range(1, num_years + 1):
        path = f'{prefix}{i}.png'
        img = np.array(Image.open(path).convert('L'))
        images.append(img)
    return np.stack(images, axis=0)  # Shape: (T, H, W)

# === Load images ===
images = load_images_in_order(19)
threshold = 50

# Binary mask
binary = images > threshold

# Count lit years per pixel
lit_count = np.sum(binary, axis=0)  # (H, W)

# === Plot with color map and colorbar ===
plt.figure(figsize=(10, 8))
plt.imshow(lit_count, cmap='plasma', interpolation='nearest')
cbar = plt.colorbar(label='Years Lit (out of 19)')
plt.title('Nightlights Growth Frequency Map (2014–2032)')
plt.axis('off')

# Save
plt.savefig('Output/growth_frequency_colored_map.png', bbox_inches='tight', dpi=300)
plt.show()