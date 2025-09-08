#!/usr/bin/env python3
"""
Simple test script to verify authentication endpoints
"""
import requests
import json

def test_auth_endpoints():
    """Test basic authentication endpoints"""
    print("🔍 Testing Authentication Endpoints")
    print("=" * 50)
    
    base_url = "http://localhost:8000/api"
    
    # Test 1: Check if server is running
    try:
        response = requests.get("http://localhost:8000/")
        print(f"✅ Server is running: {response.status_code}")
    except Exception as e:
        print(f"❌ Server not accessible: {e}")
        return
    
    # Test 2: Test registration endpoint
    print("\n📝 Testing Registration Endpoint:")
    try:
        register_data = {
            "username": "testuser123",
            "email": "testuser123@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123"
        }
        
        response = requests.post(f"{base_url}/auth/register/", json=register_data)
        print(f"Registration Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            data = response.json()
            print(f"User created: {data.get('user', {}).get('username', 'N/A')}")
        else:
            print(f"❌ Registration failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
    
    # Test 3: Test login endpoint
    print("\n🔐 Testing Login Endpoint:")
    try:
        login_data = {
            "username": "testuser123",
            "password": "testpass123"
        }
        
        response = requests.post(f"{base_url}/auth/token/", json=login_data)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            data = response.json()
            print(f"Access Token: {data.get('access', 'N/A')[:20]}...")
            print(f"Refresh Token: {data.get('refresh', 'N/A')[:20]}...")
            
            # Test 4: Test profile endpoint
            print("\n👤 Testing Profile Endpoint:")
            headers = {"Authorization": f"Bearer {data['access']}"}
            profile_response = requests.get(f"{base_url}/auth/profile/", headers=headers)
            
            if profile_response.status_code == 200:
                profile_data = profile_response.json()
                print(f"✅ Profile retrieved: {profile_data.get('username', 'N/A')}")
            else:
                print(f"❌ Profile failed: {profile_response.status_code}")
                
        else:
            print(f"❌ Login failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Ready for frontend testing!")
    print("\n📋 Test Steps:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Try registering a new account")
    print("3. Try logging in with the registered account")
    print("4. Check if you're redirected to dashboard")
    print("\n🔧 Debug Info:")
    print("- Check browser console for detailed logs")
    print("- Check Django logs for backend errors")
    print("- Use the debug components on login/register pages")

if __name__ == "__main__":
    test_auth_endpoints() 