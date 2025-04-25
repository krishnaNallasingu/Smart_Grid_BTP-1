var geometry = /* color: #0B4A8B */ee.Geometry.Polygon(
        [[[-116.48307387522725, 37.12246623202814],
          [-116.48307387522725, 34.98210532236753],
          [-113.47281996897725, 34.98210532236753],
          [-113.47281996897725, 37.12246623202814]]], null, false);

// change the above coordinates to your desire location

var startYear = 2014;
var endYear = 2022;

for (var year = startYear; year <= endYear; year++) {
  var startDate = ee.Date.fromYMD(year, 5, 1);
  var endDate = startDate.advance(1, 'month');

  var dataset = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG')
                  .filter(ee.Filter.date(startDate, endDate));

  var nighttime = dataset.select('avg_rad').median().clip(geometry);

  Export.image.toDrive({
    image: nighttime,
    description: 'NightLights_' + year,
    folder: 'NTL_05_Las_Vegas',
    fileNamePrefix: 'NTL_' + year,
    region: geometry,
    scale: 500, // approximate scale in meters
    crs: 'EPSG:4326',
    maxPixels: 1e13
  });
}
