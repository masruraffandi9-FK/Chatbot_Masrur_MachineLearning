import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Ambil API Key dari Vercel Environment Variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    # Gunakan 'gemini-1.5-flash-latest' atau 'gemini-pro' sebagai cadangan
    # Terkadang 'gemini-1.5-flash' saja dianggap tidak ada di beberapa titik server
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

@app.route('/')
def home():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not GOOGLE_API_KEY:
        return jsonify({"response": "API Key tidak terbaca."})

    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        # Tambahkan safety_settings jika perlu, tapi untuk sekarang kita buat simpel
        response = model.generate_content(user_message)
        
        # Ambil teksnya, pastikan tidak kosong
        bot_reply = response.text if response.text else "Maaf, AI tidak bisa menjawab itu."
        return jsonify({"response": bot_reply})
            
    except Exception as e:
        # Jika 'gemini-1.5-flash-latest' gagal, coba ganti ke 'gemini-pro' secara otomatis
        try:
            fallback_model = genai.GenerativeModel('gemini-pro')
            response = fallback_model.generate_content(user_message)
            return jsonify({"response": response.text})
        except:
            return jsonify({"response": f"Masih sinkronisasi API: {str(e)}"})

app = app