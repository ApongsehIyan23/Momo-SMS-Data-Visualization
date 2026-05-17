CREATE TABLE Users (

    user_id INT PRIMARY KEY AUTO_INCREMENT
        COMMENT 'Unique identifier for each user',
    
    full_name VARCHAR(100) NOT NULL
         COMMENT 'Full name of the user as exctracted from SMS',
    
    user_type VARCHAR(20) NOT NULL
         COMMENT 'Type of user:Individual, Agent, Service or Business'

  CONSTRAINT chck_user_type
      CHECK (user_type IN('Individual', 'Agent','Service','Business'))
        
);
 
 CREATE TABLE Transaction_Categories (

    category_id INT PRIMARY KEY AUTO_INCREMENT
        COMMENT 'Unique identifier for each transaction category',

    category_name VARCHAR(50) NOT NULL UNIQUE
        COMMENT 'Name of the category: Payment, Transfer, Bank Deposit, etc.',

    description TEXT NULL
        COMMENT 'Brief explanation of what this category represents'

);

CREATE TABLE Transactions (

    transaction_id INT PRIMARY KEY AUTO_INCREMENT
         COMMENT 'Internal unique identifier for each transaction',
    
    original_transaction_id VARCHAR(50) NULL
         COMMENT 'original transaction ID from MOMO SMS',
    
    category_id INT NOT NULL
        COMMENT 'Foreign Key linking to transaction category',
    
    amount DECIMAL(15,2) NOT NULL
       COMMENT 'Transaction amount in Rwandan francs',
    
    fee DECIMAL(10,2) NULL
        COMMENT 'fee charged for the transaction. 0 if no fee',
    
    balance_after DECIMAL(15,2) NULL
        COMMENT 'Account balance after transaction was completed',
    
    transaction_date DATETIME NOT NULL
        COMMENT 'Date and time when transaction occured',

    status VARCHAR(10) NOT NULL
        COMMENT 'Transaction status: Success or Failed',

    raw_sms TEXT NOT NULL
       COMMENT 'Complete original sms body',
    
    CONSTRAINT fk_category
       FOREIGN KEY (category_id)
       REFERENCES Transaction_categories(category_id),
    
    CONSTRAINT chck_status
       CHECK(status IN ('Success','Failed'))

);


CREATE TABLE Transaction_Parties (

    party_id INT PRIMARY KEY AUTO_INCREMENT
        COMMENT 'Unique identifier for each party record',

    transaction_id INT NOT NULL
        COMMENT 'Foreign key linking to the transaction',

    user_id INT NOT NULL
        COMMENT 'Foreign key linking to the user involved',

    role VARCHAR(20) NOT NULL
        COMMENT 'Role of the user in the transaction: Sender, Receiver or Agent',

    CONSTRAINT fk_party_transaction
        FOREIGN KEY (transaction_id)
        REFERENCES Transactions(transaction_id),

    CONSTRAINT fk_party_user
        FOREIGN KEY (user_id)
        REFERENCES Users(user_id),

    CONSTRAINT chck_role
        CHECK (role IN ('Sender', 'Receiver', 'Agent'))

);


CREATE TABLE System_Logs (

    log_id INT PRIMARY KEY AUTO_INCREMENT
        COMMENT 'Unique identifier for each log entry',

    log_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        COMMENT 'Timestamp when the log entry was created',

    log_level VARCHAR(10) NOT NULL
        COMMENT 'Severity level: INFO, WARNING or ERROR',

    etl_stage VARCHAR(20) NOT NULL
        COMMENT 'Pipeline stage that generated the log: Extract, Transform, Load or Export',

    message TEXT NOT NULL
        COMMENT 'Human readable description of what happened',

    CONSTRAINT chck_log_level
        CHECK (log_level IN ('INFO', 'WARNING', 'ERROR')),

    CONSTRAINT chck_etl_stage
        CHECK (etl_stage IN ('Extract', 'Transform', 'Load', 'Export'))

);

/* 
    Indexes for performance optimization
*/

CREATE INDEX idx_users_full_name
   ON Users(full_name);

CREATE INDEX idx_transactions_date
   ON Transactions(transaction_date);

CREATE INDEX idx_transaction_category
    ON Transactions(category_id);

CREATE INDEX idx_transactions_status
    ON Transactions(status);

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

INSERT INTO Users (full_name, user_type) VALUES
('Jane Smith', 'Individual'),
('Samuel Carter', 'Individual'),
('Alex Doe', 'Individual'),
('Robert Brown', 'Individual'),
('Linda Green', 'Individual'),
('MTN Mobile Money', 'Service'),
('Agent Sophia', 'Agent');



INSERT INTO Transaction_Categories (category_name, description) VALUES
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
    'Incoming Money',
    'Money received from another MoMo user. Identified by "You have received" at the start of the SMS body.'
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