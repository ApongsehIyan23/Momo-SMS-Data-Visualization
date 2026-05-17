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