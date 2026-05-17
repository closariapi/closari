from flask import Flask, request
from twilio.rest import Client
from groq import Groq
import os

app = Flask(__name__)

# Twilio - ambil dari environment variables
TWILIO_SID   = os.environ.get("TWILIO_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN")
FROM_NUMBER  = "whatsapp:+6288211488947"

twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)

# Groq AI - ambil dari environment variables
GROQ_KEY = os.environ.get("GROQ_KEY")
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

@app.route("/webhook", methods=["POST"])
def webhook():
    phone = request.form.get("From", "")  # format: whatsapp:+628xxx
    text  = request.form.get("Body", "")
    print(f"Masuk dari {phone}: {text}")

    if not phone or not text:
        return "OK", 200

    reply = get_ai_reply(phone, text)

    twilio_client.messages.create(
        from_=FROM_NUMBER,
        to=phone,
        body=reply
    )
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "Server Closari aktif!", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)