TEAM NAME: Execution Trio
TEAM MEMBERS: Luigi Birasa Ntore
              Henriette Iraguha
              Apongseng Foghang

# MoMo SMS Processing System

A local ETL pipeline that parses MTN MoMo SMS transaction data from XML, cleans and categorizes it, stores it in SQLite, and serves an interactive dashboard via a local HTTP server.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Setup](#setup)
- [Usage](#usage)
- [ETL Pipeline](#etl-pipeline)
- [Storage Layer](#storage-layer)
- [Presentation Layer](#presentation-layer)
- [Error Handling](#error-handling)
- [Configuration](#configuration)

---

## Overview

This system takes a raw MoMo SMS XML export (`momo.xml`), runs it through a Luigi-orchestrated ETL pipeline, stores categorized transactions in a SQLite database, and exposes summary statistics through a browser-based dashboard.

```
momo.xml → ETL Pipeline → SQLite → Export Engine → dashboard.json → Browser Dashboard
```

---

## Project Structure

```
project/
├── data/
│   ├── raw/
│   │   └── momo.xml              # Input: MoMo SMS XML export
│   ├── db/
│   │   └── db.sqlite3            # SQLite database
│   └── processed/
│       └── dashboard.json        # Exported summary stats
├── dead_letter/                  # Unparseable transaction snippets
├── etl.log                       # Pipeline error and warning log
├── config.py                     # Keywords, paths, and settings
├── __init__.py                   # Python package marker
├── parse_xml.py                  # Process 1: Extract
├── clean_normalize.py            # Process 2: Transform (clean)
├── categorize.py                 # Process 3: Transform (categorize)
├── load_db.py                    # Process 4: Load to SQLite
├── run.py                        # Export engine: generates dashboard.json
├── chart_handler.js              # Fetches dashboard.json via HTTP
└── index.html                    # Dashboard: charts and data table
```

---

## Architecture

The system has three layers:

**ETL Pipeline** — orchestrated by Luigi, runs four sequential tasks to move data from raw XML to a structured database.

**Storage Layer** — SQLite holds all categorized transactions; `run.py` reads from it and exports aggregated stats to `dashboard.json`.

**Presentation Layer** — a Python HTTP server (`http.server`) serves `index.html` and `dashboard.json`; `chart_handler.js` fetches the JSON and renders stat cards, bar charts, pie charts, and a data table.

---

## Setup

### Prerequisites

- Python 3.9+
- pip

### Install dependencies

```bash
pip install luigi
```

### Add your data

Place your MoMo SMS XML export file at:

```
data/raw/momo.xml
```

---

## Usage

### 1. Run the ETL pipeline

```bash
python -m luigi --module load_db LoadTask --local-scheduler
```

This runs all four pipeline tasks in sequence: parse → clean → categorize → load.

### 2. Export dashboard data

```bash
python run.py
```

This reads from the SQLite database and writes summary stats to `data/processed/dashboard.json`.

### 3. Serve the dashboard

```bash
python -m http.server 8000
```

Then open your browser at:

```
http://localhost:8000/index.html
```

---

## ETL Pipeline

The pipeline is orchestrated by **Luigi** and runs four tasks in sequence.

### Parse (`parse_xml.py`)

Reads `momo.xml` and extracts the following fields from each `<transaction>` element into a raw Python dictionary:

| Field | Description |
|---|---|
| `id` | Unique transaction ID |
| `date` | Raw date string |
| `amount` | Raw amount string (e.g. `"5,000 RWF"`) |
| `sender` | Raw sender phone number |
| `receiver` | Raw receiver phone number |
| `type` | Transaction type |
| `message` | Original SMS body |

Unparseable transactions are logged to `etl.log` and saved to `dead_letter/` for manual review.

### Clean (`clean_normalize.py`)

Normalizes each raw dictionary:

- Strips currency symbols and commas from amounts (`"5,000 RWF"` → `5000`)
- Standardizes phone numbers to E.164 format (`"0781234567"` → `"+250781234567"`)
- Parses dates to ISO 8601 (`"2025-03-15 14:32:00"`)
- Trims whitespace from all text fields
- Removes duplicate transactions

Missing or invalid values are logged as warnings and either skipped or filled with a default.

### Categorize (`categorize.py`)

Classifies each cleaned transaction into a category using keyword rules defined in `config.py`. Examples:

| Category | Keywords |
|---|---|
| `send_money` | transfer, sent, paid |
| `receive_money` | received, incoming |
| `payment` | merchant, bill, purchase |
| `deposit` | deposited, top-up |
| `withdrawal` | withdrawn, cash out |

### Load (`load_db.py`)

Inserts categorized transactions into the SQLite database at `data/db/db.sqlite3`.

Schema:

```sql
CREATE TABLE transactions (
    id       TEXT PRIMARY KEY,
    date     TEXT,
    amount   REAL,
    sender   TEXT,
    receiver TEXT,
    type     TEXT,
    category TEXT,
    message  TEXT
);
```

---

## Storage Layer

### SQLite Database (`data/db/db.sqlite3`)

Stores all processed transactions. Key columns: `id`, `date`, `amount`, `sender`, `category`.

### Export Engine (`run.py`)

Reads from SQLite and produces `data/processed/dashboard.json` containing:

- **Summary stats** — total transactions, total volume, unique senders
- **Monthly totals** — aggregated spend/receive per month
- **Top senders/receivers** — ranked by transaction count or volume

---

## Presentation Layer

### HTTP Server

Serves static files from the project root on port 8000:

```bash
python -m http.server 8000
```

### `chart_handler.js`

Fetches `dashboard.json` via HTTP and passes data to the chart rendering functions.

### `index.html`

Renders the dashboard with:

- **Stat cards** — key summary numbers
- **Bar chart** — monthly transaction totals
- **Pie chart** — breakdown by category
- **Data table** — paginated transaction list

---

## Error Handling

| Error type | Behaviour |
|---|---|
| Unparseable XML transaction | Logged to `etl.log`, snippet saved to `dead_letter/` |
| Missing or invalid field value | Warning logged to `etl.log`, value skipped or defaulted |
| Luigi task failure | Task reruns cleanly on next invocation (atomic output targets) |

Review errors at any time:

```bash
cat etl.log
ls dead_letter/
```

---

## Configuration

All keywords, file paths, and pipeline settings are defined in `config.py`:

```python
# config.py

RAW_XML     = "data/raw/momo.xml"
DB_PATH     = "data/db/db.sqlite3"
OUTPUT_JSON = "data/processed/dashboard.json"
DEAD_LETTER = "dead_letter/"
LOG_FILE    = "etl.log"

CATEGORY_KEYWORDS = {
    "send_money":    ["transfer", "sent", "paid"],
    "receive_money": ["received", "incoming"],
    "payment":       ["merchant", "bill", "purchase"],
    "deposit":       ["deposited", "top-up"],
    "withdrawal":    ["withdrawn", "cash out"],
}
```

---

## License

MIT
Link for the project: https://github.com/users/ApongsehIyan23/projects/4
