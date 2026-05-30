from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
import os

# Load transactions from JSON file

json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'transactions.json')

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

        parts = auth_header.split(' ')
        if len(parts) != 2:
            return False

        encoded = parts[1]

        try:
            decoded = base64.b64decode(encoded).decode('utf-8')
            username, password = decoded.split(':', 1)
            return username == VALID_USERNAME and password == VALID_PASSWORD
        except Exception:
            return False

    def deny_access(self):
        self.send_response(401)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {"error": "Unauthorized. Invalid credentials."}
        self.wfile.write(json.dumps(response).encode())

    
    def get_transaction_id(self):
        try:
            return int(self.path.split('/')[2])
        except (IndexError, ValueError):
            return None

    # GET ENDPOINTS
   

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
            transaction_id = self.get_transaction_id()

            if transaction_id is None:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "Transaction ID must be a number"}
                self.wfile.write(json.dumps(response).encode())
                return

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

    # POST ENDPOINT
    

    def do_POST(self):

        if not self.verify_user():
            self.deny_access()
            return

        if self.path == '/transactions':

            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "Request body cannot be empty"}
                self.wfile.write(json.dumps(response).encode())
                return

            body = self.rfile.read(content_length)

            try:
                new_transaction = json.loads(body.decode('utf-8'))
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "Invalid JSON format in request body"}
                self.wfile.write(json.dumps(response).encode())
                return


            required_fields = ['transaction_id', 'category', 'amount',
                                'sender', 'receiver', 'transaction_date']
            for field in required_fields:
                if field not in new_transaction:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = {"error": f"Missing required field: {field}"}
                    self.wfile.write(json.dumps(response).encode())
                    return

# Validate amount is positive

            try:
                if float(new_transaction['amount']) <= 0:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = {"error": "Amount must be greater than zero"}
                    self.wfile.write(json.dumps(response).encode())
                    return
            except (ValueError, TypeError):
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "Amount must be a valid number"}
                self.wfile.write(json.dumps(response).encode())
                return

# Check for duplicate transaction ID
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

    
    # PUT ENDPOINT
   

    def do_PUT(self):

        if not self.verify_user():
            self.deny_access()
            return

        if self.path.startswith('/transactions/'):
            transaction_id = self.get_transaction_id()

            if transaction_id is None:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "Transaction ID must be a number"}
                self.wfile.write(json.dumps(response).encode())
                return

            transaction = transactions_dict.get(transaction_id)

            if not transaction:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "Transaction not found"}
                self.wfile.write(json.dumps(response).encode())
                return

            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "Request body cannot be empty"}
                self.wfile.write(json.dumps(response).encode())
                return

            body = self.rfile.read(content_length)

# Handle invalid JSON
            try:
                updates = json.loads(body.decode('utf-8'))
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "Invalid JSON format in request body"}
                self.wfile.write(json.dumps(response).encode())
                return

# Handle empty updates object
            if not updates:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "No fields provided to update"}
                self.wfile.write(json.dumps(response).encode())
                return

            transaction.update(updates)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(transaction).encode())

        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response).encode())

    
    # DELETE ENDPOINT
    

    def do_DELETE(self):

        if not self.verify_user():
            self.deny_access()
            return

        if self.path.startswith('/transactions/'):
            transaction_id = self.get_transaction_id()

            if transaction_id is None:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "Transaction ID must be a number"}
                self.wfile.write(json.dumps(response).encode())
                return

            transaction = transactions_dict.get(transaction_id)

            if not transaction:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"error": "Transaction not found"}
                self.wfile.write(json.dumps(response).encode())
                return

            transactions_dict.pop(transaction_id)
            transactions_list.remove(transaction)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"message": "Transaction deleted successfully"}
            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response).encode())


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), Momoapi)
    print('MoMo SMS API running on http://localhost:8080')
    print('Press CTRL+C to stop the server')
    server.serve_forever()