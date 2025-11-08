"""
Voiceflow API Test Script
This script helps verify your Voiceflow API setup before running the main application.
"""

import requests
import json
import sys

def test_api_key(api_key):
    """Test if the API key is valid by making a simple request"""
    try:
        # Test with a simple launch request
        response = requests.post(
            'https://general-runtime.voiceflow.com/state/user/test_user/interact',
            json={'request': {'type': 'launch'}},
            headers={
                'Authorization': api_key,
                'versionID': 'production'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data:  # Non-empty response
                print("API Key is valid and project is accessible")
                print(f"   Response contains {len(data)} trace(s)")
                return True
            else:
                print("API Key works but returned empty response")
                print("   Make sure your Voiceflow project is published")
                return False
        elif response.status_code == 401:
            print("API Key is invalid or unauthorized")
            return False
        elif response.status_code == 404:
            print("Project not found - check your API key")
            return False
        else:
            print(f"API request failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("Request timed out - check your internet connection")
        return False
    except requests.exceptions.ConnectionError:
        print("Connection error - check your internet connection")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def test_transcripts_api(api_key, project_id, version_id):
    """Test the Transcripts API configuration"""
    try:
        url = "https://api.voiceflow.com/v2/transcripts"
        
        payload = {
            "projectID": project_id,
            "versionID": version_id,
            "sessionID": "test_session"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": api_key
        }
        
        response = requests.put(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code in [200, 201]:
            print("Transcripts API is working correctly")
            return True
        elif response.status_code == 401:
            print("Transcripts API: Unauthorized - check your API key")
            return False
        elif response.status_code == 400:
            print("Transcripts API: Bad request - check Project ID and Version ID")
            return False
        else:
            print(f"Transcripts API failed with status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Transcripts API test error: {e}")
        return False

def main():
    print("Voiceflow API Configuration Test")
    print("=" * 50)
    
    # Try to import configuration
    try:
        from config import API_KEY, PROJECT_ID, VERSION_ID
        print("Configuration file (config.py) found")
        api_key = API_KEY
        project_id = PROJECT_ID
        version_id = VERSION_ID
    except ImportError:
        print("No config.py file found, using manual input")
        api_key = input("Enter your Voiceflow API Key: ").strip()
        project_id = input("Enter your Project ID (or press Enter to skip transcripts test): ").strip()
        version_id = input("Enter your Version ID (or press Enter to skip transcripts test): ").strip()
    
    print(f"\nTesting Configuration:")
    print(f"   API Key: {api_key[:15]}..." + "*" * 20 if api_key else "Not provided")
    print(f"   Project ID: {project_id if project_id else 'Not provided'}")
    print(f"   Version ID: {version_id if version_id else 'Not provided'}")
    
    # Test 1: Basic API Key validation
    print(f"\n1. Testing API Key format...")
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        print("API Key is not configured")
        sys.exit(1)
    
    if not api_key.startswith('VF.DM.'):
        print("API Key format appears incorrect (should start with 'VF.DM.')")
        sys.exit(1)
    
    print("API Key format is correct")
    
    # Test 2: Dialog Manager API
    print(f"\n2. Testing Dialog Manager API...")
    dm_success = test_api_key(api_key)
    
    # Test 3: Transcripts API (if configured)
    if project_id and version_id and project_id != 'YOUR_PROJECT_ID_HERE' and version_id != 'YOUR_VERSION_ID_HERE':
        print(f"\n3. Testing Transcripts API...")
        transcripts_success = test_transcripts_api(api_key, project_id, version_id)
    else:
        print(f"\n3. Skipping Transcripts API test (Project ID or Version ID not configured)")
        transcripts_success = None
    
    # Summary
    print(f"\n" + "=" * 50)
    print("Test Summary:")
    print(f"   Dialog Manager API: {'Pass' if dm_success else 'Fail'}")
    
    if transcripts_success is not None:
        print(f"   Transcripts API: {'Pass' if transcripts_success else 'Fail'}")
    else:
        print(f"   Transcripts API: Skipped")
    
    if dm_success:
        print(f"\nYour setup is ready! You can now run VoiceflowAPIGuide.py")
        if transcripts_success is False:
            print("   Note: Chat will work, but transcripts won't be saved")
    else:
        print(f"\nSetup issues found. Please fix the above errors before continuing.")
        print("   Common fixes:")
        print("   - Make sure your Voiceflow project is published")
        print("   - Verify your API key is correct and complete")
        print("   - Check your internet connection")

if __name__ == "__main__":
    main()