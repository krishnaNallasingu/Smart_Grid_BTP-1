gdalwarp -t_srs EPSG:4326 -r bilinear -tr 0.001 0.001 -co COMPRESS=DEFLATE GHSL_2020.tif GHSL_2020_destretched.tif
gdalwarp -t_srs EPSG:4326 -r bilinear -tr 0.001 0.001 -co COMPRESS=DEFLATE GHSL_2025.tif GHSL_2025_destretched.tif
gdalwarp -t_srs EPSG:4326 -r bilinear -tr 0.001 0.001 -co COMPRESS=DEFLATE GHSL_2015.tif GHSL_2015_destretched.tif
gdalwarp -t_srs EPSG:4326 -r bilinear -tr 0.001 0.001 -co COMPRESS=DEFLATE GHSL_2030.tif GHSL_2030_destretched.tif
