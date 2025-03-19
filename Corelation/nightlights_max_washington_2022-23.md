```javascript
var dataset = ee.ImageCollection('NOAA/VIIRS/DNB/ANNUAL_V22')
                  .filter(ee.Filter.date('2022-01-01', '2023-01-01'))
                  .median();  // Reduce collection to a single image

var nighttime = dataset.select('maximum');

// Define visualization parameters
var nighttimeVis = {min: 0.0, max: 60.0};
Map.setCenter(-77.1056, 38.8904, 8);
Map.addLayer(nighttime, nighttimeVis, 'Nighttime');

// Define Region of Interest (ROI)
var geometry = ee.Geometry.Polygon(
    [[[-78.24942696563728, 39.984566109238514],
      [-78.24942696563728, 37.96918430732993],
      [-75.53580391876228, 37.96918430732993],
      [-75.53580391876228, 39.984566109238514]]], null, false);

// Clip the image to the region
var clippedImage = nighttime.clip(geometry);

// Export the image to Google Drive
Export.image.toDrive({
  image: clippedImage,
  description: 'Nighttime_Lights',
  scale: 500,  // Pixel resolution in meters
  region: geometry,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13
});

```