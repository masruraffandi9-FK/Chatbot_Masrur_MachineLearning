import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Ambil API Key dari Vercel Environment Variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    # Gunakan format models/ untuk stabilitas di Vercel
    model = genai.GenerativeModel('models/gemini-1.5-flash')

@app.route('/')
def home():
    # Sesuaikan dengan nama file di folder templates kamu
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not GOOGLE_API_KEY:
        return jsonify({"response": "Konfigurasi API Key belum selesai di Vercel."})

    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        # Gunakan generate_content langsung (lebih stabil dibanding start_chat)
        response = model.generate_content(user_message)
        
        if response.text:
            return jsonify({"response": response.text})
        else:
            return jsonify({"response": "AI tidak memberikan jawaban, coba lagi."})
            
    except Exception as e:
        # Menampilkan pesan error asli agar kita tahu masalahnya
        return jsonify({"response": f"Terjadi kesalahan: {str(e)}"})

# Diperlukan oleh Vercel
app = app