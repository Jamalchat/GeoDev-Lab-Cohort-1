import geopandas as gpd
import pandas as pd

wards = gpd.read_file("data/processed/wards.gpkg", layer="wards")
pop = pd.read_csv("data/raw/ward_population.csv")

first_try = wards.merge(pop, left_on="ward_name", right_on="ward", how="left")
matched = first_try["population_2024"].notnull().sum()
print("Matched on first try:", matched, "of", len(wards))
print(wards)
print(pop)

def clean_name(name):
    return name.strip().lower().replace(" ", "_")

wards["join_key"] = wards["ward_name"].apply(clean_name)
pop["join_key"] = pop["ward"].apply(clean_name)

joined = wards.merge(pop, on="join_key", how="left")
matched = joined["population_2024"].notnull().sum()
print("Matched after cleaning:", matched, "of", len(wards))
print(joined[["ward_name", "population_2024"]])
