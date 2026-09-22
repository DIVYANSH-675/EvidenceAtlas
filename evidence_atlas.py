"""Build an offline evidence report from SciFact prediction JSONL files."""
import argparse
import html
import json
from pathlib import Path


def load_index(path, key):
    result = {}
    for line in Path(path).read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        identity = str(row[key])
        if identity in result:
            raise ValueError(f"Duplicate {key}: {identity}")
        result[identity] = row
    return result


