#!/usr/bin/env python3
"""
Test script for Citizen Bot Pakistan
This script tests the application to ensure it's working properly.
"""

import sys
import os
import json
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import vertexai
        print("✅ Vertex AI imported successfully")
    except ImportError as e:
        print(f"⚠️  Vertex AI import failed: {e}")
        print("🔄 Will use fallback mode")
    
    try:
        from multi_agents import AgentOrchestrator
        print("✅ Multi-agents imported successfully")
    except ImportError as e:
        print(f"❌ Multi-agents import failed: {e}")
        return False
    
    return True

def test_fallback_mode():
    """Test fallback mode functionality."""
    print("\n🔄 Testing fallback mode...")
    
    # Set fallback mode
    os.environ['FALLBACK_MODE'] = 'true'
    
    try:
        from multi_agents import AgentOrchestrator
        orchestrator = AgentOrchestrator()
        
        # Test with sample data
        test_issue = "I need help with my children's education expenses. My monthly income is 25,000 and I have 3 children."
        test_user_info = {
            "monthly_income": 25000,
            "number_of_children": 3,
            "children_ages": [8, 12, 15],
            "location": "Karachi"
        }
        
        result = orchestrator.solve_user_issue(test_issue, test_user_info)
        
        if result.get("status") == "success":
            print("✅ Fallback mode test passed")
            print(f"📊 Found {len(result.get('scheme_details', []))} relevant schemes")
            return True
        else:
            print(f"❌ Fallback mode test failed: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Fallback mode test failed with exception: {e}")
        return False

def test_flask_app():
    """Test Flask application."""
    print("\n🌐 Testing Flask application...")
    
    try:
        from app import app
        
        # Test app creation
        with app.test_client() as client:
            # Test home page
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home page loads successfully")
            else:
                print(f"❌ Home page failed: {response.status_code}")
                return False
            
            # Test API endpoints
            response = client.get('/api/schemes')
            if response.status_code == 200:
                print("✅ Schemes API works")
            else:
                print(f"❌ Schemes API failed: {response.status_code}")
                return False
            
            # Test issue submission
            test_data = {
                "issue": "I need help with education expenses",
                "user_info": {
                    "monthly_income": 25000,
                    "family_size": 4,
                    "location": "Karachi"
                }
            }
            
            response = client.post('/submit-issue', 
                                 json=test_data,
                                 content_type='application/json')
            
            if response.status_code == 200:
                print("✅ Issue submission works")
                data = response.get_json()
                if data.get("status") == "success":
                    print("✅ AI analysis works")
                else:
                    print(f"⚠️  AI analysis returned: {data.get('status')}")
            else:
                print(f"❌ Issue submission failed: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist."""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "app.py",
        "multi_agents.py",
        "requirements.txt",
        "templates/index.html",
        "templates/about.html",
        "templates/help.html"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path} exists")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    return True

def main():
    """Main test function."""
    print("🧪 Citizen Bot Pakistan - Test Suite")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Fallback Mode", test_fallback_mode),
        ("Flask App", test_flask_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test passed")
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The app is ready to run.")
        print("\n🚀 To start the application:")
        print("   python app.py")
        print("   Then visit: http://localhost:5000")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Run: pip install -r requirements.txt")
        print("   2. Check file permissions")
        print("   3. Verify Python version (3.8+)")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

