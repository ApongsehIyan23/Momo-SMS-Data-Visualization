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

class Momoapi(BaseHTTPRequestHandler):

    def verify_user(self):
        auth_header = self.headers.get('Authorization')

        if not auth_header:
            return False

        encoded = auth_header.split(' ')[1]

        decoded = base64.b64decode(encoded).decode('utf-8')

        username, password = decoded.split(':')

        return username == VALID_USERNAME and password == VALID_PASSWORD

    def deny_access(self):
        self.send_response(401)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {"error": "Unauthorized. Invalid credentials."}
        self.wfile.write(json.dumps(response).encode())
