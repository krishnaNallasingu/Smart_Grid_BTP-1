from PIL import Image
import numpy as np

def compute_difference(image_path_early, image_path_late, output_filename, threshold=50, color=(255, 0, 0)):
    """Compute and save a difference image between two years.
    
    Highlights:
    - Red: Newly lit in late image only
    - White: Lit in both
    """
    # Load grayscale images
    early = np.array(Image.open(image_path_early).convert('L'))
    late = np.array(Image.open(image_path_late).convert('L'))
    
    # Generate binary masks
    mask_early = early > threshold
    mask_late = late > threshold
    
    # Compute changes
    both_lit = mask_early & mask_late      # White
    newly_lit = ~mask_early & mask_late    # Red
    
    # Create output RGB image
    output = np.zeros((*early.shape, 3), dtype=np.uint8)
    output[both_lit] = [255, 255, 255]     # White
    output[newly_lit] = color             # Color
    
    # Save result
    Image.fromarray(output).save(output_filename)
    print(f"Saved: {output_filename}")

# === Call the function for each comparison ===

# 1.png to 9.png → actual difference 2014–2022
compute_difference('Input/1.png', 'Input/9.png', 'Output/_delhi_actual_difference_2014_2022.png', color=(255, 0, 0))

# 10.png to 19.png → prediction difference 2022–2032
compute_difference('Input/10.png', 'Input/19.png', 'Output/_delhi_prediction_difference_2022_2032.png', color=(0, 255, 0))

# 1.png to 19.png → total difference 2014–2032
compute_difference('Input/1.png', 'Input/19.png', 'Output/_delhi_complete_difference_2014_2032.png', color = (0, 0, 255))
