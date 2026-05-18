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

## Database Design

### Overview
The database is built on SQLite and consists of five tables designed from analyzing 1,691 real MoMo SMS transaction records. The schema was normalized to 3NF to eliminate redundancy while maintaining practical usability.

### Entity Relationship Diagram (ERD)
The full ERD diagram is available in the repository at `docs/erd_diagram.png`.

### Tables

**Users** — Stores all parties involved in transactions including individuals, agents, businesses, and services. Each user is identified by an auto-generated user_id since phone numbers in the dataset are shared across multiple people and cannot serve as reliable identifiers.

**Transaction_Categories** — A reference table holding nine transaction types: Payment, Transfer, Bank Deposit, Incoming Money, Airtime/Bill Payment, Third-Party Service, Withdrawal, Bank Transfer, and Reversal. Each category is identified by specific keywords or prefix codes in the SMS body.

**Transactions** — The main table storing each processed MoMo SMS transaction. Uses an auto-generated primary key because approximately 50% of transactions (all transfers and bank deposits) have no MoMo-issued ID. The original MoMo ID is preserved in a nullable column when available.

**Transaction_Parties** — A junction table resolving the many-to-many relationship between Users and Transactions. Each record captures one user's role (Sender, Receiver, or Agent) in a specific transaction. This design handles variable participant counts across different transaction types.

**System_Logs** — A standalone table with no foreign key relationships that tracks ETL pipeline activity for debugging and auditing.

### Relationships
- Transaction_Categories (1) to Transactions (M) — one category has many transactions
- Users (M) to Transactions (M) via Transaction_Parties — many-to-many resolved through junction table
- System_Logs — standalone, no relationships

### Key Design Decisions
- Phone numbers were excluded from the Users table after discovering they are shared across multiple people in the dataset
- The Transactions table uses auto-generated IDs because 50% of SMS records contain no MoMo transaction ID
- The message and sms_date columns were removed during normalization since message fields were consistently empty and sms_date was always a fixed timezone offset from transaction_date
- Direction and service_code were removed from Transaction_Categories as both violated 3NF by being fully determined by category_name
- Failed transactions are categorized by their intended type (e.g., Third-Party Service) with status set to Failed, rather than having a separate Failed category

### Database Files
- ERD diagram: `docs/erd_diagram.png`
- SQL setup script: `database/database_setup.sql`
- JSON schema examples: `examples/json_schemas.json`
- Full design document: `docs/Database_Design_Document.pdf`

## Project Structure
```
.
├── README.md
├── .env.example
├── requirements.txt
├── index.html
├── docs/
│   ├── erd_diagram.png
│   └── Database_Design_Document.pdf
├── database/
│   └── database_setup.sql
├── examples/
│   └── json_schemas.json
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