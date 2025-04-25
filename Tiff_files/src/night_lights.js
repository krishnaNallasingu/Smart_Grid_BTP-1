var geometry = 
    /*WASHINGTON*/
    ee.Geometry.Polygon(
        [[[-78.49769757376221, 39.90711575123437],
          [-78.49769757376221, 37.846134898619894],
          [-75.65223858938721, 37.846134898619894],
          [-75.65223858938721, 39.90711575123437]]], null, false);

var startYear = 2014;
var endYear = 2022;

for (var year = startYear; year <= endYear; year++) {
  var startDate = ee.Date.fromYMD(year, 1, 1);
  var endDate = ee.Date.fromYMD(year + 1, 1, 1);
  
  var dataset = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG')
                  .filterDate(startDate, endDate)
                  .select('avg_rad');
  
  var yearlyAvg = dataset.mean().clip(geometry);
  
  Export.image.toDrive({
    image: yearlyAvg,
    description: 'NTL_' + year,
    folder: 'NTL_01_Washington',
    fileNamePrefix: 'NTL_' + year,
    region: geometry,
    scale: 500,
    maxPixels: 1e13,
    fileFormat: 'GeoTIFF'
  });
}
