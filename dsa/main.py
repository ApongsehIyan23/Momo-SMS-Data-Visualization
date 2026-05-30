"""
    Algorithm for extracting transaction details from sms messages
    target transaction details: trans_type, amount, sender, receiever, timestamp

    1. Iterate throught each transaction in the transactions list
    2. For each transaction, identify the category
    3. Based on the category, use regex patterns to extract the required details
    4. Add to a json and store in the json object of transactions

"""

import xml.etree.ElementTree as ET
import sys
import os

# add the parent directory to the path so we can import the etl package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsa import (
    Transaction,
    PaymentTransaction,
    TransferTransaction,
    BankDepositTransaction,
    IncomingMoneyTransaction,
    AirtimeBillTransaction,
    ThirdPartyTransaction,
    WithdrawalTransaction,
    BankTransferTransaction,
    ReversalTransaction
)


# Parse the XML file
tree = ET.parse('data/raw/modified_sms_v2.xml')
root = tree.getroot()

# list to store the raw sms messages
sms_messages = []

# Iterate through each SMS element and find all its "body" elements
for sms in root.findall('sms'):
    body = sms.attrib.get('body')
    if body:
        sms_messages.append(body)

print('The length of the sms messages list is: ', len(sms_messages))


# Classify and extract each SMS message
for sms in sms_messages:

    # FAILED TRANSACTIONS: check first because they contain *143* which overlaps with reversal
    if "*143*" in sms and "failed" in sms:

        # Format 1: third-party style failed
        if "the transaction with amount" in sms:
            ThirdPartyTransaction.extract_failed(sms)

        # Format 2: bill payment style failed
        elif "Your payment of" in sms and "has failed" in sms:
            AirtimeBillTransaction.extract_failed(sms)

    # REVERSAL
    elif "*143*" in sms and "has been reversed" in sms:
        ReversalTransaction.extract(sms)

    # AIRTIME/BILL PAYMENT: check before Payment because both contain "Your payment of"
    elif "*162*" in sms and "payment of" in sms:
        AirtimeBillTransaction.extract(sms)

    # PAYMENT
    elif "Your payment of" in sms and "*162*" not in sms:
        PaymentTransaction.extract(sms)

    # TRANSFER
    elif "*165*" in sms and "transferred to" in sms:
        TransferTransaction.extract(sms)

    # BANK DEPOSIT
    elif "*113*" in sms and "bank deposit of" in sms:
        BankDepositTransaction.extract(sms)

    # INCOMING MONEY
    elif sms.startswith("You have received"):
        IncomingMoneyTransaction.extract(sms)

    # THIRD-PARTY SERVICE
    elif "*164*" in sms and "transaction of" in sms:
        ThirdPartyTransaction.extract(sms)

    # WITHDRAWAL
    elif "withdrawn" in sms and "via agent" in sms:
        WithdrawalTransaction.extract(sms)

    # BANK TRANSFER
    elif "imbank.bank" in sms and "You have transferred" in sms:
        BankTransferTransaction.extract(sms)

    # UNCLASSIFIED: OTP messages, Yello! confirmations, unknown formats
    else:
        Transaction.counters["Skipped"] += 1


# Print summary and save
Transaction.print_summary()
print(f"Total SMS messages:   {len(sms_messages)}")
Transaction.save_to_json()