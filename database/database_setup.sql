-- MoMo SMS Data Processing System
-- Database Setup Script
-- Team:3
-- Members: Henriette Iraguha
--          Luigi Birasa Ntore
--           Apongseh Foghang


CREATE DATABASE IF NOT EXISTS momo_sms_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE momo_sms_db;


--  the Users

CREATE TABLE Users (

    user_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT
        COMMENT 'Unique identifier for each user',

    full_name VARCHAR(100) NOT NULL
        COMMENT 'Full name of the user as extracted from SMS',

    user_type VARCHAR(20) NOT NULL
        COMMENT 'Type of user: Individual, Agent, Service or Business',


    CONSTRAINT chk_user_type
        CHECK (user_type IN ('Individual', 'Agent', 'Service', 'Business'))


);


CREATE TABLE  Transaction_Categories (

    category_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT
        COMMENT 'Unique identifier for each transaction category',

    category_name VARCHAR(50) NOT NULL UNIQUE
        COMMENT 'Name of the category: Payment, Transfer, Bank Deposit etc',

    description TEXT NULL
        COMMENT 'Brief explanation of what this category represents'
);



CREATE TABLE  Transactions (

    transaction_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT
        COMMENT 'Internal unique identifier for each transaction',

    original_transaction_id VARCHAR(50) NULL UNIQUE
        COMMENT 'Original transaction ID from MoMo SMS e.g TxId: 73214484437',

    category_id INT UNSIGNED NOT NULL
        COMMENT 'Foreign Key linking to transaction category',

    amount DECIMAL(15,2) NOT NULL
        COMMENT 'Transaction amount in Rwandan Francs',

    fee DECIMAL(10,2) NOT NULL DEFAULT 0.00
        COMMENT 'Fee charged for the transaction. 0 if no fee',

    balance_after DECIMAL(15,2) NOT NULL
        COMMENT 'Account balance after transaction was completed',

    transaction_date DATETIME NOT NULL
        COMMENT 'Date and time when transaction occurred',

    status VARCHAR(10) NOT NULL
        COMMENT 'Transaction status: Success or Failed',

    raw_sms TEXT NOT NULL
        COMMENT 'Complete original SMS body for reference and auditing',


    CONSTRAINT fk_category
        FOREIGN KEY (category_id)
        REFERENCES Transaction_Categories(category_id)
        ON UPDATE CASCADE,

    CONSTRAINT chk_status
        CHECK (status IN ('Success', 'Failed')),

    CONSTRAINT chk_amount_positive
        CHECK (amount > 0),

    CONSTRAINT chk_fee_non_negative
        CHECK (fee >= 0),

    CONSTRAINT chk_balance_non_negative
        CHECK (balance_after >= 0)

);

CREATE TABLE Transaction_Parties (

    party_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT
        COMMENT 'Unique identifier for each party record',

    transaction_id INT UNSIGNED NOT NULL
        COMMENT 'Foreign key linking to the transaction',

    user_id INT UNSIGNED NOT NULL
        COMMENT 'Foreign key linking to the user involved',

    role VARCHAR(20) NOT NULL
        COMMENT 'Role of the user in the transaction: Sender, Receiver or Agent',


    CONSTRAINT fk_party_transaction
        FOREIGN KEY (transaction_id)
        REFERENCES Transactions(transaction_id)
        ON DELETE CASCADE ON UPDATE CASCADE,

    CONSTRAINT fk_party_user
        FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON UPDATE CASCADE,

    CONSTRAINT chk_role
        CHECK (role IN ('Sender', 'Receiver', 'Agent')),

    CONSTRAINT uq_transaction_role
        UNIQUE (transaction_id, role)

);


