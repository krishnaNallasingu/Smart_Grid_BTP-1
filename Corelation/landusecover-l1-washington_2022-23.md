```javascript
// Load MODIS Land Cover Dataset
var dataset = ee.ImageCollection('MODIS/061/MCD12Q1')
                  .filter(ee.Filter.date('2022-01-01', '2022-12-31')) // Select year 2022
                  .first();  // Get the first image (MCD12Q1 provides yearly data)

// Select the Land Cover Classification (IGBP scheme)
var igbpLandCover = dataset.select('LC_Type1');

// Define Visualization Parameters
var igbpLandCoverVis = {
  min: 1, max: 17,
  palette: [
    '05450a', '086a10', '54a708', '78d203', '009900', 'c6b044', 'dcd159',
    'dade48', 'fbff13', 'b6ff05', '27ff87', 'c24f44', 'a5a5a5', 'ff6d4c',
    '69fff8', 'f9ffa4', '1c0dff'
  ],
};

var geometry = ee.Geometry.Polygon(
    [[[-78.24942696563728, 39.984566109238514],
      [-78.24942696563728, 37.96918430732993],
      [-75.53580391876228, 37.96918430732993],
      [-75.53580391876228, 39.984566109238514]]], null, false);

// Clip the Image to the Selected Region
var clippedLULC = igbpLandCover.clip(geometry);

// Add the Clipped Layer to the Map
Map.centerObject(geometry, 7);
Map.addLayer(clippedLULC, igbpLandCoverVis, 'IGBP Land Cover');

// Export the Image to Google Drive as a GeoTIFF
Export.image.toDrive({
  image: clippedLULC,
  description: 'MODIS_LULC_2022',
  scale: 500,  // 500m resolution
  region: geometry,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13
});

```