import geopandas as gpd
import fiona
import zipfile
import os

# Assuming your KMZ file is named 'my_polygon.kmz'
kmz_file_path = './public/files/kmz/war-zone.kmz'
kml_file_path = 'doc.kml' # The default KML file name inside a KMZ
output_sql_path = './public/files/kmz-sql/polygon.sql'

# Decompress the KMZ file
with zipfile.ZipFile(kmz_file_path, 'r') as kmz:
    kmz.extract(kml_file_path)

# Enable KML driver for reading
fiona.drvsupport.supported_drivers['KML'] = 'rw'

# Optional: KMZ (not always directly supported)
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'

# Read the KML file into a GeoDataFrame
gdf = gpd.read_file(kml_file_path, driver="KML")

# Clean up the extracted KML file
os.remove(kml_file_path)

# The GeoDataFrame now holds your polygon data
# For a single polygon, you can get the geometry directly
polygon_geometry = gdf.iloc[0].geometry

# Write result to file
with open(output_sql_path, 'w', encoding='utf-8') as f:
    for _, row in gdf.iterrows():
        geom_wkt = row.geometry.wkt
        name = row.get("Name", "null").replace("'", "''")  # Escape single quotes
        sql = f"INSERT INTO polygon (name, raw_value) VALUES ('{name}', '{geom_wkt}');\n"
        f.write(sql)

print('Cheer meh!')