CREATE TABLE  System_Logs (

    log_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT
        COMMENT 'Unique identifier for each log entry',

    log_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        COMMENT 'Timestamp when the log entry was created',

    log_level VARCHAR(10) NOT NULL
        COMMENT 'Severity level: INFO, WARNING or ERROR',

    etl_stage VARCHAR(20) NOT NULL
        COMMENT 'Pipeline stage: Extract, Transform, Load or Export',

    message TEXT NOT NULL
        COMMENT 'Human readable description of what happened',

    CONSTRAINT chk_log_level
        CHECK (log_level IN ('INFO', 'WARNING', 'ERROR')),

    CONSTRAINT chk_etl_stage
        CHECK (etl_stage IN ('Extract', 'Transform', 'Load', 'Export'))

);

-- indexex of all the tables 

CREATE INDEX idx_users_full_name
    ON Users(full_name);

CREATE INDEX idx_users_type
    ON Users(user_type);

CREATE INDEX idx_transactions_date
    ON Transactions(transaction_date);

CREATE INDEX idx_transaction_category
    ON Transactions(category_id);

CREATE INDEX idx_transactions_status
    ON Transactions(status);

CREATE INDEX idx_transactions_amount
    ON Transactions(amount);

CREATE INDEX idx_original_txid
    ON Transactions(original_transaction_id);

CREATE INDEX idx_party_transaction
    ON Transaction_Parties(transaction_id);

CREATE INDEX idx_party_user
    ON Transaction_Parties(user_id);

CREATE INDEX idx_party_role
    ON Transaction_Parties(role);

CREATE INDEX idx_logs_level
    ON System_Logs(log_level);

CREATE INDEX idx_logs_stage
    ON System_Logs(etl_stage);

CREATE INDEX idx_logs_date
    ON System_Logs(log_date);



-- Real users extracted from XML file

INSERT INTO Users (full_name, user_type) VALUES
('Jane Smith', 'Individual'),
('Samuel Carter', 'Individual'),
('Alex Doe',  'Individual'),
('Robert Brown', 'Individual'),
('Linda Green',  'Individual'),
('MTN Mobile Money', 'Service'),
('Agent Sophia',  'Agent'),
('Abebe Chala CHEBUDIE', 'Individual'),
('DIRECT PAYMENT LTD',  'Business');


INSERT INTO Transaction_Categories
(category_name, description) VALUES
(
    'Payment',
    'Merchant or person payment made using a MoMo pay code.'  
),
(
    'Transfer',
    'Person-to-person money transfer to another MoMo user.'
),
(
    'Bank Deposit',
    'Money deposited from a bank account into the MoMo wallet.'
),
(
    'Incoming Money',
    'Money received from another MoMo user. Identified by You have received at the start of the SMS body.'  
),
(
    'Airtime/Bill Payment',
    'Payment for airtime, data bundles, or utilities such as MTN Cash Power, WASAC, and Bundles and Packs.' 
),
(
    'Third-Party Service',
    'Transaction initiated by a third-party company debiting the MoMo account.'
),
(
    'Withdrawal',
    'Cash withdrawal from MoMo account through a physical agent.'  
),
(
    'Bank Transfer',
    'Money transferred from MoMo wallet to a bank account.'
),
(
    'Reversal',
    'A previously completed transaction that has been reversed and money returned.'
);


-- Real transactions from XML file

