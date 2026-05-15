from flask import Flask, request
import requests
from groq import Groq

app = Flask(__name__)

TOKEN    = "wati_a25a27d5-04f7-4202-adb3-63c35d10b849.p_G0lLjySFgx26zaTi1iQazskNnQbfXKUVy-Nz01DNTfn3j1ZMFkLd9kK6kAdNs-adMN48BnoemnxSssdsvlXycpEgQ6h0AT6yUZnap81wy-uBXZefVuQ3ZdDihHy7Hd"
ENDPOINT = "https://live-mt-server.wati.io/10158876"
HEADERS  = {"Authorization": f"Bearer {TOKEN}"}

GROQ_KEY = "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"
client   = Groq(api_key=GROQ_KEY)

SYSTEM_PROMPT = """
Kamu adalah asisten penjualan Closari yang ramah dan profesional.
Kamu membantu customer menjawab pertanyaan dan memandu proses order via WhatsApp.
Balas dalam Bahasa Indonesia, singkat dan natural seperti chat biasa.
Maksimal 3-4 kalimat per balasan.
"""

history = {}

def get_ai_reply(phone, text):
    if phone not in history:
        history[phone] = []
    history[phone].append({"role": "user", "content": text})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history[phone],
        max_tokens=500
    )
    reply = response.choices[0].message.content
    history[phone].append({"role": "assistant", "content": reply})
    return reply

def send_message(phone, message):
    phone = phone.replace("+", "").replace("-", "").replace(" ", "")
    url = f"{ENDPOINT}/api/v1/sendSessionMessage/{phone}"
    r = requests.post(url, data={"messageText": message}, headers=HEADERS)
    print(f"Kirim ke {phone}: {r.status_code} - {r.text}")

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
    reply = get_ai_reply(phone, text)
    send_message(phone, reply)
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "Server Closari aktif!", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)