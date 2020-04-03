from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from myFunc.utils import *
from config import *

class S(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def regenOut(self):
        self.out = "<!DOCTYPE html><html lang=\"en\"><head><script>var data="
        with mutex:
            with open("webserver/chain.json") as f:
                self.out += f.read()
                f.close()
            self.out += ";</script>"
            with open("webserver/index.html") as f:
                self.out += f.read()
                f.close()

    def do_GET(self):
        self._set_response()
        self.regenOut()
        self.wfile.write("{}".format(self.out).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self._set_response()
        data = post_data.decode('utf-8').split("=")[1]
        producer = Thread(target=produce, args=(str(data),), name="ProducerThread")
        producer.start()
        self.regenOut()
        self.wfile.write("{}".format(self.out).encode('utf-8'))

def webServerRun(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('localhost', port)
    while not exit_event.isSet():
        httpd = server_class(server_address, handler_class)
        httpd.handle_request()
        httpd.server_close()