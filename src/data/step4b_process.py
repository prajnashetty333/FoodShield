import json
import csv
import os
import time

start_time = time.time()

# Locked commodities and their CPC codes
cpc_mapping = {
    "'0111": "wheat",
    "'0113": "rice",
    "'0112": "maize",
    "'2165": "palm_oil",
    "'2351f": "sugar",
    "'23511.02": "sugar",
    "'21631.01": "sunflower_oil"
}

input_entities = "c:/Users/prajn/Downloads/datathon20206/food-trade-resilience/data/raw/unique_entities.json"
trade_data_path = "c:/Users/prajn/Downloads/datathon20206/food-trade-resilience/data/raw/Trade_DetailedTradeMatrix_E_All_Data_(Normalized).csv"
out_dir = "c:/Users/prajn/Downloads/datathon20206/food-trade-resilience/data/processed/foodshield"
os.makedirs(out_dir, exist_ok=True)

with open(input_entities, "r", encoding="utf-8") as f:
    entities = json.load(f)

# Entity dict to track properties
# key: country_code
entity_data = {}

for row in entities:
    code, m49, name = row
    std_name = name.strip()
    
    # Classification logic
    entity_type = "UNKNOWN"
    is_aggregate = False
    
    # We saw these territories earlier
    territories = [
        "johnston island", "midway island", "wake island", 
        "canton and enderbury islands", "macao", "hong kong", "taiwan",
        "united states minor outlying islands", "heard and mcdonald islands",
        "palestine", "bouvet island", "french polynesia", "new caledonia", 
        "martinique", "reunion", "guadeloupe", "french guiana"
    ]
    
    name_lower = std_name.lower()
    
    # Basic check for aggregates (none were found previously, but keep logic)
    agg_keywords = ["world", "unspecified", "nes", "aggregate", "eu(", "european union", "group", "total", "areas", "confidential"]
    for kw in agg_keywords:
        if kw in name_lower.split() or f" {kw} " in f" {name_lower} ":
            is_aggregate = True
            entity_type = "AGGREGATE"
            break
            
    if not is_aggregate:
        is_territory = False
        for t in territories:
            if t in name_lower:
                is_territory = True
                break
        if is_territory:
            entity_type = "ECONOMY/TERRITORY"
        else:
            entity_type = "COUNTRY"
            
    is_valid_analytical_entity = "YES" if not is_aggregate else "NO"

    entity_data[code] = {
        "country_code": code,
        "m49_code": m49,
        "country_name": name,
        "standardized_country_name": std_name,
        "entity_type": entity_type,
        "is_aggregate": "YES" if is_aggregate else "NO",
        "is_valid_analytical_entity": is_valid_analytical_entity,
        "is_trade_reporter": "NO",
        "is_trade_partner": "NO",
        "has_wheat_trade": "NO",
        "has_rice_trade": "NO",
        "has_maize_trade": "NO",
        "has_palm_oil_trade": "NO",
        "has_sugar_trade": "NO",
        "has_sunflower_oil_trade": "NO"
    }

# Pass through the 8GB dataset
# We don't need to parse every field using csv.reader, splitting by comma is much faster
# But since some fields might have commas inside quotes, we should be careful.
# Wait, column indices:
# 0: Reporter Country Code
# 1: Reporter Country Code (M49)
# 2: Reporter Countries (might contain comma)
# 3: Partner Country Code
# 4: Partner Country Code (M49)
# 5: Partner Countries (might contain comma)
# 6: Item Code
# 7: Item Code (CPC) -> this is what we need!
# Since CPC codes don't have commas, and we know they appear around 7th or 8th column, it might be tricky with simple split.
# Actually, csv.reader is robust and we only do it once. Let's use csv.reader to be safe, maybe it takes 5 mins.

