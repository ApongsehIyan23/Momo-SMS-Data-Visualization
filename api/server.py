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

    def do_GET(self):

        if not self.verify_user():
            self.deny_access()
            return

        if self.path == '/transactions':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(transactions_list).encode())

        elif self.path.startswith('/transactions/'):
            transaction_id = int(self.path.split('/')[2])

            transaction = transactions_dict.get(transaction_id)

            if transaction:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(transaction).encode())
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "Transaction not found"}
                self.wfile.write(json.dumps(response).encode())

        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):

        if not self.verify_user():
            self.deny_access()
            return

        if self.path == '/transactions':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            new_transaction = json.loads(body.decode('utf-8'))

            required_fields = ['transaction_id', 'category', 'amount', 'sender', 'receiver', 'transaction_date']
            for field in required_fields:
                if field not in new_transaction:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = {"error": f"Missing required field: {field}"}
                    self.wfile.write(json.dumps(response).encode())
                    return

            if new_transaction['transaction_id'] in transactions_dict:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "Transaction ID already exists"}
                self.wfile.write(json.dumps(response).encode())
                return

            transactions_list.append(new_transaction)
            transactions_dict[new_transaction['transaction_id']] = new_transaction

            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(new_transaction).encode())

        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_PUT(self):

        if not self.verify_user():
            self.deny_access()
            return

        if self.path.startswith('/transactions/'): 
            transaction_id = int(self.path.split('/')[2])
            transaction = transactions_dict.get(transaction_id)

            if not transaction:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "Transaction not found"}
                self.wfile.write(json.dumps(response).encode())
                return
                content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            updates = json.loads(body.decode('utf-8'))

            transaction.update(updates)


           