from zipfile import ZipFile
import kml2geojson
import os
import json

# Define paths
kmz_file_path = './public/files/kmz/cambodia-thai-war-zone.kmz'  # Replace with your KMZ file path
output_directory = 'output_dir' # Replace with your desired output directory

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Extract the KML file from the KMZ
extracted_kml_path = os.path.join(output_directory, 'doc.kml')
with ZipFile(kmz_file_path, 'r') as kmz_file:
    kmz_file.extract('doc.kml', output_directory) # Assumes 'doc.kml' is the primary KML file

# Convert the extracted KML to GeoJSON
geojson_data = kml2geojson.main.convert(extracted_kml_path)

# Save the GeoJSON to a file
output_geojson_path = os.path.join(output_directory, 'output.geojson')
with open(output_geojson_path, 'w') as f:
    json.dump(geojson_data, f, indent=4)

print(f"KMZ converted to GeoJSON and saved to: {output_geojson_path}")