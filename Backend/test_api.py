#!/usr/bin/env python3
"""
Simple API test script to verify the backend is working.
Run this after starting the API server.
"""

import requests
import json
import time

def test_api():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Sentinel Ledger API...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        print("   Make sure the API server is running on port 8000")
        return False
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Service: {response.json().get('service')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing root endpoint: {e}")
    
    # Test tokens endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/tokens")
        if response.status_code == 200:
            print("✅ Tokens endpoint working")
            data = response.json()
            print(f"   Found {data.get('total', 0)} tokens")
        else:
            print(f"❌ Tokens endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing tokens endpoint: {e}")
    
    # Test docs endpoint
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ API documentation available")
            print(f"   Docs URL: {base_url}/docs")
        else:
            print(f"❌ Docs endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing docs endpoint: {e}")
    
    print("\n🎉 API test completed!")
    return True

if __name__ == "__main__":
    test_api()
