

var startYear = 2014;
var endYear = 2030;

for (var year = startYear; year <= endYear; year++) {
  var image = ee.Image('JRC/GHSL/P2023A/GHS_BUILT_S/' + year.toString());
  var builtSurface = image.select('built_surface');
  
  // Clip the image to the region of interest (geometry)
  var clippedImage = builtSurface.clip(geometry);
  
  Export.image.toDrive({
    image: clippedImage,
    description: 'GHSL_' + year,
    folder: 'GHSL_01_Washington',
    fileNamePrefix: 'GHSL_' + year,
    region: geometry,
    scale: 500,
    maxPixels: 1e13,
    fileFormat: 'GeoTIFF'
  });
}
