import geopandas as gpd

wards= gpd.read_file("data/processed/wards.gpkg", layer="wards")

print(wards.head())
print("Rows and columns:", wards.shape)
print(wards.geom_type.value_counts())
print("CRS:", wards.crs)
print("Bounds:", wards.total_bounds)