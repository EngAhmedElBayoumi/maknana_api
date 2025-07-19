#!/usr/bin/env python3
"""
Test the API response directly using requests.
"""

import requests
import json

def test_api_response():
    """Test the actual API response."""
    print("🌐 Testing API Response Directly...")
    
    # Test the audit logs API
    url = "http://127.0.0.1:8001/api/notifications/audit-logs/"
    
    try:
        response = requests.get(url)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {data.get('count', 0)} audit logs")
            
            results = data.get('results', [])
            if results:
                print("\n📋 First few logs:")
                for i, log in enumerate(results[:3]):
                    print(f"   Log {i+1}:")
                    for key, value in log.items():
                        print(f"     - {key}: {value}")
                    print()
                
                # Check if user fields are present
                first_log = results[0]
                has_user_email = 'user_email' in first_log
                has_user_name = 'user_name' in first_log
                
                print(f"🔍 User fields check:")
                print(f"   - user_email present: {has_user_email}")
                print(f"   - user_name present: {has_user_name}")
                
                if has_user_email and has_user_name:
                    print("✅ User fields are properly included")
                else:
                    print("❌ User fields are missing")
                    print(f"   Available fields: {list(first_log.keys())}")
            else:
                print("ℹ️ No audit logs found")
        else:
            print(f"❌ API request failed: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Django server")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_api_response()

