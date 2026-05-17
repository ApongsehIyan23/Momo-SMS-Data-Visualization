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
