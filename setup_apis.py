#!/usr/bin/env python3
"""
Setup script to enable required Google Cloud APIs for the Citizen Bot Pakistan project.
This script helps enable the necessary APIs for the AI agent to work properly.
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def enable_api(api_name, project_id):
    """Enable a specific API for the project."""
    print(f"Enabling {api_name} for project {project_id}...")
    
    command = f"gcloud services enable {api_name} --project={project_id}"
    success, stdout, stderr = run_command(command)
    
    if success:
        print(f"✅ Successfully enabled {api_name}")
        return True
    else:
        print(f"❌ Failed to enable {api_name}: {stderr}")
        return False

def main():
    """Main function to enable required APIs."""
    project_id = "ultimate-realm-473419-c7"
    
    print("🚀 Setting up Google Cloud APIs for Citizen Bot Pakistan")
    print(f"Project ID: {project_id}")
    print("-" * 50)
    
    # Required APIs for Vertex AI
    required_apis = [
        "aiplatform.googleapis.com",  # Vertex AI API
        "generativelanguage.googleapis.com",  # Generative Language API
        "compute.googleapis.com",  # Compute Engine API (often required)
    ]
    
    print("Required APIs:")
    for api in required_apis:
        print(f"  - {api}")
    print()
    
    # Check if gcloud is installed
    success, _, _ = run_command("gcloud --version")
    if not success:
        print("❌ Google Cloud CLI (gcloud) is not installed or not in PATH.")
        print("Please install it from: https://cloud.google.com/sdk/docs/install")
        return False
    
    print("✅ Google Cloud CLI found")
    
    # Authenticate if needed
    print("Checking authentication...")
    success, stdout, stderr = run_command("gcloud auth list --filter=status:ACTIVE --format=value(account)")
    if not success or not stdout.strip():
        print("❌ Not authenticated with Google Cloud.")
        print("Please run: gcloud auth login")
        return False
    
    print(f"✅ Authenticated as: {stdout.strip()}")
    
    # Enable APIs
    print("\nEnabling required APIs...")
    success_count = 0
    
    for api in required_apis:
        if enable_api(api, project_id):
            success_count += 1
    
    print(f"\n📊 Results: {success_count}/{len(required_apis)} APIs enabled successfully")
    
    if success_count == len(required_apis):
        print("🎉 All APIs enabled successfully!")
        print("\nYou can now run the agent with:")
        print("  python agents.py")
        return True
    else:
        print("⚠️  Some APIs failed to enable. You may need to:")
        print("  1. Check your project permissions")
        print("  2. Enable APIs manually in the Google Cloud Console")
        print("  3. Wait a few minutes for changes to propagate")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
