import json
import os
import pickle
import hashlib
import platform
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path("tests").resolve()))

groups = defaultdict(list)
has_failure = False
target_env = {
    "system": platform.system(),
    "platform": platform.platform(),
    "python": sys.version.split()[0],
    "hashseed": os.environ.get("PYTHONHASHSEED"),
}

print("TARGET ENVIRONMENT:", target_env)

result_files = sorted(Path("results").glob("*.json"))

if not result_files:
    print("No result files found in results/")
    sys.exit(1)

for file in result_files:
    data = json.loads(file.read_text(encoding="utf-8"))
    if "environment" not in data:
        print("Skipping non-matrix result:", file.name)
        continue

    env = data["environment"]

    for obj_name, obj_result in data["objects"].items():
        if "error" in obj_result:
            has_failure = True
            print("\nPICKLE ERROR:", file.name, obj_name, obj_result)
            continue

        if not obj_result.get("roundtrip_hash_identical", True):
            has_failure = True
            print("\nROUNDTRIP HASH CHANGED:", file.name, obj_name, obj_result)

        if "sha256" not in obj_result:
            continue

        try:
            source_bytes = bytes.fromhex(obj_result["pickle_hex"])
            restored = pickle.loads(source_bytes)
            target_bytes = pickle.dumps(restored, protocol=env["protocol"])
            target_sha256 = hashlib.sha256(target_bytes).hexdigest()
        except Exception as e:
            has_failure = True
            print(
                "\nCROSS LOAD ERROR:",
                {
                    "source_file": file.name,
                    "object": obj_name,
                    "source_system": env["system"],
                    "source_python": env["python"].split()[0],
                    "source_protocol": env["protocol"],
                    "target": target_env,
                    "error": type(e).__name__,
                    "message": str(e),
                },
            )
            continue

        if target_sha256 != obj_result["sha256"]:
            has_failure = True
            print(
                "\nCROSS LOAD HASH CHANGED:",
                {
                    "source_file": file.name,
                    "object": obj_name,
                    "source_system": env["system"],
                    "source_python": env["python"].split()[0],
                    "source_protocol": env["protocol"],
                    "source_hashseed": env["hashseed"],
                    "target": target_env,
                    "source_sha256": obj_result["sha256"],
                    "target_sha256": target_sha256,
                },
            )

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
        has_failure = True
        print("\nUNSTABLE:", key)
        for row in rows:
            print(row)

if has_failure:
    sys.exit(1)
