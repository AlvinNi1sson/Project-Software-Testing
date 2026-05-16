import json
from pathlib import Path
from collections import defaultdict

groups = defaultdict(list)

for file in Path("results").glob("*.json"):
    data = json.loads(file.read_text(encoding="utf-8"))
    env = data["environment"]

    for obj_name, obj_result in data["objects"].items():
        if "sha256" not in obj_result:
            continue

        key = (obj_name, env["protocol"])
        groups[key].append({
            "file": file.name,
            "system": env["system"],
            "python": env["python"].split()[0],
            "hashseed": env["hashseed"],
            "sha256": obj_result["sha256"],
            "length": obj_result["length"],
        })

for key, rows in groups.items():
    hashes = {row["sha256"] for row in rows}

    if len(hashes) > 1:
        print("\nUNSTABLE:", key)
        for row in rows:
            print(row)