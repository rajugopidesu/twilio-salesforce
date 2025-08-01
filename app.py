from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import whisper
import os
import tempfile

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render"""
    return jsonify({"status": "healthy", "message": "Transcription service is running"})

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Transcribe Twilio recording using Whisper
    
    Expected JSON payload:
    {
        "account_sid": "your_twilio_account_sid",
        "auth_token": "your_twilio_auth_token", 
        "recording_sid": "REyour_recording_sid",
        "whisper_model_size": "base"  // optional, defaults to "base"
    }
    """
    try:
        # Extract input parameters from request
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        account_sid = data.get('account_sid')
        auth_token = data.get('auth_token')
        recording_sid = data.get('recording_sid')
        whisper_model_size = data.get('whisper_model_size', 'base')
        
        # Validate required parameters
        if not all([account_sid, auth_token, recording_sid]):
            return jsonify({"error": "Missing required parameters: account_sid, auth_token, recording_sid"}), 400
        
        # Create temporary file for recording
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            recording_filename = temp_file.name
        
        try:
            # Download recording from Twilio
            print(f"📥 Downloading recording: {recording_sid}")
            recording_url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Recordings/{recording_sid}.mp3'
            response = requests.get(recording_url, auth=HTTPBasicAuth(account_sid, auth_token))
            
            if response.status_code != 200:
                raise Exception(f"Twilio download error: {response.status_code} - {response.text}")
            
            # Save recording to temporary file
            with open(recording_filename, "wb") as f:
                f.write(response.content)
            
            print(f"✅ Recording downloaded: {len(response.content)} bytes")
            
            # Load Whisper model and transcribe
            print(f"🧠 Loading Whisper model: {whisper_model_size}")
            model = whisper.load_model(whisper_model_size)
            
            print("🎤 Transcribing audio...")
            result = model.transcribe(recording_filename)
            transcript = result["text"]
            
            print(f"✅ Transcription completed: {len(transcript)} characters")
            
            return jsonify({
                "transcript": transcript,
                "recording_sid": recording_sid,
                "model_size": whisper_model_size,
                "status": "success"
            })
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(recording_filename)
                print("🧹 Temporary file cleaned up")
            except:
                pass
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with usage instructions"""
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
                "whisper_model_size": "base"  // optional
            }
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 