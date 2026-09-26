import tempfile
import unittest
from pathlib import Path
from evidence_atlas import build_report, render, load_index


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.claims = {"1": {"claim": "<script>alert(1)</script>"}}
        self.corpus = {"10": {"title": "Study A", "abstract": ["Observed effect"]},
                       "20": {"title": "Study B", "abstract": ["Different result"]}}

    def test_mixed_evidence_and_escaping(self):
        pred = {"1": {"evidence": {"10": {"label": "SUPPORT", "sentences": [0]},
                                    "20": {"label": "CONTRADICT", "sentences": [0]}}}}
        report = build_report(self.claims, self.corpus, pred)
        self.assertTrue(report[0]["mixed_predictions"])
        page = render(report)
        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertIn("Observed effect", page)

    def test_missing_doc_warning(self):
        report = build_report(self.claims, self.corpus,
                              {"1": {"evidence": {"99": {"label": "SUPPORT", "sentences": [0]}}}})
        self.assertTrue(report[0]["warnings"])
        self.assertFalse(report[0]["mixed_predictions"])

    def test_negative_sentence_is_rejected(self):
        with self.assertRaises(ValueError):
            build_report(self.claims, self.corpus,
                         {"1": {"evidence": {"10": {"label": "SUPPORT", "sentences": [-1]}}}})

    def test_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "claims.jsonl"
            path.write_text('{"id": 1}\n{"id": 1}\n')
            with self.assertRaises(ValueError):
                load_index(path, "id")
