#!/usr/bin/env python3
"""
Test script to verify login endpoint
"""
import requests
import json

def test_login():
    """Test the login endpoint"""
    print("🔍 Testing Login Endpoint")
    print("=" * 40)
    
    # Test credentials (you may need to adjust these)
    credentials = {
        "username": "lokesh_04",
        "password": "testpass123"  # You'll need to set this password
    }
    
    try:
        # Test login endpoint
        response = requests.post(
            "http://localhost:8000/api/auth/token/",
            json=credentials,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"Access Token: {data.get('access', 'N/A')[:20]}...")
            print(f"Refresh Token: {data.get('refresh', 'N/A')[:20]}...")
            
            # Test profile endpoint with the token
            headers = {"Authorization": f"Bearer {data['access']}"}
            profile_response = requests.get(
                "http://localhost:8000/api/auth/profile/",
                headers=headers
            )
            
            if profile_response.status_code == 200:
                profile_data = profile_response.json()
                print(f"✅ Profile retrieved: {profile_data.get('username', 'N/A')}")
            else:
                print(f"❌ Profile failed: {profile_response.status_code}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Django server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login() 