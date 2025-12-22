import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# --- KONFIGURASI GEMINI ---
# Kita mengambil API Key dari Environment Variable (agar aman)
# Nanti kita setting kuncinya di dashboard Vercel
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Konfigurasi model jika API Key ditemukan
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

# --- RUTE WEBSITE ---

@app.route('/')
def home():
    # Ini akan menampilkan file HTML (tampilan chat)
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not GOOGLE_API_KEY:
        return jsonify({"response": "Error: API Key belum di-setting di Vercel!"})

    data = request.get_json()
    user_message = data.get('message', '')

    try:
        # Kirim pesan user ke Gemini
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_message)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Maaf, terjadi kesalahan: {str(e)}"

    return jsonify({"response": bot_reply})

# Baris ini penting untuk Vercel
app = app