#!/usr/bin/env python3
"""
Fallback configuration for Citizen Bot Pakistan
This allows the app to run without Google Cloud APIs for testing purposes.
"""

import os
import json
from typing import Dict, Any

# Fallback configuration
FALLBACK_CONFIG = {
    "use_fallback": True,
    "project_id": "fallback-project",
    "location": "us-central1",
    "model": "fallback-model"
}

def setup_fallback_environment():
    """Setup environment for fallback mode."""
    print("🔄 Setting up fallback mode...")
    
    # Set environment variables for fallback
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'fallback-credentials.json'
    os.environ['FALLBACK_MODE'] = 'true'
    
    # Create fallback credentials file
    fallback_credentials = {
        "type": "service_account",
        "project_id": "fallback-project",
        "private_key_id": "fallback-key-id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nFALLBACK_KEY\n-----END PRIVATE KEY-----\n",
        "client_email": "fallback@fallback-project.iam.gserviceaccount.com",
        "client_id": "fallback-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
    }
    
    with open("fallback-credentials.json", "w") as f:
        json.dump(fallback_credentials, f, indent=2)
    
    print("✅ Fallback mode configured")
    return True

def create_test_data():
    """Create test data for fallback mode."""
    print("📊 Creating test data...")
    
    test_schemes = {
        "education_schemes": [
            {
                "name": "Test Education Grant",
                "min_children": 1,
                "max_monthly_income": 50000,
                "description": "Test education grant for demonstration purposes",
                "benefits": "Monthly stipend of PKR 1,000 per child",
                "required_documents": ["CNIC", "Children's birth certificates", "Income certificate"],
                "application_process": "Apply online through test portal",
                "helpline": "0800-TEST-01",
                "website": "https://test-education.gov.pk"
            }
        ],
        "healthcare_schemes": [
            {
                "name": "Test Health Card",
                "income_limit": 60000,
                "description": "Test health card for demonstration purposes",
                "benefits": "Free treatment at test hospitals",
                "required_documents": ["CNIC", "Income certificate", "Recent photograph"],
                "application_process": "Apply at test health centers",
                "helpline": "0800-TEST-02",
                "website": "https://test-health.gov.pk"
            }
        ]
    }
    
    with open("test_schemes.json", "w") as f:
        json.dump(test_schemes, f, indent=2)
    
    print("✅ Test data created")
    return True

def main():
    """Main fallback setup function."""
    print("🔄 Citizen Bot Pakistan - Fallback Setup")
    print("=" * 40)
    
    setup_fallback_environment()
    create_test_data()
    
    print("\n" + "=" * 40)
    print("✅ Fallback setup completed!")
    print("\n📋 You can now run the app in fallback mode:")
    print("   python app.py")
    print("\n⚠️  Note: This uses fallback explanations instead of AI.")
    print("   For full functionality, complete the Google Cloud setup.")

if __name__ == "__main__":
    main()

