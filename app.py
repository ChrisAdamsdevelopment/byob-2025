from flask import Flask, render_template, request, send_file
import os, base64

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    payload = request.form["payload"]
    with open("output/payload.b64", "w") as f:
        f.write(base64.b64encode(payload.encode()).decode())
    return send_file("output/payload.b64", as_attachment=True)

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    app.run(port=8081)
