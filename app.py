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
    
    # KITA COBA GEMINI 1.5 PRO (Biasanya lebih stabil di berbagai region)
    # Jika gagal, URL ini mudah diganti ke gemini-1.0-pro
    model_name = "gemini-1.5-pro" 
    url = f"https://generativelanguage.googleapis.com/v1/models/{model_name}:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": user_message}]}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        if response.status_code == 200:
            bot_reply = response_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"response": bot_reply})
        else:
            # Jika 1.5-pro tidak ada, kita coba tembak gemini-1.0-pro sebagai usaha terakhir
            url_fallback = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.0-pro:generateContent?key={API_KEY}"
            res_fall = requests.post(url_fallback, headers=headers, json=payload)
            if res_fall.status_code == 200:
                bot_reply = res_fall.json()['candidates'][0]['content']['parts'][0]['text']
                return jsonify({"response": bot_reply})
            
            error_msg = response_data.get('error', {}).get('message', 'Model tidak tersedia di region kamu.')
            return jsonify({"response": f"Pesan dari Google: {error_msg}"})
            
    except Exception as e:
        return jsonify({"response": f"Masalah koneksi: {str(e)}"})

app = app