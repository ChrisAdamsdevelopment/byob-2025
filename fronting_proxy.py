import http.server, socketserver, ssl, json

class FrontProxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"[+] Fronting proxy received request")

if __name__ == "__main__":
    with open("config_front.json") as f:
        cfg = json.load(f)

    handler = FrontProxy
    httpd = socketserver.TCPServer(("0.0.0.0", 443), handler)
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile="key.pem", certfile="cert.pem", server_side=True)
    print(f"[+] Fronting on {cfg['front_domain']} forwarding to {cfg['local_forward']}")
    httpd.serve_forever()
