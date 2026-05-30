# MoMo SMS API Documentation

## Project: MoMo SMS Data Visualization
## Team: Execution Trio
## Base URL: http://localhost:8080

---

## Authentication

This API uses Basic Authentication. Every request must include 
a valid username and password encoded in base64.

**How to include credentials:**
curl -u admin:MomoSms26 http://localhost:8080/transactions


**What happens without credentials:**
```json
{
  "error": "Unauthorized. Invalid credentials."
}
```

---

## Endpoints

---

## 1. GET /transactions

Returns all transactions stored in the system.

**Method:** GET  
**Authentication:** Required  
**URL:** http://localhost:8080/transactions

**Request Example:**
```bash
curl -u admin:MomoSms26 http://localhost:8080/transactions
```

**Response Example (200 OK):**
```json
[
  {
    "transaction_id": 1,
    "original_transaction_id": "76662021700",
    "category": "Incoming Money",
    "amount": 2000,
    "fee": 0,
    "balance_after": 2000,
    "transaction_date": "2024-05-10 16:30:51",
    "status": "Success",
    "sender": "Jane Smith",
    "receiver": "Abebe Chala CHEBUDIE",
    "raw_sms": "You have received 2000 RWF from Jane Smith"
  },
  {
    "transaction_id": 2,
    "original_transaction_id": "73214484437",
    "category": "Payment",
    "amount": 1000,
    "fee": 0,
    "balance_after": 1000,
    "transaction_date": "2024-05-10 16:31:39",
    "status": "Success",
    "sender": "Abebe Chala CHEBUDIE",
    "receiver": "Jane Smith",
    "raw_sms": "Your payment of 1,000 RWF to Jane Smith has been completed"
  }
]
```

**Error Codes:**
| Code | Meaning |
|---|---|
| 200 | Success. Returns list of all transactions. |
| 401 | Unauthorized. Invalid or missing credentials. |
| 404 | Endpoint not found. |

---

## 2. GET /transactions/{id}

Returns a single transaction by its ID.

**Method:** GET  
**Authentication:** Required  
**URL:** http://localhost:8080/transactions/{id}

**URL Parameter:**
| Parameter | Type | Description |
|---|---|---|
| id | Integer | The transaction_id of the transaction to retrieve |

**Request Example:**
```bash
curl -u admin:MomoSms26 http://localhost:8080/transactions/1
```

**Response Example (200 OK):**
```json
{
  "transaction_id": 1,
  "original_transaction_id": "76662021700",
  "category": "Incoming Money",
  "amount": 2000,
  "fee": 0,
  "balance_after": 2000,
  "transaction_date": "2024-05-10 16:30:51",
  "status": "Success",
  "sender": "Jane Smith",
  "receiver": "Abebe Chala CHEBUDIE",
  "raw_sms": "You have received 2000 RWF from Jane Smith"
}
```

**Response Example (404 Not Found):**
```json
{
  "error": "Transaction not found"
}
```

**Error Codes:**
| Code | Meaning |
|---|---|
| 200 | Success. Returns the requested transaction. |
| 401 | Unauthorized. Invalid or missing credentials. |
| 404 | Transaction not found. ID does not exist. |

---

## 3. POST /transactions

Adds a new transaction to the system.

**Method:** POST  
**Authentication:** Required  
**URL:** http://localhost:8080/transactions  
**Content-Type:** application/json

**Required Fields:**
| Field | Type | Description |
|---|---|---|
| transaction_id | Integer | Unique ID for the transaction |
| category | String | Transaction type e.g. Payment, Transfer |
| amount | Number | Transaction amount in RWF |
| sender | String | Name of the sender |
| receiver | String | Name of the receiver |
| transaction_date | String | Date and time of transaction |

**Request Example:**
```bash
curl -u admin:MomoSms26 \
  -X POST \
  -H "Content-Type: application/json" \
  -d "{\"transaction_id\":999,\"category\":\"Payment\",\"amount\":5000,\"sender\":\"Account Holder\",\"receiver\":\"Samuel Carter\",\"transaction_date\":\"2024-06-02 10:00:00\",\"fee\":0,\"balance_after\":1000,\"status\":\"Success\",\"raw_sms\":\"Your payment of 5000 RWF to Samuel Carter has been completed\"}" \
  http://localhost:8080/transactions
```