INSERT INTO Transactions (
    original_transaction_id,
    category_id,
    amount,
    fee,
    balance_after,
    transaction_date,
    status,
    raw_sms
) VALUES
(
    '76662021700',
    4,
    2000.00,
    0.00,
    2000.00,
    '2024-05-10 16:30:51',
    'Success',
    'You have received 2000 RWF from Jane Smith on your mobile money account'
),
(
    '73214484437',
    1,
    1000.00,
    0.00,
    1000.00,
    '2024-05-10 16:31:39',
    'Success',
    'Your payment of 1,000 RWF to Jane Smith 12845 has been completed'
),
(
    '51732411227',
    1,
    600.00,
    0.00,
    400.00,
    '2024-05-10 21:32:32',
    'Success',
    'Your payment of 600 RWF to Samuel Carter 95464 has been completed'
),
(
    'BANK_DEP_001',
    3,
    40000.00,
    0.00,
    40400.00,
    '2024-05-11 18:43:49',
    'Success',
    'A bank deposit of 40000 RWF has been added to your mobile money account'
),
(
    '13913173274',
    5,
    2000.00,
    0.00,
    25280.00,
    '2024-05-12 11:41:28',
    'Success',
    'Your payment of 2000 RWF to Airtime with token has been completed'
),
(
    '17818959211',
    1,
    2000.00,
    0.00,
    38400.00,
    '2024-05-11 18:48:42',
    'Success',
    'Your payment of 2,000 RWF to Samuel Carter 14965 has been completed'
),
(
    'MOB_TRF_001',
    2,
    10000.00,
    100.00,
    28300.00,
    '2024-05-11 20:34:47',
    'Success',
    '10000 RWF transferred to Samuel Carter from 36521838'
),
(
    '45434420466',
    1,
    10900.00,
    0.00,
    14380.00,
    '2024-05-12 13:26:13',
    'Success',
    'Your payment of 10,900 RWF to Jane Smith 59543 has been completed'
),
(
    '17006777609',
    7,
    50000.00,
    1100.00,
    2401.00,
    '2024-11-23 13:23:44',
    'Success',
    'You have via agent: Agent Sophia withdrawn 50000 RWF from your mobile money account'
),
(
    '82113964658',
    1,
    3500.00,
    0.00,
    10880.00,
    '2024-05-12 13:34:25',
    'Success',
    'Your payment of 3,500 RWF to Alex Doe 43810 has been completed'
);

-- Links users to transactions with roles

INSERT INTO Transaction_Parties
(transaction_id, user_id, role) VALUES
(1,  1, 'Sender'),
(1,  8, 'Receiver'),
(2,  8, 'Sender'),
(2,  1, 'Receiver'),
(3,  8, 'Sender'),
(3,  2, 'Receiver'),
(4,  6, 'Sender'),
(4,  8, 'Receiver'),
(5,  8, 'Sender'),
(5,  6, 'Receiver'),
(6,  8, 'Sender'),
(6,  2, 'Receiver'),
(7,  8, 'Sender'),
(7,  2, 'Receiver'),
(8,  8, 'Sender'),
(8,  1, 'Receiver'),
(9,  8, 'Sender'),
(9,  7, 'Agent'),
(10, 8, 'Sender'),
(10, 3, 'Receiver');


-- ETL pipeline processing events

INSERT INTO System_Logs
(log_level, etl_stage, message) VALUES
(
    'INFO',
    'Extract',
    'Pipeline started for modified_sms_v2.xml'
),
(
    'INFO',
    'Extract',
    'Parsed 1691 SMS records from modified_sms_v2.xml'
),
(
    'WARNING',
    'Transform',
    'Skipped OTP message: Dear Customer, your MTN MoMo application one-time password is...'
),
(
    'WARNING',
    'Transform',
    'Skipped Yello! notification: Yello!Umaze kugura 2000Rwf(1GB)/30days igura 2,000 RWF'
),
(
    'INFO',
    'Transform',
    'Categorized 1661 transactions: 662 payments, 585 transfers, 248 bank deposits, 63 incoming, 53 airtime, 36 third-party, 3 withdrawals, 6 bank transfers, 1 reversal'
),
(
    'ERROR',
    'Transform',
    'Could not parse amount from SMS: 1) 2024-08-23 DEPOSIT RWF 25000 Receiver: 250795963036 Sender: Fee: RWF'
),
(
    'INFO',
    'Load',
    'Inserted 1661 transactions into database'
),
(
    'INFO',
    'Export',
    'dashboard.json exported successfully with summary statistics'
);

-- VIEW: Complete transaction details

CREATE VIEW vw_transaction_details AS
SELECT
    t.transaction_id,
    t.original_transaction_id,
    tc.category_name,
    t.amount,
    t.fee,
    t.balance_after,
    t.transaction_date,
    t.status,
    sender.full_name   AS sender_name,
    receiver.full_name AS receiver_name
FROM Transactions t
JOIN Transaction_Categories tc
    ON t.category_id = tc.category_id
