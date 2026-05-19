import os
import sys
import json
import pickle
import hashlib
import platform
from pathlib import Path

from objects import get_test_objects


def hash_pickle(obj, protocol):
    data = pickle.dumps(obj, protocol=protocol)
    sha256 = hashlib.sha256(data).hexdigest()

    restored = pickle.loads(data)
    data_after_load = pickle.dumps(restored, protocol=protocol)
    sha256_after_load = hashlib.sha256(data_after_load).hexdigest()

    return {
        "sha256": sha256,
        "length": len(data),
        "pickle_hex": data.hex(),
        "roundtrip_sha256": sha256_after_load,
        "roundtrip_hash_identical": sha256 == sha256_after_load,
    }


def main():
    protocol = int(os.environ["PICKLE_PROTOCOL"])
    objects = get_test_objects()

    result = {
        "environment": {
            "system": platform.system(),
            "platform": platform.platform(),
            "python": sys.version,
            "protocol": protocol,
            "hashseed": os.environ.get("PYTHONHASHSEED"),
        },
        "objects": {},
    }

    has_failure = False

    for name, obj in objects.items():
        try:
            result["objects"][name] = hash_pickle(obj, protocol)
            if not result["objects"][name]["roundtrip_hash_identical"]:
                has_failure = True
        except Exception as e:
            has_failure = True
            result["objects"][name] = {
                "error": type(e).__name__,
                "message": str(e),
            }

    Path("results").mkdir(exist_ok=True)

    filename = (
        f"results/"
        f"{platform.system()}-"
        f"py{sys.version_info.major}.{sys.version_info.minor}-"
        f"p{protocol}-"
        f"seed{os.environ.get('PYTHONHASHSEED')}.json"
    )

    Path(filename).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

    if has_failure:
        sys.exit(1)


if __name__ == "__main__":
    main()
