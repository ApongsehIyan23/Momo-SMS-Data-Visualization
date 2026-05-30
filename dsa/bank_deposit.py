import re
from .base_transaction import Transaction


class BankDepositTransaction(Transaction):

    def __init__(self, amount, balance_after, transaction_date, raw_sms):
        super().__init__(
            original_transaction_id=None,
            category="Bank Deposit",
            amount=amount,
            fee=None,
            balance_after=balance_after,
            transaction_date=transaction_date,
            status="Success",
            sender=None,
            receiver="Abebe Chala CHEBUDIE",
            raw_sms=raw_sms
        )

    @classmethod
    def extract(cls, sms):
        amount_match = re.search(r'deposit of ([\d,]+) RWF', sms)
        date_match = re.search(r'at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', sms)
        balance_match = re.search(r'BALANCE :([\d,]+) RWF', sms)

        tx = cls(
            amount=cls.clean_amount(amount_match.group(1)) if amount_match else None,
            balance_after=cls.clean_amount(balance_match.group(1)) if balance_match else None,
            transaction_date=date_match.group(1) if date_match else None,
            raw_sms=sms
        )
        tx.to_dict()
        Transaction.counters["Bank Deposit"] += 1