**Response Example (201 Created):**
```json
{
  "transaction_id": 999,
  "category": "Payment",
  "amount": 5000,
  "fee": 0,
  "balance_after": 1000,
  "transaction_date": "2024-06-02 10:00:00",
  "status": "Success",
  "sender": "Account Holder",
  "receiver": "Samuel Carter",
  "raw_sms": "Your payment of 5000 RWF to Samuel Carter has been completed"
}
```

**Response Example (400 Bad Request — Missing Field):**
```json

{
  "error": "Missing required field: amount
}

**Response Example (400 Bad Request — Duplicate ID):**
```json
{
  "error": "Transaction ID already exists"
}
```

**Error Codes:**
| Code | Meaning |
|---|---|
| 201 | Created. New transaction added successfully. |
| 400 | Bad Request. Missing required field or duplicate ID. |
| 401 | Unauthorized. Invalid or missing credentials. |
| 404 | Endpoint not found. |

---

## 4. PUT /transactions/{id}
**Response Example (400 Bad Request — Duplicate ID):**
```json
{
  "error": "Transaction ID already exists"
}
```

**Error Codes:**
| Code | Meaning |
|---|---|
| 201 | Created. New transaction added successfully. |
| 400 | Bad Request. Missing required field or duplicate ID. |
| 401 | Unauthorized. Invalid or missing credentials. |
| 404 | Endpoint not found. |

---

## 4. PUT /transactions/{id}
Updates an existing transaction by its ID.

**Method:** PUT  
**Authentication:** Required  
**URL:** http://localhost:8080/transactions/{id}  
**Content-Type:** application/json

**URL Parameter:**
| Parameter | Type | Description |
|---|---|---|
| id | Integer | The transaction_id of the transaction to update |

**Note:** Only include the fields you want to update. 
All other fields remain unchanged.

**Request Example:**
```bash
curl -u admin:MomoSms26 \
  -X PUT \
  -H "Content-Type: application/json" \
  -d "{\"amount\":9999,\"status\":\"Failed\"}" \
  http://localhost:8080/transactions/1
```

**Response Example (200 OK):**
```json
{
  "transaction_id": 1,
  "original_transaction_id": "76662021700",
  "category": "Incoming Money",
  "amount": 9999,
  "fee": 0,
  "balance_after": 2000,
  "transaction_date": "2024-05-10 16:30:51",
  "status": "Failed",
  "sender": "Jane Smith",
  "receiver": "Abebe Chala CHEBUDIE",
  "raw_sms": "You have received 2000 RWF from Jane Smith"
}
```

**Response Example (404 Not Found):**
```json
{
  "error": "Transaction not found"
}
```

**Error Codes:**
| Code | Meaning |
|---|---|
| 200 | Success. Transaction updated successfully. |
| 401 | Unauthorized. Invalid or missing credentials. |
| 404 | Transaction not found. ID does not exist. |

---

## 5. DELETE /transactions/{id}

Deletes a transaction by its ID.

**Method:** DELETE  
**Authentication:** Required  
**URL:** http://localhost:8080/transactions/{id}

**URL Parameter:**
| Parameter | Type | Description |
|---|---|---|
| id | Integer | The transaction_id of the transaction to delete |

**Request Example:**
```bash
curl -u admin:MomoSms26 \
  -X DELETE \
  http://localhost:8080/transactions/1
```

**Response Example (200 OK):**
```json
{
  "message": "Transaction deleted successfully"
}
```

**Response Example (404 Not Found):**
```json
{
  "error": "Transaction not found"
}
```

**Error Codes:**
| Code | Meaning |
|---|---|
| 200 | Success. Transaction deleted successfully. |
| 401 | Unauthorized. Invalid or missing credentials. |
| 404 | Transaction not found. ID does not exist. |

---

## Error Code Summary

| Code | Meaning |
|---|---|
| 200 | OK. Request successful. |
| 201 | Created. New resource created successfully. |
| 400 | Bad Request. Missing fields or duplicate ID. |
| 401 | Unauthorized. Invalid or missing credentials. |
| 404 | Not Found. Resource or endpoint does not exist. |