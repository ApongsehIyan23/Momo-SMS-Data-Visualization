import re
from .base_transaction import Transaction


class BankTransferTransaction(Transaction):

    def __init__(self, original_transaction_id, amount, balance_after,
                 transaction_date, receiver, raw_sms):
        super().__init__(
            original_transaction_id=original_transaction_id,
            category="Bank Transfer",
            amount=amount,
            fee=None,
            balance_after=balance_after,
            transaction_date=transaction_date,
            status="Success",
            sender="Abebe Chala CHEBUDIE",
            receiver=receiver,
            raw_sms=raw_sms
        )

    @classmethod
    def extract(cls, sms):
        amount_match = re.search(r'transferred ([\d,]+) RWF', sms)
        receiver_match = re.search(r'to (.+?) \(\d+\)', sms)
        date_match = re.search(r'at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', sms)
        balance_match = re.search(r'new balance: ([\d,]+) RWF', sms)
        txid_match = re.search(r'Financial Transaction Id: (\d+)', sms)

        tx = cls(
            original_transaction_id=txid_match.group(1) if txid_match else None,
            amount=cls.clean_amount(amount_match.group(1)) if amount_match else None,
            balance_after=cls.clean_amount(balance_match.group(1)) if balance_match else None,
            transaction_date=date_match.group(1) if date_match else None,
            receiver=receiver_match.group(1).strip() if receiver_match else None,
            raw_sms=sms
        )
        tx.to_dict()
        Transaction.counters["Bank Transfer"] += 1