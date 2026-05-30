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

## REST API

### Overview
A REST API built in plain Python using http.server that exposes MoMo SMS transaction data through five secured endpoints. All endpoints are protected with Basic Authentication.

### API Files
- API server: `api/server.py`
- API documentation: `docs/api_docs.md`
- Full API report: `docs/Week3_Report.pdf`

### Running the API

**Step 1 — Parse the XML file and generate transaction data:**
```bash
python dsa/main.py
```
This reads `data/raw/modified_sms_v2.xml` and saves the parsed 
transactions to `data/processed/transactions.json`.

**Step 2 — Start the API server:**
```bash
python api/server.py
```
The API will be running at `http://localhost:8080`

**Step 3 — Test the API using curl:**
```bash
curl -u admin:MomoSms26 http://localhost:8080/transactions
```

### Authentication
All endpoints require Basic Authentication.
Username: admin
Password: MomoSms26

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /transactions | Returns all transactions |
| GET | /transactions/{id} | Returns one transaction by ID |
| POST | /transactions | Adds a new transaction |
| PUT | /transactions/{id} | Updates an existing transaction |
| DELETE | /transactions/{id} | Deletes a transaction |

### DSA Integration
Two search algorithms were implemented and compared in `dsa/search_comparison.py`:

- **Linear Search O(n)** — scans through transactions one by one
- **Dictionary Lookup O(1)** — jumps directly to transaction by ID

Dictionary lookup was consistently faster especially for large datasets. Full comparison results are available in `docs/Week3_Report.pdf`.

---

## Project Structure
## Project Structure
```
.
├── README.md
├── .env.example
├── requirements.txt
├── index.html
├── docs/
│   ├── erd_diagram.png
|   ├── AI_usage_log.md
│   ├── api_docs.md
│   ├── Database_Design_Document.pdf
│   └── Week3_Report.pdf
├── database/
│   └── database_setup.sql
├── examples/
│   └── json_schemas.json
├── api/
│   └── server.py
├── dsa/
│   ├── __init__.py
│   ├── main.py
│   ├── base_transaction.py
│   ├── payment.py
│   ├── transfer.py
│   ├── bank_deposit.py
│   ├── incoming_money.py
│   ├── airtime_bill.py
│   ├── third_party.py
│   ├── withdrawal.py
│   ├── bank_transfer.py
│   ├── reversal.py
│   └── search_comparison.py
├── screenshots/
│   ├── 01_get_all_transactions.png
│   ├── 02_unauthorized_401.png
│   ├── 03_get_one_transaction.png
│   ├── 04_post_new_transaction.png
│   ├── 05_put_update_transaction.png
│   └── 06_delete_transaction.png
├── data/
│   ├── raw/
│   │   └── modified_sms_v2.xml
│   └── processed/
│       ├── dashboard.json
│       └── transactions.json
├── web/
│   ├── styles.css
│   ├── chart_handler.js
│   └── assets/
├── etl/
│   ├── __init__.py
│   ├── config.py
│   ├── parse_xml.py
│   ├── clean_normalize.py
│   ├── categorize.py
│   ├── load_db.py
│   └── run.py
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