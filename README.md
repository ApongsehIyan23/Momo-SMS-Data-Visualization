# Momo SMS Data Visualization

## Team Name: Execution Trio

## Project Description
An enterprise-level fullstack application that processes MoMo (Mobile Money) SMS data in XML format. The system cleans, categorizes, and stores transaction data in a SQLite relational database, then visualizes the processed data through an interactive web dashboard featuring charts, tables, and summary statistics.

### How It Works
1. **Extract** — Parse MoMo SMS transaction data from XML files.
2. **Transform** — Clean, normalize, and categorize each transaction.
3. **Load** — Store the processed data in a SQLite database.
4. **Export** — Generate a JSON summary from the database for the frontend.
5. **Visualize** — Display interactive charts and tables on a web dashboard.

## Team Members

| Name               | Role        |
|--------------------|-------------|
| Luigi Birasa Ntore | Developer   |
| Henriette Iraguha  | Developer   |
| Apongseh Foghang   | Developer   |

## Architecture Diagram
Our high-level system architecture diagram can be found here:

🔗 [View Architecture Diagram on Miro](https://miro.com/app/board/uXjVHW93BGg=/?share_link_id=977839675202)

## Scrum Board
Our project tasks are tracked using GitHub Projects:

🔗 [View Scrum Board](https://github.com/users/ApongsehIyan23/projects/4)

## Project Structure
```
.
├── README.md
├── .env.example
├── requirements.txt
├── index.html
├── web/
│   ├── styles.css
│   ├── chart_handler.js
│   └── assets/
├── data/
│   ├── raw/
│   │   └── momo.xml
│   ├── processed/
│   │   └── dashboard.json
│   ├── db.sqlite3
│   └── logs/
│       ├── etl.log
│       └── dead_letter/
├── etl/
│   ├── __init__.py
│   ├── config.py
│   ├── parse_xml.py
│   ├── clean_normalize.py
│   ├── categorize.py
│   ├── load_db.py
│   └── run.py
├── api/
│   ├── __init__.py
│   ├── app.py
│   ├── db.py
│   └── schemas.py
├── scripts/
│   ├── run_etl.sh
│   ├── export_json.sh
│   └── serve_frontend.sh
└── tests/
    ├── test_parse_xml.py
    ├── test_clean_normalize.py
    └── test_categorize.py
```

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation
```bash
git clone https://github.com/ApongsehIyan23/Momo-SMS-Data-Visualization.git
cd Momo-SMS-Data-Visualization
pip install -r requirements.txt
```

### Running the ETL Pipeline
```bash
python etl/run.py --xml data/raw/momo.xml
```

### Starting the Dashboard
```bash
python -m http.server 8000
```
Then open `http://localhost:8000/index.html` in your browser.
