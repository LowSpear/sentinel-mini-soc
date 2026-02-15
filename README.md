\# Sentinel



A lightweight, cross-platform log scanner that detects suspicious patterns using simple rules.

\- Multi-language (first run asks language and remembers it via config.json)

\- Scans .log/.txt files from a folder

\- Generates terminal report and optional JSON



\## Run

```bash

python -m sentinel.cli



Scan a folder:



python -m sentinel.cli --path sample\_logs



Export JSON:



python -m sentinel.cli --path sample\_logs --json report.json

