#!/usr/bin/env python3

import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from lib.json_io import load_json, save_json
from urllib.parse import urlparse, parse_qs

def make_handler(requisition_file): # Factory function necessary to pass a parameter to handler (instantiated by HTTPServer)
    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            token = query_params.get('ref', [None])[0]
            if token:
                save_json({ 'requisition_id': token }, requisition_file)
                print(f"Token saved to {requisition_file}")
            else:
                print("No token received.")

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body>Authentication complete. You can close this window.</body></html>")
            threading.Thread(target=self.server.shutdown, daemon=True).start()

    return CallbackHandler

def main(port, requisition_file):
    server_address = ('', port)
    handler_class = make_handler(requisition_file)
    httpd = HTTPServer(server_address, handler_class)
    print(f"Listening on http://localhost:{port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: 4.requisition.py <port> <requisition_file>') # Eg 8080 io/requisition.json
        sys.exit(1)

    port = int(sys.argv[1])
    requisition_file = sys.argv[2]
    main(port, requisition_file)
