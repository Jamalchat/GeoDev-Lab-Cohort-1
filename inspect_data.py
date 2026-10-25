
#%%

# import csv

# with open('states.csv', encoding='utf-8-sig') as f:
#     reader = csv.DictReader(f)
#     rows = list(reader)

#     # print("Number of rows:", len(rows))
#     # print("columns:", list(rows[0].keys()))

# values = []
# for row in rows:
#     raw = row["area_km2"].strip()
#     if raw == "":
#         continue
#     values.append(float(raw))

# print("Largest value", max(values))
# print("Smallest value", min(values))
# print("Count", len(values))  


# %%

def inspect_column(filename, column):

    with open(filename, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    values = []
    for row in rows:
        raw = row[column].strip()
        if raw == "":
            continue
        values.append(float(raw))

    return {
        "smallest": min(values),
        "largest": max(values),
        "count": len(values)
    }

results = inspect_column("states.csv", "area_km2")
print(results)

results = inspect_column("states.csv", "lgas")
print(results)

# %%
