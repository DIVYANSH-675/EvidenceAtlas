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


def build_report(claims, corpus, predictions):
    report = []
    for identity, prediction in predictions.items():
        if identity not in claims:
            raise ValueError(f"Unknown claim: {identity}")
        evidence, warnings = [], []
        for doc_id, item in prediction.get("evidence", {}).items():
            label = item["label"]
            if label not in ("SUPPORT", "CONTRADICT"):
                raise ValueError(f"Unsupported label: {label}")
            doc = corpus.get(str(doc_id))
            if doc is None:
                warnings.append(f"Document {doc_id} missing from corpus")
                continue
            selected = []
            for index in item["sentences"]:
                if type(index) is not int or not 0 <= index < len(doc["abstract"]):
                    raise ValueError(f"Invalid sentence index in document {doc_id}: {index}")
                selected.append({"index": index, "text": doc["abstract"][index]})
            if not selected:
                warnings.append(f"Document {doc_id} has no selected rationale sentences")
            evidence.append({"document": str(doc_id), "title": doc["title"],
                             "label": label, "sentences": selected})
        labels = {entry["label"] for entry in evidence if entry["sentences"]}
        report.append({"id": identity, "claim": claims[identity]["claim"],
                       "mixed_predictions": len(labels) > 1, "evidence": evidence,
                       "warnings": warnings})
    return report


def render(report):
    esc = lambda value: html.escape(str(value), quote=True)
    pieces = ['<!doctype html><html lang="en"><meta charset="utf-8">',
              '<meta name="viewport" content="width=device-width,initial-scale=1">',
              '<title>EvidenceAtlas</title><style>body{font:18px system-ui;max-width:960px;margin:40px auto;padding:20px;background:#f5f6fa;color:#202a36}article{padding:24px;background:white;margin:20px 0;border-radius:12px}blockquote{border-left:4px solid #526a99;padding-left:16px}small{color:#555}</style>',
              '<h1>EvidenceAtlas</h1><p>Model predictions with source sentences. Mixed labels require review; they do not establish a scientific contradiction.</p>']
    for row in report:
        pieces.append(f'<article><h2>{esc(row["claim"])}</h2><small>Claim {esc(row["id"])}</small>')
        if row["mixed_predictions"]:
            pieces.append('<p><strong>Mixed evidence predictions: review experimental context.</strong></p>')
        if not row["evidence"]:
            pieces.append('<p>No linked evidence available.</p>')
        for warning in row["warnings"]:
            pieces.append(f'<p>{esc(warning)}</p>')
        for item in row["evidence"]:
            pieces.append(f'<details open><summary>{esc(item["label"])} — {esc(item["title"])} (document {esc(item["document"])})</summary>')
            for sentence in item["sentences"]:
                pieces.append(f'<blockquote><small>Sentence {sentence["index"]}</small><p>{esc(sentence["text"])}</p></blockquote>')
            pieces.append('</details>')
        pieces.append('</article>')
    return '\n'.join(pieces) + '</html>\n'


