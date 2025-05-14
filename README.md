![Smart Grid Logo](https://github.com/krishnaNallasingu/Smart_Grid_BTP-1/blob/main/logo.jpg)

# Smart Grid BTP-1

This project focuses on analyzing and predicting ideal power grid locations using various datasets such as Night Time Lights (NTL), Land Use Land Cover (LULC), and Global Human Settlement Layer (GHSL). The project involves preprocessing data, predicting power grid locations, and visualizing results.

---

## Table of Contents
1. [Setup Instructions](#setup-instructions)
2. [Execution Steps](#execution-steps)
3. [File Structure](#file-structure)
4. [Datasets](#datasets)
5. [Notes](#notes)
6. [Acknowledgments](#acknowledgments)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/krishnaNallasingu/Smart_Grid_BTP-1.git
```

### 2. Create a Virtual Environment and Install Dependencies
```bash
cd Smart_Grid_BTP-1
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

---

## Execution Steps

### 1. Preprocess the Data
#### Convert TIFF files to PNG format:
```bash
cd preprocess
python3 converter.py
```
This script processes TIFF files and converts them into PNG format for further analysis.

#### Reduce Image Resolution (Optional):
To decrease the resolution of images for specific use cases:
```bash
python3 res_decreaser.py
```

#### Crop Images to a Specific Aspect Ratio (Optional):
To crop images to a desired aspect ratio:
```bash
python3 aspect.py
```

### 2. Predict Power Plant Locations
Run the predictor script to predict power plant locations:
```bash
cd ..
python3 predictor.py
```

### 3. Find Ideal Power Grid Locations
#### Using Night Time Lights Data:
```bash
python3 locator.py
```
#### Using Temporal Analysis:
```bash
python3 locator_Temporal.py
```
#### Using Layered Analysis (NTL + LULC):
```bash
python3 locator_layer.py
```
#### Using GHSL Data:
```bash
python3 locator_ghsl.py
```

### 4. Compare Night Lights Results
#### Compute Differences:
```bash
cd comparision
python3 compare.py
```
#### Analyze Growth Over Time:
```bash
python3 growth.py
```
#### Analyze Years of Illumination:
```bash
python3 growth2.py
```
Results will be saved in the `Output` folder.

---

## File Structure
```
Smart_Grid_BTP-1/
├── README.md           # Project description and documentation
├── requirements.txt    # Python package dependencies
├── predictor.py        # Main prediction script
├── preprocess/         # Preprocessing scripts
│   ├── converter.py    # Convert TIFF to PNG
│   ├── res_decreaser.py # Reduce image resolution
│   └── aspect.py       # Crop images to specific aspect ratio
├── comparision/        # Scripts for comparing results
│   ├── compare.py      # Compute differences between images
│   ├── growth.py       # Analyze growth over time
│   └── growth2.py      # Analyze years of illumination
├── locator.py          # Predict grid locations using NTL
├── locator_Temporal.py # Predict grid locations using temporal analysis
├── locator_layer.py    # Predict grid locations using layered analysis
├── locator_ghsl.py     # Predict grid locations using GHSL data
├── Png_Files/          # Processed PNG files
├── Tiff_files/         # Source TIFF files
└── Data/               # Results and additional data
```

---

## Datasets
- **Night Time Lights (NTL):** [VIIRS](https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_DNB_MONTHLY_V1_VCMCFG)
- **Land Use Land Cover (LULC):** [MODIS](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MCD12Q1)
- **Global Human Settlement Layer (GHSL):** [Google Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/JRC_GHSL_P2023A_GHS_BUILT_S#description)
- **Model:** [Kaggle](https://www.kaggle.com/code/susheelkrishna2/ntl-predictions)

---

## Notes
- **OSM Data:** Due to high resolution, OSM data was not used. GHSL data serves as a proxy.
- **GHSL Data:** Available every 5 years from 1975 to 2030. Comparisons are made for every 5th year.

---

## Acknowledgments
- **Final Presentation:** [Canva](https://www.canva.com/design/DAGmd8N1DDk/a3d2r4E0oYxRFX2EjkxoAw/edit?utm_content=DAGmd8N1DDk&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

Thank you for exploring this project!
