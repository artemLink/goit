import json
import socketserver
import socket
from http.server import BaseHTTPRequestHandler
import urllib.parse
import pathlib
import mimetypes
from datetime import datetime
import threading


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        if post_data:
            self.send_response(303)
            self.send_header('Location', '/message')
            self.end_headers()


            pairs = post_data.split('&')
            data = {}
            for pair in pairs:
                key, value = pair.split('=')
                data[key] = value

            timestamp = datetime.now().isoformat()

            try:
                with open('storage/data.json', 'r') as json_file:
                    file_data = json.load(json_file)
            except FileNotFoundError:
                file_data = {}

            file_data[timestamp] = data

            with open('storage/data.json', 'w') as json_file:
                json.dump(file_data, json_file, indent=2)


def run_http_server():
    with socketserver.TCPServer(("", 3000), HttpHandler) as httpd:
        print("HTTP server is running at port 3000...")
        httpd.serve_forever()


def handle_socket_data():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('localhost', 5000))
        print("Socket server is running at port 5000...")
        while True:
            data, _ = sock.recvfrom(1024)


http_thread = threading.Thread(target=run_http_server)
http_thread.start()

socket_thread = threading.Thread(target=handle_socket_data)
socket_thread.start()
