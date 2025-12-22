import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Ambil API Key dari Vercel Environment Variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if GOOGLE_API_KEY:
    # Set konfigurasi secara manual ke versi v1 (Stabil)
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Inisialisasi model
    # Jika gemini-1.5-flash masih bermasalah, gunakan gemini-1.5-flash-latest
    model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not GOOGLE_API_KEY:
        return jsonify({"response": "Konfigurasi API Key belum selesai."})

    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        # Tambahkan instruksi agar respon lebih cepat
        response = model.generate_content(user_message)
        
        return jsonify({"response": response.text})
            
    except Exception as e:
        # Jika masih 404, kita akan menangkap pesan errornya di sini
        return jsonify({"response": f"Sistem sedang sinkronisasi: {str(e)}"})

app = app