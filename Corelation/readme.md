# Nighttime Lights and Land Use/Land Cover (LULC) Correlation Analysis

This project aims to analyze the correlation between nighttime lights data and Land Use/Land Cover (LULC) data for a specific region. By comparing these two datasets, we can gain insights into the relationship between human activity, urbanization, and land cover changes.

## Project Overview

The core idea is to:

1.  **Acquire Data:** Obtain nighttime lights data and LULC data for the chosen region and time period.
2.  **Preprocess Data:** Clean, format, and potentially resample the data to ensure compatibility.
3.  **Spatial Alignment:** Ensure both datasets are spatially aligned (same coordinate system, resolution, and extent).
4.  **Data Comparison:** Compare the two datasets using various raster analysis techniques.
5.  **Statistical Analysis:** Calculate correlation coefficients and other relevant statistics.
6.  **Visualization:** Create maps and graphs to visualize the relationship between nighttime lights and LULC.
7. **Interpretation:** Interpret the results and draw conclusions about the relationship between the two datasets.

## Detailed Steps

### 1. Data Acquisition

#### 1.1 Nighttime Lights Data

*   **Source:** The primary source for nighttime lights data is the **Visible Infrared Imaging Radiometer Suite (VIIRS) Day/Night Band (DNB)**, available from the **National Oceanic and Atmospheric Administration (NOAA)**.
    *   **Website:** [https://eogdata.noaa.gov/products/vnl/](https://eogdata.noaa.gov/products/vnl/)
    *   **Data Type:** Radiance-calibrated nighttime lights, typically provided as monthly or annual composites.
    *   **Resolution:** Approximately 500-750 meters.
    *   **Format:** GeoTIFF.
    * **Data to download:** You can download the annual or monthly cloud free data.
*   **Alternative Source:**
    *   **Earth Observation Group (EOG):** [https://eogdata.mines.edu/products/vnl/](https://eogdata.mines.edu/products/vnl/)
    *   **DMSP-OLS:** Older dataset, but useful for historical analysis (1992-2013).
*   **Considerations:**
    *   **Time Period:** Select the appropriate time period for your analysis.
    *   **Cloud Cover:** VIIRS data is typically cloud-free, but check for any remaining cloud contamination.
    *   **Calibration:** Be aware of potential calibration issues between different years or sensors.

#### 1.2 Land Use/Land Cover (LULC) Data

*   **Source:** The best source depends on the region and resolution you need.
    *   **Global Datasets:**
        *   **ESA WorldCover:** [https://esa-worldcover.org/en](https://esa-worldcover.org/en) (10m resolution, global coverage)
        *   **Copernicus Global Land Cover:** [https://lcviewer.vito.be/](https://lcviewer.vito.be/) (100m resolution, global coverage)
        *   **MODIS Land Cover:** [https://lpdaac.usgs.gov/products/mcd12q1v006/](https://lpdaac.usgs.gov/products/mcd12q1v006/) (500m resolution, global coverage)
    *   **Regional/National Datasets:**
        *   **USGS National Land Cover Database (NLCD):** [https://www.mrlc.gov/](https://www.mrlc.gov/) (For the US)
        *   **European Environment Agency (EEA) Corine Land Cover:** [https://land.copernicus.eu/pan-european/corine-land-cover](https://land.copernicus.eu/pan-european/corine-land-cover) (For Europe)
        *   **National/Regional Mapping Agencies:** Check the official mapping agencies for your specific region.
*   **Data Type:** Categorical data representing different land cover classes (e.g., forest, urban, water, agriculture).
*   **Resolution:** Varies depending on the source (10m to 1km).
*   **Format:** GeoTIFF.
*   **Considerations:**
    *   **Classification Scheme:** Understand the LULC classification scheme used by the dataset.
    *   **Accuracy:** Check the reported accuracy of the LULC data.
    *   **Time Period:** Ensure the LULC data is from the same or a comparable time period as the nighttime lights data.

### 2. Data Preprocessing

#### 2.1 Data Cleaning
* **Night Lights:**
    * Check for any no data values and handle them.
    * Check for any outliers and handle them.
* **LULC:**
    * Check for any no data values and handle them.
    * Check for any errors in the classification and handle them.

#### 2.2 Data Formatting
*   **File Format:** Ensure both datasets are in GeoTIFF format.
*   **Coordinate System:** Verify that both datasets use the same coordinate reference system (CRS). If not, reproject one of them.
*   **Data Type:** Ensure that the data type is appropriate for analysis (e.g., float for nighttime lights, integer for LULC classes).

#### 2.3 Resampling (if necessary)

*   If the resolutions of the two datasets are different, you may need to resample one of them to match the other.
*   **Method:** Use a resampling method appropriate for the data type (e.g., nearest neighbor for categorical LULC, bilinear or cubic for continuous nighttime lights).
*   **Tool:** GDAL, Rasterio, or QGIS.

### 3. Spatial Alignment

*   **Extent:** Ensure both datasets cover the same geographic area. If not, clip one of them to match the other.
*   **Resolution:** Ensure both datasets have the same resolution.
*   **Coordinate System:** Ensure both datasets have the same coordinate system.
*   **Tool:** GDAL, Rasterio, or QGIS.

### 4. Data Comparison

#### 4.1 Zonal Statistics

*   **Concept:** Calculate statistics (e.g., mean, sum, standard deviation) of nighttime lights within each LULC class.
*   **Method:**
    1.  Use the LULC raster as "zones."
    2.  Calculate statistics of the nighttime lights raster within each zone.
*   **Tool:** GDAL, Rasterio, or QGIS.

#### 4.2 Raster Overlay

*   **Concept:** Overlay the two rasters to analyze the relationship between nighttime lights and specific LULC classes at each pixel.
*   **Method:**
    1.  Create a new raster where each pixel value represents a combination of nighttime lights and LULC class.
    2.  Analyze the distribution of nighttime lights values within each LULC class.
*   **Tool:** GDAL, Rasterio, or QGIS.

#### 4.3 Change Detection (if applicable)

*   **Concept:** If you have multiple time periods of data, analyze changes in nighttime lights and LULC over time.
*   **Method:**
    1.  Calculate the difference in nighttime lights between two time periods.
    2.  Calculate the change in LULC classes between two time periods.
    3.  Compare the changes in nighttime lights with the changes in LULC.
*   **Tool:** GDAL, Rasterio, or QGIS.

### 5. Statistical Analysis

#### 5.1 Correlation Analysis

*   **Concept:** Calculate the correlation coefficient (e.g., Pearson's r) between nighttime lights and LULC.
*   **Method:**
    1.  Extract the nighttime lights values for each LULC class.
    2.  Calculate the correlation coefficient between the nighttime lights values and the LULC class.
*   **Tool:** Python (NumPy, SciPy), R.

#### 5.2 Regression Analysis

*   **Concept:** Model the relationship between nighttime lights and LULC using regression techniques.
*   **Method:**
    1.  Use nighttime lights as the dependent variable.
    2.  Use LULC classes (or derived variables) as independent variables.
    3.  Fit a regression model.
*   **Tool:** Python (Statsmodels, Scikit-learn), R.

### 6. Visualization

#### 6.1 Maps

*   **Nighttime Lights Map:** Display the nighttime lights data as a grayscale or color-coded map.
*   **LULC Map:** Display the LULC data as a categorical map with different colors for each class.
*   **Overlay Map:** Overlay the nighttime lights and LULC data to visualize their spatial relationship.
*   **Change Detection Map:** Display the changes in nighttime lights and LULC over time.
*   **Tool:** QGIS, ArcGIS, Python (Matplotlib, GeoPandas).

#### 6.2 Graphs

*   **Box Plots:** Show the distribution of nighttime lights values within each LULC class.
*   **Scatter Plots:** Plot nighttime lights values against LULC class (or derived variables).
*   **Bar Charts:** Compare the mean nighttime lights values for different LULC classes.
*   **Line Graphs:** Show the change in nighttime lights and LULC over time.
*   **Tool:** Python (Matplotlib, Seaborn), R.

### 7. Interpretation

*   **Analyze the Results:** Examine the correlation coefficients, regression results, maps, and graphs.
*   **Draw Conclusions:** What is the relationship between nighttime lights and LULC in your region?
*   **Consider Limitations:** Acknowledge any limitations of the data or methods.
*   **Discuss Implications:** What are the implications of your findings for urban planning, environmental management, or other relevant fields?

## Tools

*   **GIS Software:** QGIS, ArcGIS
*   **Programming Languages:** Python (GDAL, Rasterio, NumPy, SciPy, Matplotlib, Seaborn, GeoPandas), R
*   **Data Processing Libraries:** GDAL, Rasterio
*   **Statistical Libraries:** NumPy, SciPy, Statsmodels, Scikit-learn (Python), R

## Example Python Code Snippets (Illustrative)

```python
# Example: Reading a GeoTIFF file with Rasterio
import rasterio
with rasterio.open("nighttime_lights.tif") as src:
    nightlights_data = src.read(1)  # Read the first band

# Example: Calculating zonal statistics with Rasterio and NumPy
import numpy as np
import rasterio.mask
with rasterio.open("lulc.tif") as src:
    lulc_data = src.read(1)
    profile = src.profile

# Assuming you have a list of unique LULC classes
unique_classes = np.unique(lulc_data)
for class_id in unique_classes:
    mask = lulc_data == class_id
    masked_nightlights = np.where(mask, nightlights_data, np.nan)
    mean_nightlights = np.nanmean(masked_nightlights)
    print(f"Mean nightlights for class {class_id}: {mean_nightlights}")

# Example: Calculating correlation
from scipy.stats import pearsonr
correlation, p_value = pearsonr(nightlights_data.flatten(), lulc_data.flatten())
print(f"Correlation: {correlation}, p-value: {p_value}")
```
