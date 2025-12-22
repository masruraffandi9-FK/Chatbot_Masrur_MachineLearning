import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Ambil API Key dari Vercel Environment Variables
API_KEY = os.getenv('GOOGLE_API_KEY')

@app.route('/')
def home():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not API_KEY:
        return jsonify({"response": "API Key belum diatur di Vercel."})

    user_message = request.get_json().get('message', '')
    
    # URL API Google Gemini Resmi (Versi v1 - Stabil)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    # Struktur data sesuai dokumentasi resmi Google
    payload = {
        "contents": [{
            "parts": [{"text": user_message}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        # Ambil teks balasan dari struktur JSON Google
        if response.status_code == 200:
            bot_reply = response_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"response": bot_reply})
        else:
            error_msg = response_data.get('error', {}).get('message', 'Kesalahan API')
            return jsonify({"response": f"API Error: {error_msg}"})
            
    except Exception as e:
        return jsonify({"response": f"Koneksi gagal: {str(e)}"})

app = app