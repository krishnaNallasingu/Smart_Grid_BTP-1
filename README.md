![alternate](https://github.com/krishnaNallasingu/Smart_Grid_BTP-1/blob/main/logo.jpg)

# How to run the code ? 
### 1. Clone the Repository
```bash
git clone https://github.com/krishnaNallasingu/Smart_Grid_BTP-1.git
```

### 2. Install Dependencies
```bash
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

### 3. Converting the images
```bash
cd preprocess
python3 converter.py
```

### 4. Predict Locations of Power Plants
```bash
cd ..
python3 predictor.py
```

### 5. Finding Ideal Powergrid Locations
```bash
python3 locator.py
```

### 6. Comparing the Night Lights results
- go to the comparision folder
- add your files : actual night lights data and the predicted ones
- name the files as `{number}.png`
- store them in the `Input` folder
- to see the differences :
```bash
cd comparision
python3 compare.py
```
- to see the growth of places each year:
```bash
python3 growth.py
```
- to see how many years the lights were on :
```bash
python3 growth2.py
```
- finally you will see the output images in the `Output` folder.
  - `actual_difference_2014_2022.png` tells the difference between first actual year vs last actual year
  - `prediction_difference_2022_2032.png` tells the difference between firest predicted year vs last predicted year
  - `complete_difference_2014_2032.png` tells the difference between first actual year vs last predicted year

---

# File Structure

```
Smart_Grid_BTP-1/
├── README.md           # Project description and documentation
├── readme.md          # Instructions to run the code
├── requirements.txt   # Python package dependencies
├── predictor.py       # Main prediction script
├── Png_Files/        # Converted PNG image files
│   ├── LULC/        # Land Use Land Cover PNG images (2014-2022)
│   └── NTL/         # Night Time Lights PNG images (2014-2022)
├── preprocess/
│   └── converter.py  # Script to convert TIFF files to PNG
└── Tiff_files/      # Source TIFF image files
    ├── LULC/        # Land Use Land Cover TIFF images (2014-2022)
    └── NTL/         # Night Time Lights TIFF images (2014-2022)
```

# Datasets
- NightLights : [VIIRS](https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_DNB_MONTHLY_V1_VCMCFG)
- lulc : [MODIS](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MCD12Q1)
- model : [Kaggle](https://www.kaggle.com/code/susheelkrishna2/ntl-predictions)
- GHSL : [Google Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/JRC_GHSL_P2023A_GHS_BUILT_S#description)

  # Notes :
  - unable to get OSM data because it is very high resolution and out night lights data is covered over nearly 25K sqkm. so as a proxy to the osm, we are using ghsl data.
  - ghsl data is available from 1975 to 2030 for every 5 years only. so while comparing, we are comparing only every 5th year!
