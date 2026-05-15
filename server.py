from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN    = "wati_a25a27d5-04f7-4202-adb3-63c35d10b849.p_G0lLjySFgx26zaTi1iQazskNnQbfXKUVy-Nz01DNTfn3j1ZMFkLd9kK6kAdNs-adMN48BnoemnxSssdsvlXycpEgQ6h0AT6yUZnap81wy-uBXZefVuQ3ZdDihHy7Hd"
ENDPOINT = "https://live-mt-server.wati.io/10158876"
HEADERS  = {"Authorization": f"Bearer {TOKEN}"}

def send_message(phone, message):
    url = f"{ENDPOINT}/api/v1/sendSessionMessage/{phone}"
    r = requests.post(url, data={"messageText": message}, headers=HEADERS)
    print("Kirim:", r.text)

@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    data = request.json or {}
    print("Masuk:", data)

    phone = data.get("waId")
    text  = data.get("text", "")

    if data.get("owner"):
        return "OK", 200
    if not phone or not text:
        return "OK", 200

    send_message(phone, f"Halo! Kamu bilang: {text}")
    return "OK", 200

# Test endpoint
@app.route("/", methods=["GET"])
def home():
    return "Server Closari aktif!", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)