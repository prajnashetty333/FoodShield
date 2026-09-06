import csv
import json
import time

start_time = time.time()
file_path = "c:/Users/prajn/Downloads/datathon20206/food-trade-resilience/data/raw/Trade_DetailedTradeMatrix_E_All_Data_(Normalized).csv"

entities = set()

with open(file_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if len(row) >= 6:
            entities.add((row[0], row[1], row[2]))
            entities.add((row[3], row[4], row[5]))

out_list = sorted(list(entities))
print(f"Found {len(out_list)} unique entities.")

with open("c:/Users/prajn/Downloads/datathon20206/food-trade-resilience/data/raw/unique_entities.json", "w", encoding="utf-8") as out:
    json.dump(out_list, out, indent=2)

print(f"Elapsed: {time.time() - start_time:.2f}s")
