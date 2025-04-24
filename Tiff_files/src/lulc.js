// Define your region of interest
var geometry = /* color: #d63000 */ee.Geometry.Polygon(
    [[[-79.6104828125, 42.1057705066091],
      [-79.6104828125, 36.588415552450094],
      [-71.0850921875, 36.588415552450094],
      [-71.0850921875, 42.1057705066091]]], null, false);

// Define visualization parameters (optional)
var igbpLandCoverVis = {
    min: 1.0,
    max: 17.0,
    palette: [
      '05450a', '086a10', '54a708', '78d203', '009900', 'c6b044', 'dcd159',
      'dade48', 'fbff13', 'b6ff05', '27ff87', 'c24f44', 'a5a5a5', 'ff6d4c',
      '69fff8', 'f9ffa4', '1c0dff'
    ],
  };
  
  // Load the MODIS land cover dataset
  var dataset = ee.ImageCollection('MODIS/061/MCD12Q1').select('LC_Type1');
  
  // Loop through each year from 2014 to 2022
  for (var year = 2014; year <= 2022; year++) {
    // Filter the dataset for the specific year
    var image = dataset
      .filter(ee.Filter.calendarRange(year, year, 'year'))
      .first()
      .clip(geometry);  // Clip to your area of interest
  
    // Add to map (optional for visualization)
    Map.addLayer(image, igbpLandCoverVis, 'LULC ' + year);
  
    // Export the image
    Export.image.toDrive({
      image: image,
      description: 'MODIS_LULC_' + year,
      folder: 'GEE_LULC_Exports_2',
      fileNamePrefix: 'MODIS_LULC_' + year,
      region: geometry,
      scale: 500,  // MODIS native resolution
      crs: 'EPSG:4326',
      maxPixels: 1e13
    });
  }
  
  // Center map for viewing
  Map.centerObject(geometry, 6);
  