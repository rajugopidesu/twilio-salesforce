from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import whisper
import os
import tempfile
import torch
import gc

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Transcription service is running"})

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        account_sid = data.get('account_sid')
        auth_token = data.get('auth_token')
        recording_sid = data.get('recording_sid')
        whisper_model_size = data.get('whisper_model_size', 'base')

        if not all([account_sid, auth_token, recording_sid]):
            return jsonify({"error": "Missing required parameters: account_sid, auth_token, recording_sid"}), 400

        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            recording_filename = temp_file.name

        try:
            print(f"📥 Downloading recording: {recording_sid}")
            recording_url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Recordings/{recording_sid}.mp3'
            response = requests.get(recording_url, auth=HTTPBasicAuth(account_sid, auth_token))

            if response.status_code != 200:
                raise Exception(f"Twilio download error: {response.status_code} - {response.text}")

            with open(recording_filename, "wb") as f:
                f.write(response.content)

            print(f"✅ Recording downloaded: {len(response.content)} bytes")

            print(f"🧠 Loading Whisper model: {whisper_model_size}")
            device = 'cuda' if torch.cuda.is_available() else 'cpu'

            try:
                model = whisper.load_model(whisper_model_size).to(device)
            except Exception as model_error:
                raise Exception(f"Failed to load Whisper model: {model_error}")

            print("🎤 Transcribing audio...")
            result = model.transcribe(recording_filename)
            transcript = result["text"]
            print(f"✅ Transcription completed: {len(transcript)} characters")

            # Free memory
            del model
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

            return jsonify({
                "transcript": transcript,
                "recording_sid": recording_sid,
                "model_size": whisper_model_size,
                "status": "success"
            })

        finally:
            try:
                os.unlink(recording_filename)
                print("🧹 Temporary file cleaned up")
            except Exception as cleanup_error:
                print(f"⚠️ Cleanup error: {cleanup_error}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Twilio Recording Transcription Service",
        "endpoints": {
            "/health": "Health check endpoint",
            "/transcribe": "POST endpoint for transcription",
            "/": "This help message"
        },
        "usage": {
            "method": "POST",
            "url": "/transcribe",
            "content_type": "application/json",
            "body": {
                "account_sid": "your_twilio_account_sid",
                "auth_token": "your_twilio_auth_token",
                "recording_sid": "REyour_recording_sid",
                "whisper_model_size": "tiny"  # recommended for low memory
            }
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
