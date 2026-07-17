"""Minimal HTTP backend built on the standard library only.

Listens on 0.0.0.0:8080 and answers "/" with a plain-text greeting.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "0.0.0.0"
PORT = 8080
MESSAGE = b"Hello from Effective Mobile!"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(MESSAGE)))
            self.end_headers()
            self.wfile.write(MESSAGE)
        else:
            self.send_error(404, "Not Found")

    def log_message(self, format, *args):
        # Log to stdout so `docker logs` picks it up
        print(f"{self.address_string()} - {format % args}", flush=True)


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Backend listening on {HOST}:{PORT}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
