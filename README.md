# EvidenceAtlas

An offline evidence explorer for SciFact predictions.

An extension maintained by Divyansh Gupta, based on [https://github.com/allenai/scifact](https://github.com/allenai/scifact) at `68b98a56d93e0f9da0d2aab4e6c3294699a0f72e`. Upstream source, licenses, citations and commit history are preserved. See [upstream documentation](UPSTREAM_README.md).

## Added functionality

Joins model predictions to claims, document titles and exact rationale sentences. Highlights mixed support/contradict predictions, warns about missing documents, rejects invalid sentence indices and escapes report text. Open report.html in your browser; no server or external scripts are required.

## Quick start

The new utility uses Python 3.10+ and the standard library. The examples are synthetic. GPU packages are not required for the new utility or its tests.

```bash
python3 evidence_atlas.py --claims examples/claims.jsonl --corpus examples/corpus.jsonl --predictions examples/predictions.jsonl --output report.html
python3 -m unittest discover -s tests -v
```

## Scope and limitations

This does not extract claims, run inference, or prove that studies contradict each other. Mixed model labels need human review of experimental context. Upstream code, models, claims and abstract data have separate terms; see LICENSE.md and UPSTREAM_README.md.

## Licensing

The new `evidence_atlas.py`, its tests, synthetic examples, CI workflow and this README are MIT licensed in ADDITIONS_LICENSE. Upstream files retain their existing notices and terms; the new license does not relicense them.
