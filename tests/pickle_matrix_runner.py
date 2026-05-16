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
    return {
        "sha256": hashlib.sha256(data).hexdigest(),
        "length": len(data),
        "pickle_hex": data.hex(),
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

    for name, obj in objects.items():
        try:
            result["objects"][name] = hash_pickle(obj, protocol)
        except Exception as e:
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


if __name__ == "__main__":
    main()