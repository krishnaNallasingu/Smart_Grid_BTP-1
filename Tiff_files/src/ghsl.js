

var geometry = /* color: #d63000 */ee.Geometry.Polygon(
        [[[-78.49769757376221, 39.90711575123437],
          [-78.49769757376221, 37.846134898619894],
          [-75.65223858938721, 37.846134898619894],
          [-75.65223858938721, 39.90711575123437]]], null, false);

/*WASHINGTON*/
/* WORKS FOR EVERY 5 YEARS*/

var geometry = /* color: #98ff00 */ee.Geometry.Polygon(
        [[[-88.30848858938721, 37.288817604934025],
          [-88.30848858938721, 35.153052590149485],
          [-85.46302960501221, 35.153052590149485],
          [-85.46302960501221, 37.288817604934025]]], null, false);

/*NASHVILLIE*/

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
