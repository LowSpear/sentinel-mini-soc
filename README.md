A lightweight, cross-platform log scanner that detects suspicious patterns using simple rules.

\- Multi-language (first run asks language and remembers it via config.json)

\- Scans .log/.txt files from a folder

\- Generates terminal report and optional JSON



\## Run

```bash

python -m sentinel.cli


Export JSON:


BASIC COMMANDS:

python -m sentinel.cli --path sample\_logs --json report.json

python -m sentinel.cli --path sample_logs


If you want to set the language:


python -m sentinel.cli --path sample_logs --set-lang


If you want to change the threshold:


python -m sentinel.cli --path sample_logs --bf 7 --admin 4