LEFT JOIN Transaction_Parties tp_s
    ON t.transaction_id = tp_s.transaction_id
    AND tp_s.role = 'Sender'
LEFT JOIN Users sender
    ON tp_s.user_id = sender.user_id
LEFT JOIN Transaction_Parties tp_r
    ON t.transaction_id = tp_r.transaction_id
    AND tp_r.role = 'Receiver'
LEFT JOIN Users receiver
    ON tp_r.user_id = receiver.user_id;

-- VIEW: Transaction summary by category

CREATE VIEW vw_category_summary AS
SELECT
    tc.category_name,
    COUNT(t.transaction_id)  AS num_transactions,
    SUM(t.amount)            AS total_amount_rwf,
    SUM(t.fee)               AS total_fees_rwf
FROM Transactions t
JOIN Transaction_Categories tc
    ON t.category_id = tc.category_id
GROUP BY tc.category_id, tc.category_name
ORDER BY total_amount_rwf DESC;

--CRUD OPS
-- CREATE: Insert a new test user

INSERT INTO Users (full_name, user_type) VALUES
('Emily Johnson', 'Individual');


SELECT * FROM Users WHERE full_name = 'Emily Johnson';

-- READ 1: All users
SELECT * FROM Users;

-- READ 2: All transactions by date

SELECT
    t.original_transaction_id,
    tc.category_name,
    t.amount,
    t.fee,
    t.balance_after,
    t.transaction_date,
    t.status
FROM Transactions t
JOIN Transaction_Categories tc
    ON t.category_id = tc.category_id
ORDER BY t.transaction_date ASC;

-- READ 3: Successful transactions only
SELECT
    original_transaction_id,
    amount,
    fee,
    balance_after,
    transaction_date
FROM Transactions
WHERE status = 'Success'
ORDER BY transaction_date ASC;

-- READ 4: Transactions above 5000 RWF
SELECT
    original_transaction_id,
    amount,
    fee,
    balance_after,
    transaction_date
FROM Transactions
WHERE amount > 5000
ORDER BY amount DESC;


SELECT * FROM vw_transaction_details
ORDER BY transaction_date ASC;

-- READ 6: Category summary via view

SELECT * FROM vw_category_summary;

-- READ 7: Row count across all tables

SELECT 'Users' AS table_name,
    COUNT(*) AS row_count FROM Users
UNION ALL
SELECT 'Transaction_Categories',
    COUNT(*) FROM Transaction_Categories
UNION ALL
SELECT 'Transactions',
    COUNT(*) FROM Transactions
UNION ALL
SELECT 'Transaction_Parties',
    COUNT(*) FROM Transaction_Parties
UNION ALL
SELECT 'System_Logs',
    COUNT(*) FROM System_Logs;

-- UPDATE 1: Change transaction status
UPDATE Transactions
SET status = 'Failed'
WHERE original_transaction_id = '82113964658';

-- Verify
SELECT original_transaction_id, status
FROM Transactions
WHERE original_transaction_id = '82113964658';

-- Restore
UPDATE Transactions
SET status = 'Success'
WHERE original_transaction_id = '82113964658';

--change type of the user
UPDATE Users
SET user_type = 'Agent'
WHERE full_name = 'Emily Johnson';

-- Verify
SELECT user_id, full_name, user_type
FROM Users
WHERE full_name = 'Emily Johnson';

-- DELETE: Remove old error logs
DELETE FROM System_Logs
WHERE log_level = 'ERROR'
AND log_date < NOW() - INTERVAL 30 DAY;

-- Verify remaining logs
SELECT log_id, log_level, etl_stage, message
FROM System_Logs
ORDER BY log_date ASC;

-- DELETE: Remove test user
DELETE FROM Users
WHERE full_name = 'Emily Johnson';

-- Verify
SELECT * FROM Users;

-- INSERT: Manual audit log entry
INSERT INTO System_Logs
(log_level, etl_stage, message)
VALUES
(
    'INFO',
    'Load',
    'Manual audit: transaction 76662021700 re-verified by admin'
);
