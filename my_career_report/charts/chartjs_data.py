import json
import os
from typing import Dict, List, Any


def generate_chartjs_data(data: Dict[str, Any], output_path: str) -> str:
    """Generate a JSON file with Chart.js-friendly data."""
    dataset = {
        "big5": data.get("big5", {}),
        "big5_norm": data.get("big5_norm", {}),
        "interest": data.get("interest", {}),
        "values": data.get("values", {}),
        "ai": data.get("ai", {}),
        "tech": {
            "labels": [item["name"] for item in data.get("tech", [])],
            "scores": [item["score"] for item in data.get("tech", [])],
        },
        "soft": {
            "labels": [item["name"] for item in data.get("soft", [])],
            "scores": [item["score"] for item in data.get("soft", [])],
        },
    }
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    return output_path