with open(trade_data_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    
    for row in reader:
        try:
            rep_code = row[0]
            part_code = row[3]
            cpc_code = row[7]
            
            # Update roles
            if rep_code in entity_data:
                entity_data[rep_code]["is_trade_reporter"] = "YES"
            if part_code in entity_data:
                entity_data[part_code]["is_trade_partner"] = "YES"
                
            # Check commodity
            if cpc_code in cpc_mapping:
                comm = cpc_mapping[cpc_code]
                if rep_code in entity_data:
                    entity_data[rep_code][f"has_{comm}_trade"] = "YES"
                if part_code in entity_data:
                    entity_data[part_code][f"has_{comm}_trade"] = "YES"
        except IndexError:
            pass

# Output CSV
csv_path = os.path.join(out_dir, "foodshield_country_universe.csv")
cols = [
    "country_code", "country_name", "standardized_country_name", "entity_type", 
    "is_aggregate", "is_valid_analytical_entity", "is_trade_reporter", "is_trade_partner",
    "has_wheat_trade", "has_rice_trade", "has_maize_trade", 
    "has_palm_oil_trade", "has_sugar_trade", "has_sunflower_oil_trade"
]

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
    writer.writeheader()
    for code in sorted(entity_data.keys(), key=lambda x: int(x) if x.isdigit() else x):
        writer.writerow(entity_data[code])

# Compute stats for report
raw_entities = len(entity_data)
counts = {"COUNTRY": 0, "ECONOMY/TERRITORY": 0, "AGGREGATE": 0, "OTHER": 0, "UNKNOWN": 0}
excluded = []
reporters = 0
partners = 0
both = 0
valid_analytical = 0

comm_counts = {
    "wheat": 0, "rice": 0, "maize": 0, "palm_oil": 0, "sugar": 0, "sunflower_oil": 0
}

for d in entity_data.values():
    counts[d["entity_type"]] += 1
    if d["is_valid_analytical_entity"] == "NO":
        excluded.append(d)
    else:
        valid_analytical += 1
        is_rep = d["is_trade_reporter"] == "YES"
        is_part = d["is_trade_partner"] == "YES"
        if is_rep: reporters += 1
        if is_part: partners += 1
        if is_rep and is_part: both += 1
        
        for c in comm_counts.keys():
            if d[f"has_{c}_trade"] == "YES":
                comm_counts[c] += 1

# Generate Report
report_path = os.path.join(out_dir, "FOODSHIELD_STEP_4B_COUNTRY_VALIDATION_REPORT.md")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("# FOODSHIELD STEP 4B: COUNTRY UNIVERSE VALIDATION REPORT\n\n")
    
    f.write("## 1. Raw universe\n\n")
    f.write(f"* Total entities detected: {raw_entities}\n")
    f.write(f"* Total unique entity codes: {len(set(d['country_code'] for d in entity_data.values()))}\n")
    f.write(f"* Total unique entity names: {len(set(d['standardized_country_name'] for d in entity_data.values()))}\n\n")
    
    f.write("## 2. Entity classification\n\n")
    f.write("| Entity Type       | Count |\n")
    f.write("| ----------------- | ----: |\n")
    f.write(f"| COUNTRY           | {counts['COUNTRY']} |\n")
    f.write(f"| ECONOMY/TERRITORY | {counts['ECONOMY/TERRITORY']} |\n")
    f.write(f"| AGGREGATE         | {counts['AGGREGATE']} |\n")
    f.write(f"| OTHER             | {counts['OTHER']} |\n")
    f.write(f"| UNKNOWN           | {counts['UNKNOWN']} |\n\n")
    
    f.write("## 3. Exclusions\n\n")
    if excluded:
        for ex in excluded:
            f.write(f"* {ex['country_code']} - {ex['standardized_country_name']} ({ex['entity_type']}): Excluded because it is an aggregate/invalid entity.\n")
    else:
        f.write("> \"No entities were excluded at the country-universe stage.\"\n\n")
        
    f.write("## 4. Final analytical universe\n\n")
    f.write(f"* total valid analytical entities: {valid_analytical}\n")
    f.write(f"* countries/economies acting as reporters: {reporters}\n")
    f.write(f"* countries/economies acting as partners: {partners}\n")
    f.write(f"* entities acting as both: {both}\n\n")
    
    f.write("## 5. Commodity coverage\n\n")
    f.write("| Commodity     | Countries/Economies with trade data |\n")
    f.write("| ------------- | ----------------------------------: |\n")
    f.write(f"| Wheat         | {comm_counts['wheat']} |\n")
    f.write(f"| Rice          | {comm_counts['rice']} |\n")
    f.write(f"| Maize         | {comm_counts['maize']} |\n")
    f.write(f"| Palm Oil      | {comm_counts['palm_oil']} |\n")
    f.write(f"| Sugar         | {comm_counts['sugar']} |\n")
    f.write(f"| Sunflower Oil | {comm_counts['sunflower_oil']} |\n\n")
    
    f.write("## 6. Important methodological decision\n\n")
    f.write("> \"Countries were not pre-selected based on import dependence or vulnerability. Country selection was determined independently of the subsequent FOODSHIELD risk calculations.\"\n\n")
    
    f.write("## 7. Data limitations\n\n")
    f.write("* Some valid economies may act only as partners and never as reporters.\n")
    f.write("* Missing trade observations for certain commodities in specific countries are preserved as structural network features, not deleted.\n\n")

print(f"Extraction and report generation finished in {time.time() - start_time:.2f} seconds.")
print("Summary:")
print(f"Raw FAOSTAT entities: {raw_entities}")
print(f"Individual countries/economies: {valid_analytical}")
print(f"Aggregates: {counts['AGGREGATE']}")
print(f"Excluded entities: {len(excluded)}")
print(f"Final analytical universe: {valid_analytical}\n")
print(f"Reporter entities: {reporters}")
print(f"Partner entities: {partners}")
print(f"Both reporter + partner: {both}\n")
print(f"Wheat coverage: {comm_counts['wheat']}")
print(f"Rice coverage: {comm_counts['rice']}")
print(f"Maize coverage: {comm_counts['maize']}")
print(f"Palm Oil coverage: {comm_counts['palm_oil']}")
print(f"Sugar coverage: {comm_counts['sugar']}")
print(f"Sunflower Oil coverage: {comm_counts['sunflower_oil']}\n")
print("Country universe status: READY")
