from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
import os

json_path = os.path.join(os.path.dirname(__file__), '..', 'dsa', 'transactions.json')

with open(json_path, 'r') as f:
    transactions_list = json.load(f)

transactions_dict = {t["transaction_id"]: t for t in transactions_list}

VALID_USERNAME = "admin"
VALID_PASSWORD = "MomoSms26"
