import re
from .base_transaction import Transaction


class IncomingMoneyTransaction(Transaction):

    def __init__(self, original_transaction_id, amount, balance_after,
                 transaction_date, sender, raw_sms):
        super().__init__(
            original_transaction_id=original_transaction_id,
            category="Incoming Money",
            amount=amount,
            fee=None,
            balance_after=balance_after,
            transaction_date=transaction_date,
            status="Success",
            sender=sender,
            receiver="Abebe Chala CHEBUDIE",
            raw_sms=raw_sms
        )

    @classmethod
    def extract(cls, sms):
        amount_match = re.search(r'received ([\d,]+) RWF', sms)
        sender_match = re.search(r'from (.+?) \(\*+\d+\)', sms)
        date_match = re.search(r'at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', sms)
        balance_match = re.search(r'new balance:([\d,]+) RWF', sms)
        txid_match = re.search(r'Financial Transaction Id: (\d+)', sms)

        tx = cls(
            original_transaction_id=txid_match.group(1) if txid_match else None,
            amount=cls.clean_amount(amount_match.group(1)) if amount_match else None,
            balance_after=cls.clean_amount(balance_match.group(1)) if balance_match else None,
            transaction_date=date_match.group(1) if date_match else None,
            sender=sender_match.group(1).strip() if sender_match else None,
            raw_sms=sms
        )
        tx.to_dict()
        Transaction.counters["Incoming Money"] += 1