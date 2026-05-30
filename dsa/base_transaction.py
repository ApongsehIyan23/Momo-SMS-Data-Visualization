from fileinput import filename
import json


class Transaction:

    # class variable: shared list of all extracted transaction dictionaries
    transactions = []

    # class variable: auto-incrementing transaction id
    transaction_id = 0

    # class variable: counters for each category
    counters = {
        "Payment": 0,
        "Transfer": 0,
        "Bank Deposit": 0,
        "Incoming Money": 0,
        "Airtime/Bill Payment": 0,
        "Third-Party Service": 0,
        "Withdrawal": 0,
        "Bank Transfer": 0,
        "Reversal": 0,
        "Failed": 0,
        "Skipped": 0
    }

    def __init__(self, original_transaction_id, category, amount, fee, balance_after,
                 transaction_date, status, sender, receiver, raw_sms):
        
        Transaction.transaction_id += 1

        self.transaction_id = Transaction.transaction_id
        self.original_transaction_id = original_transaction_id
        self.category = category
        self.amount = amount
        self.fee = fee
        self.balance_after = balance_after
        self.transaction_date = transaction_date
        self.status = status
        self.sender = sender
        self.receiver = receiver
        self.raw_sms = raw_sms

    @staticmethod
    def clean_amount(amount_str):
        """helper function to clean amount strings: '1,000' -> 1000"""
        if amount_str is None:
            return None
        return int(amount_str.replace(',', ''))

    def to_dict(self):
        """converts the transaction instance into a dictionary and appends it to the class-level transactions list"""
        transaction_dict = {
            "transaction_id": self.transaction_id,
            "original_transaction_id": self.original_transaction_id,
            "category": self.category,
            "amount": self.amount,
            "fee": self.fee,
            "balance_after": self.balance_after,
            "transaction_date": self.transaction_date,
            "status": self.status,
            "sender": self.sender,
            "receiver": self.receiver,
            "raw_sms": self.raw_sms
        }
        Transaction.transactions.append(transaction_dict)
        return transaction_dict

    @classmethod
    def print_summary(cls):
        """prints the summary of all extracted transactions"""
        print("\n========================================")
        print("Transaction categories and their counts:")
        print("========================================")
        for category, count in cls.counters.items():
            print(f"{category + ':':<22}{count}")
        print(f"========================================")
        print(f"Total extracted:      {len(cls.transactions)}")

    @classmethod
    def save_to_json(cls, filename='data/processed/transactions.json'):
        with open(filename, 'w') as f:
            json.dump(cls.transactions, f, indent=4)
        print(f"\nTransactions saved to {filename}")