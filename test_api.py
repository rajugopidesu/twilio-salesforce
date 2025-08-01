#!/usr/bin/env python3
"""
Test script for the Twilio Transcription API
Run this to test your local Flask app before deploying to Render
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5000"  # Change this to your Render URL after deployment

def test_health():
    """Test the health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_home():
    """Test the home endpoint"""
    print("\n🏠 Testing home endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Home endpoint failed: {e}")
        return False

def test_transcribe():
    """Test the transcribe endpoint"""
    print("\n🎤 Testing transcribe endpoint...")
    
    # Test data - UPDATE THESE WITH YOUR ACTUAL VALUES
    test_data = {
        "account_sid": "your_account_sid_here",
        "auth_token": "your_auth_token_here",
        "recording_sid": "REyour_recording_sid_here",
        "whisper_model_size": "base"
    }
    
    print("⚠️  WARNING: Using placeholder credentials!")
    print("   Update the test_data in this script with your actual Twilio credentials")
    print(f"   Test data: {json.dumps(test_data, indent=2)}")
    
    # Ask user if they want to proceed
    proceed = input("\nDo you want to proceed with the test? (y/N): ").lower().strip()
    if proceed != 'y':
        print("❌ Test cancelled by user")
        return False
    
    try:
        response = requests.post(
            f"{BASE_URL}/transcribe",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Transcription successful!")
            print(f"Transcript: {result.get('transcript', 'No transcript')}")
            print(f"Recording SID: {result.get('recording_sid')}")
            print(f"Model Size: {result.get('model_size')}")
        else:
            print(f"❌ Transcription failed: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Transcribe test failed: {e}")
        return False

def test_invalid_request():
    """Test with invalid data"""
    print("\n🚫 Testing invalid request...")
    
    invalid_data = {
        "account_sid": "invalid_sid",
        # Missing auth_token and recording_sid
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/transcribe",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Should return 400 for bad request
        return response.status_code == 400
        
    except Exception as e:
        print(f"❌ Invalid request test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Twilio Transcription API")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Home Endpoint", test_home),
        ("Invalid Request", test_invalid_request),
        ("Transcribe", test_transcribe)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your API is ready for deployment.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main() 