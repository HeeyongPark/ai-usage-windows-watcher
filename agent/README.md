# Agent Bootstrap

## Setup
```bash
cd /Users/mirador/Documents/ai-usage-windows-watcher/agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Initialize DB
```bash
python src/cli.py init-db
```

## Insert Sample Session
```bash
python src/cli.py record-sample --tool codex --requests 5 --tokens 2400
```

## Daily Summary
```bash
python src/cli.py summary --daily
```

