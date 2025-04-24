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

---

# File Structure

```
Smart_Grid_BTP-1/
├── README.md           # Project description and documentation
├── readme.md          # Instructions to run the code
├── requirements.txt   # Python package dependencies
├── Png_Files/        # Converted PNG image files
│   ├── LULC/        # Land Use Land Cover PNG images (2014-2022)
│   └── NTL/         # Night Time Lights PNG images (2014-2022)
├── preprocess/
│   └── converter.py  # Script to convert TIFF files to PNG
└── Tiff_files/      # Source TIFF image files
    ├── LULC/        # Land Use Land Cover TIFF images (2014-2022)
    └── NTL/         # Night Time Lights TIFF images (2014-2022)
```
