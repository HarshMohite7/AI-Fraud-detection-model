import requests
import sys

BASE_URL = "http://127.0.0.1:5000/api"

def check_profile(email, password):
    # 1. Login
    print(f"Logging in as {email}...")
    try:
        login_res = requests.post(f"{BASE_URL}/login", json={"username": email, "password": password})
        
        if login_res.status_code != 200:
            print(f"Login failed: {login_res.status_code} - {login_res.text}")
            return

        data = login_res.json()
        token = data.get("access_token")
        print(f"Login successful. Token received (len={len(token) if token else 0})")
        
        if not token:
            print("No token in response!")
            return

    except Exception as e:
        print(f"Error during login: {e}")
        return

    # 2. Get Profile
    print("Fetching profile...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        profile_res = requests.get(f"{BASE_URL}/profile", headers=headers)
        
        print(f"Profile Response Code: {profile_res.status_code}")
        print(f"Profile Response Body: {profile_res.text}")
        
    except Exception as e:
        print(f"Error fetching profile: {e}")

if __name__ == "__main__":
    # Create test user
    try:
        signup_res = requests.post(f"{BASE_URL}/signup", json={
            "name": "Test User",
            "email": "testdebug@example.com",
            "password": "password123"
        })
        print(f"Signup attempt: {signup_res.status_code}")
    except:
        pass

    check_profile("testdebug@example.com", "password123")
