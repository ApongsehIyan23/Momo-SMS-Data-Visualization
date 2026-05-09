#!/bin/bash

# Create directories
mkdir -p web/assets
mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/logs/dead_letter
mkdir -p etl
mkdir -p api
mkdir -p scripts
mkdir -p tests

# Root level files
touch README.md
touch .env.example
touch requirements.txt
touch index.html

# web/
touch web/styles.css
touch web/chart_handler.js

# data/
touch data/raw/momo.xml
touch data/processed/dashboard.json
touch data/db.sqlite3
touch data/logs/etl.log

# etl/
touch etl/__init__.py
touch etl/config.py
touch etl/parse_xml.py
touch etl/clean_normalize.py
touch etl/categorize.py
touch etl/load_db.py
touch etl/run.py

# api/
touch api/__init__.py
touch api/app.py
touch api/db.py
touch api/schemas.py

# scripts/
touch scripts/run_etl.sh
touch scripts/export_json.sh
touch scripts/serve_frontend.sh

# tests/
touch tests/test_parse_xml.py
touch tests/test_clean_normalize.py
touch tests/test_categorize.py

# Make everything executable
chmod -R +x .

echo "Project structure created successfully!"