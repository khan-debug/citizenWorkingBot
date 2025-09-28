#!/usr/bin/env python3
"""
Comprehensive setup script for Citizen Bot Pakistan
This script handles all the setup requirements to make the app runnable.
"""

import subprocess
import sys
import os
import json
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command and return the result."""
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"❌ Command failed: {result.stderr}")
            return False, result.stdout, result.stderr
        return True, result.stdout, result.stderr
    except Exception as e:
        print(f"❌ Exception running command: {str(e)}")
        return False, "", str(e)

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported. Please use Python 3.8 or higher.")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist."""
    print("📦 Setting up virtual environment...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    success, _, _ = run_command("python -m venv venv")
    if success:
        print("✅ Virtual environment created successfully")
        return True
    else:
        print("❌ Failed to create virtual environment")
        return False

def get_activation_command():
    """Get the correct activation command for the current OS."""
    if os.name == 'nt':  # Windows
        return "venv\\Scripts\\activate"
    else:  # Unix-like systems
        return "source venv/bin/activate"

def install_dependencies():
    """Install required dependencies."""
    print("📚 Installing dependencies...")
    
    # Determine pip command based on OS
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix-like systems
        pip_cmd = "venv/bin/pip"
    
    # Upgrade pip first
    success, _, _ = run_command(f"{pip_cmd} install --upgrade pip")
    if not success:
        print("❌ Failed to upgrade pip")
        return False
    
    # Install requirements
    success, _, _ = run_command(f"{pip_cmd} install -r requirements.txt")
    if success:
        print("✅ Dependencies installed successfully")
        return True
    else:
        print("❌ Failed to install dependencies")
        return False

def create_service_account_template():
    """Create a template for service account key."""
    print("🔑 Creating service account key template...")
    
    template = {
        "type": "service_account",
        "project_id": "your-project-id",
        "private_key_id": "your-private-key-id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
        "client_email": "your-service-account@your-project-id.iam.gserviceaccount.com",
        "client_id": "your-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com"
    }
    
    with open("service-account-key-template.json", "w") as f:
        json.dump(template, f, indent=2)
    
    print("✅ Service account template created: service-account-key-template.json")
    return True

def create_env_file():
    """Create environment configuration file."""
    print("⚙️ Creating environment configuration...")
    
    env_content = """# Citizen Bot Pakistan Environment Configuration
# Copy this file to .env and update the values

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=service-account-key.json
GOOGLE_CLOUD_PROJECT_ID=ultimate-realm-473419-c7
GOOGLE_CLOUD_LOCATION=us-central1

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000

# AI Model Configuration
AI_MODEL=gemini-pro

# Application Configuration
APP_NAME=Citizen Bot Pakistan
APP_VERSION=1.0.0
"""
    
    with open(".env.template", "w") as f:
        f.write(env_content)
    
    print("✅ Environment template created: .env.template")
    return True

def create_startup_scripts():
    """Create startup scripts for different platforms."""
    print("🚀 Creating startup scripts...")
    
    # Windows batch script
    windows_script = """@echo off
echo Starting Citizen Bot Pakistan...
echo.

REM Activate virtual environment
call venv\\Scripts\\activate

REM Check if service account key exists
if not exist "service-account-key.json" (
    echo ERROR: service-account-key.json not found!
    echo Please follow the setup instructions to create this file.
    echo.
    pause
    exit /b 1
)

REM Start the application
echo Starting Flask application...
python app.py

pause
"""
    
    with open("start_app.bat", "w") as f:
        f.write(windows_script)
    
    # Unix shell script
    unix_script = """#!/bin/bash
echo "Starting Citizen Bot Pakistan..."
echo

# Activate virtual environment
source venv/bin/activate

# Check if service account key exists
if [ ! -f "service-account-key.json" ]; then
    echo "ERROR: service-account-key.json not found!"
    echo "Please follow the setup instructions to create this file."
    echo
    exit 1
fi

# Start the application
echo "Starting Flask application..."
python app.py
"""
    
    with open("start_app.sh", "w") as f:
        f.write(unix_script)
    
    # Make shell script executable
    if os.name != 'nt':
        os.chmod("start_app.sh", 0o755)
    
    print("✅ Startup scripts created")
    return True

def create_setup_instructions():
    """Create detailed setup instructions."""
    print("📖 Creating setup instructions...")
    
    instructions = """# Citizen Bot Pakistan - Complete Setup Guide

## 🚀 Quick Setup (Automated)

1. **Run the setup script:**
   ```bash
   python setup.py
   ```

2. **Follow the Google Cloud setup steps below**

3. **Start the application:**
   ```bash
   # Windows
   start_app.bat
   
   # macOS/Linux
   ./start_app.sh
   ```

## 🔧 Manual Setup Steps

### 1. Google Cloud Setup

#### Create a Google Cloud Project:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Note your Project ID

#### Enable Required APIs:
1. Go to "APIs & Services" > "Library"
2. Enable these APIs:
   - Vertex AI API (`aiplatform.googleapis.com`)
   - Generative Language API (`generativelanguage.googleapis.com`)

#### Create Service Account:
1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Name: `citizen-bot-service`
4. Grant these roles:
   - Vertex AI User
   - AI Platform Developer
5. Click "Create Key" > "JSON"
6. Download the key file
7. Rename it to `service-account-key.json`
8. Place it in the project root directory

### 2. Environment Setup

#### Copy environment template:
```bash
cp .env.template .env
```

#### Edit .env file with your values:
- Update `GOOGLE_CLOUD_PROJECT_ID` with your project ID
- Update other values as needed

### 3. Install Dependencies

#### Activate virtual environment:
```bash
# Windows
venv\\Scripts\\activate

# macOS/Linux
source venv/bin/activate
```

#### Install packages:
```bash
pip install -r requirements.txt
```

### 4. Test the Setup

#### Test the agents:
```bash
python agents.py
```

#### Test the web app:
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## 🛠️ Troubleshooting

### Common Issues:

1. **"Module not found" errors:**
   - Make sure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **Authentication errors:**
   - Verify `service-account-key.json` exists and is valid
   - Check service account permissions

3. **API not enabled errors:**
   - Enable required APIs in Google Cloud Console
   - Wait a few minutes for changes to propagate

4. **Port already in use:**
   - Change port in `.env` file
   - Or kill process using port 5000

### Fallback Mode:
If Google Cloud APIs are unavailable, the app will use fallback explanations.

## 📱 Features

- **AI-Powered Analysis:** Uses Google's Gemini Pro model
- **Scheme Information:** Detailed government scheme details
- **Document Collection:** Required documents for applications
- **Helpline Integration:** Direct contact information
- **Query Forwarding:** Forward complex queries to departments
- **Multi-language Support:** English and Urdu explanations

## 🌐 Web Interface

The application provides a modern web interface with:
- Issue submission form
- AI analysis and recommendations
- Scheme details and benefits
- Document requirements
- Helpline information
- Query forwarding system

## 📞 Support

For issues or questions:
1. Check this troubleshooting guide
2. Review Google Cloud documentation
3. Contact the development team

## 🎯 Next Steps

After setup:
1. Test the application with sample queries
2. Customize scheme data in `app.py`
3. Deploy to production if needed
4. Add more schemes and features
"""
    
    with open("SETUP_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)
    
    print("✅ Setup instructions created: SETUP_INSTRUCTIONS.md")
    return True

def main():
    """Main setup function."""
    print("🚀 Citizen Bot Pakistan - Complete Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create configuration files
    create_service_account_template()
    create_env_file()
    create_startup_scripts()
    create_setup_instructions()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Follow the instructions in SETUP_INSTRUCTIONS.md")
    print("2. Create your Google Cloud service account key")
    print("3. Place service-account-key.json in the project root")
    print("4. Run the application:")
    print("   - Windows: start_app.bat")
    print("   - macOS/Linux: ./start_app.sh")
    print("\n📖 For detailed instructions, see SETUP_INSTRUCTIONS.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

