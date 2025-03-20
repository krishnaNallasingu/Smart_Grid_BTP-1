import rasterio
from rasterio.transform import Affine

# Input and output file paths
input_raster = "misaligned.tif"  # Replace with your raster file
output_raster = "aligned.tif"

# Shift parameters (modify as needed)
shift_x = 0   # No shift in X direction
shift_y = -10  # Shift downward by 10 units (adjust as per your CRS unit)

# Open the raster
with rasterio.open(input_raster) as src:
    # Modify the transform to shift the raster
    transform = src.transform * Affine.translation(shift_x, shift_y)
    
    # Copy metadata and update transform
    out_meta = src.meta.copy()
    out_meta.update({"transform": transform})
    
    # Write the output raster
    with rasterio.open(output_raster, "w", **out_meta) as dst:
        dst.write(src.read())

print(f"Raster saved as {output_raster} with adjusted alignment.")
