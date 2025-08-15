import geopandas as gpd
from shapely.geometry import Polygon, MultiPoint, LineString

# Load GeoJSON
gdf = gpd.read_file("public/files/kmz/6zone.geojson")

# Convert each geometry to Polygon
def to_polygon(geom):
    if geom.geom_type == "Polygon":
        return geom
    elif geom.geom_type == "MultiPolygon":
        return geom.convex_hull  # or geom.envelope
    elif geom.geom_type == "LineString":
        return geom.buffer(0.0001)  # buffer to create area
    elif geom.geom_type == "Point":
        return geom.buffer(0.0001)
    elif geom.geom_type == "MultiPoint":
        return MultiPoint(geom.geoms).convex_hull
    else:
        return None  # or raise Exception

# Apply conversion
gdf["geometry"] = gdf["geometry"].apply(to_polygon)

# Save to new GeoJSON
gdf.to_file("public/files/kmz/6zone.geojson", driver="GeoJSON")
print("✅ Saved as converted_polygons.geojson")
