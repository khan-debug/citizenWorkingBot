# Citizen Bot Pakistan - AI Agent Setup

This project contains an AI agent that helps explain government policies and eligibility criteria to Pakistani citizens in simple, plain language.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Cloud Project with billing enabled
- Service account credentials

### Installation

1. **Clone and setup the project:**
   ```bash
   git clone <your-repo-url>
   cd citizen-bot-pakistan
   ```

2. **Activate the virtual environment:**
   ```bash
   # On Windows
   .\venv\Scripts\Activate.ps1
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Enable required Google Cloud APIs:**
   ```bash
   python setup_apis.py
   ```
   
   Or manually enable these APIs in the [Google Cloud Console](https://console.cloud.google.com):
   - Vertex AI API (`aiplatform.googleapis.com`)
   - Generative Language API (`generativelanguage.googleapis.com`)

5. **Run the agent:**
   ```bash
   python agents.py
   ```

## 🔧 Configuration

### Authentication
The project uses a service account key file (`service-account-key.json`) for authentication. Make sure this file is present and contains valid credentials.

### Project Settings
- **Project ID:** `ultimate-realm-473419-c7`
- **Location:** `us-central1`
- **Model:** `gemini-pro`

## 📁 Project Structure

```
citizen-bot-pakistan/
├── agents.py              # Main AI agent implementation
├── app.py                  # Flask web application
├── setup_apis.py          # API setup script
├── service-account-key.json # Google Cloud credentials
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🤖 How the Agent Works

The `explain_in_plain_language()` function takes technical government policy information and converts it into simple, citizen-friendly explanations.

### Features:
- **AI-Powered Explanations:** Uses Google's Gemini Pro model for natural language processing
- **Fallback System:** Provides rule-based explanations when AI is unavailable
- **Citizen-Friendly:** Focuses on clear, encouraging language for Pakistani citizens
- **Error Handling:** Graceful degradation when services are unavailable

### Example Usage:

```python
from agents import explain_in_plain_language

technical_data = """
{
    "status": "INELIGIBLE",
    "scheme": "Ehsaas Education Grant",
    "reason_code": "INCOME_EXCEEDS_LIMIT",
    "details": "User's monthly income of 35000 is greater than the allowed maximum of 30000."
}
"""

explanation = explain_in_plain_language(technical_data)
print(explanation)
```

## 🛠️ Troubleshooting

### Common Issues:

1. **"Module not found" errors:**
   - Make sure you're in the virtual environment
   - Run `pip install -r requirements.txt`

2. **Authentication errors:**
   - Verify `service-account-key.json` exists and is valid
   - Check that the service account has proper permissions

3. **API not enabled errors:**
   - Run `python setup_apis.py` to enable required APIs
   - Or manually enable APIs in Google Cloud Console

4. **Model not found errors:**
   - The project uses `gemini-pro` model
   - Ensure Vertex AI API is enabled for your project

### Fallback Mode:
If the AI service is unavailable, the agent will automatically switch to a rule-based fallback system that provides basic explanations for common scenarios.

## 🔒 Security Notes

- Keep your `service-account-key.json` file secure and never commit it to version control
- The service account should have minimal required permissions
- Consider using environment variables for sensitive configuration in production

## 📝 Development

### Adding New Explanation Rules:
Edit the `create_fallback_explanation()` function in `agents.py` to add new rule-based explanations for specific scenarios.

### Testing:
```bash
python agents.py
```

This will run the test case with sample data and show the agent's output.

## 🌐 Web Application

The project also includes a Flask web application (`app.py`) that provides REST API endpoints for policy information.

To run the web app:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Google Cloud documentation for API setup
3. Contact the development team

## 🎯 Future Enhancements

- [ ] Support for multiple languages (Urdu, Punjabi)
- [ ] Integration with more government databases
- [ ] Voice-based explanations
- [ ] Mobile app integration
- [ ] Real-time policy updates
