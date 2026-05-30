import re
from .base_transaction import Transaction


class AirtimeBillTransaction(Transaction):

    def __init__(self, original_transaction_id, amount, fee, balance_after,
                 transaction_date, status, receiver, raw_sms):
        super().__init__(
            original_transaction_id=original_transaction_id,
            category="Airtime/Bill Payment",
            amount=amount,
            fee=fee,
            balance_after=balance_after,
            transaction_date=transaction_date,
            status=status,
            sender="Abebe Chala CHEBUDIE",
            receiver=receiver,
            raw_sms=raw_sms
        )

    @classmethod
    def extract(cls, sms):
        txid_match = re.search(r'TxId:(\d+)', sms)
        amount_match = re.search(r'payment of ([\d,]+) RWF', sms)
        receiver_match = re.search(r'to (.+?) with token', sms)
        date_match = re.search(r'completed at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', sms)
        fee_match = re.search(r'Fee was ([\d,]+) RWF', sms)
        balance_match = re.search(r'new balance: ([\d,]+) RWF', sms)

        tx = cls(
            original_transaction_id=txid_match.group(1) if txid_match else None,
            amount=cls.clean_amount(amount_match.group(1)) if amount_match else None,
            fee=cls.clean_amount(fee_match.group(1)) if fee_match else None,
            balance_after=cls.clean_amount(balance_match.group(1)) if balance_match else None,
            transaction_date=date_match.group(1) if date_match else None,
            status="Success",
            receiver=receiver_match.group(1).strip() if receiver_match else None,
            raw_sms=sms
        )
        tx.to_dict()
        Transaction.counters["Airtime/Bill Payment"] += 1

    @classmethod
    def extract_failed(cls, sms):
        """handles failed airtime/bill payment format: *143*TxId:XXXXX*S*Your payment of... has failed"""
        txid_match = re.search(r'TxId:(\d+)', sms)
        amount_match = re.search(r'payment of ([\d,]+) RWF', sms)
        receiver_match = re.search(r'to (.+?) with token', sms)
        date_match = re.search(r'failed at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', sms)

        tx = cls(
            original_transaction_id=txid_match.group(1) if txid_match else None,
            amount=cls.clean_amount(amount_match.group(1)) if amount_match else None,
            fee=None,
            balance_after=None,
            transaction_date=date_match.group(1) if date_match else None,
            status="Failed",
            receiver=receiver_match.group(1).strip() if receiver_match else None,
            raw_sms=sms
        )
        tx.to_dict()
        Transaction.counters["Failed"] += 1