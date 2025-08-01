# Twilio Recording Transcription Service

A Flask web service that transcribes Twilio call recordings using OpenAI Whisper.

## Features

- 🎤 Transcribe Twilio call recordings using Whisper
- 🌐 RESTful API endpoints
- ☁️ Ready for deployment on Render
- 🔒 Secure parameter validation
- 🧹 Automatic temporary file cleanup

## API Endpoints

### Health Check
```
GET /health
```
Returns service status.

### Transcribe Recording
```
POST /transcribe
```

**Request Body:**
```json
{
    "account_sid": "your_twilio_account_sid",
    "auth_token": "your_twilio_auth_token",
    "recording_sid": "REyour_recording_sid",
    "whisper_model_size": "base"  // optional, defaults to "base"
}
```

**Response:**
```json
{
    "transcript": "The transcribed text from the audio recording",
    "recording_sid": "REyour_recording_sid",
    "model_size": "base",
    "status": "success"
}
```

## Deployment on Render

### Option 1: Using render.yaml (Recommended)

1. **Fork/Clone this repository**
2. **Connect to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Deploy:**
   - Render will automatically build and deploy your service
   - Your service will be available at: `https://your-service-name.onrender.com`

### Option 2: Manual Deployment

1. **Create a new Web Service on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" → "Web Service"
   - Connect your GitHub repository

2. **Configure the service:**
   - **Name:** `twilio-transcription-service`
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

3. **Deploy:**
   - Click "Create Web Service"
   - Render will build and deploy your application

## Local Development

### Prerequisites
- Python 3.9+
- pip

### Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd <your-repo-directory>

# Option 1: Use the setup script (recommended)
python setup.py

# Option 2: Install manually
pip install git+https://github.com/openai/whisper.git
pip install torch
pip install -r requirements.txt

# Run locally
python app.py
```

### Test the API
```bash
# Health check
curl https://your-service-name.onrender.com/health

# Transcribe a recording
curl -X POST https://your-service-name.onrender.com/transcribe \
  -H "Content-Type: application/json" \
  -d '{
    "account_sid": "your_account_sid",
    "auth_token": "your_auth_token",
    "recording_sid": "REyour_recording_sid"
  }'
```

## Whisper Model Sizes

- `tiny`: Fastest, least accurate
- `base`: Good balance (default)
- `small`: Better accuracy
- `medium`: High accuracy
- `large`: Best accuracy, slowest

## Error Handling

The service returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (missing parameters)
- `500`: Server error (Twilio API error, Whisper error, etc.)

## Security Notes

- Never commit your Twilio credentials to version control
- Use environment variables for sensitive data in production
- The service validates all input parameters
- Temporary files are automatically cleaned up

## Troubleshooting

### Common Issues

1. **Build fails on Render:**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version is compatible

2. **Whisper model download fails:**
   - Render may have network restrictions
   - Try using a smaller model size

3. **Twilio authentication fails:**
   - Verify your Account SID and Auth Token
   - Check that the recording SID exists

### Logs
Check Render logs for detailed error information:
- Go to your service dashboard
- Click on "Logs" tab
- Look for error messages and stack traces

## License

MIT License 