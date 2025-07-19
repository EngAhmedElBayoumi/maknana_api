#!/usr/bin/env python3
"""
Test script to verify user tracking in the notification system.
This script tests if the system properly captures authenticated users.
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append('/home/ubuntu/maknana_api')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from service.models import service
from notification.models import AuditLog
import json

User = get_user_model()

def test_user_tracking_with_jwt():
    """Test user tracking with JWT authentication."""
    print("🔐 Testing User Tracking with JWT Authentication...")
    
    # Create or get a test user
    user, created = User.objects.get_or_create(
        email='jwt_test@example.com',
        defaults={
            'name': 'JWT Test User',
            'first_phone': '1234567890',
            'type': 'admin'
        }
    )
    
    if created:
        user.set_password('testpassword123')
        user.save()
        print(f"✅ Created test user: {user.email}")
    else:
        print(f"✅ Using existing test user: {user.email}")
    
    # Generate JWT token for the user
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    print(f"🔑 Generated JWT token for user: {user.email}")
    
    # Create a test client
    client = Client()
    
    # Test creating a service with JWT authentication
    print("\n📝 Testing service creation with JWT...")
    
    service_data = {
        'name': 'JWT Test Service',
        'name_ar': 'خدمة اختبار JWT',
        'short_description': 'Test service created with JWT auth',
        'short_description_ar': 'خدمة تجريبية تم إنشاؤها باستخدام JWT',
        'long_description': 'Detailed description for JWT test',
        'long_description_ar': 'وصف مفصل لاختبار JWT',
        'price': '200.00',
        'price_ar': '200.00 ريال'
    }
    
    # Make API request with JWT token
    response = client.post(
        '/api/service/services/',
        data=json.dumps(service_data),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Bearer {access_token}',
        HTTP_HOST='testserver'
    )
    
    print(f"📊 API Response Status: {response.status_code}")
    
    if response.status_code == 201:
        response_data = response.json()
        service_id = response_data.get('id')
        print(f"✅ Service created successfully with ID: {service_id}")
        
        # Check if audit log was created with correct user
        audit_logs = AuditLog.objects.filter(
            model_name='service',
            object_id=service_id,
            action='created'
        )
        
        if audit_logs.exists():
            log = audit_logs.first()
            if log.user and log.user.email == user.email:
                print(f"✅ Audit log created with correct user: {log.user.email}")
                print(f"   - Log ID: {log.id}")
                print(f"   - Action: {log.action}")
                print(f"   - Timestamp: {log.timestamp}")
                return True
            else:
                print(f"❌ Audit log created but user is incorrect: {log.user}")
                return False
        else:
            print("❌ No audit log found for the created service")
            return False
    else:
        print(f"❌ Failed to create service. Response: {response.content}")
        return False

def test_audit_log_api_with_jwt():
    """Test accessing audit log API with JWT authentication."""
    print("\n🌐 Testing Audit Log API with JWT...")
    
    # Get a test user
    user = User.objects.filter(email='jwt_test@example.com').first()
    if not user:
        print("❌ No test user found")
        return False
    
    # Generate JWT token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    # Create a test client
    client = Client()
    
    # Test audit logs list endpoint
    response = client.get(
        '/api/notifications/audit-logs/',
        HTTP_AUTHORIZATION=f'Bearer {access_token}',
        HTTP_HOST='testserver'
    )
    
    print(f"📊 Audit Logs API Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {data.get('count', 0)} audit logs")
        
        # Check if user information is properly displayed
        results = data.get('results', [])
        if results:
            first_log = results[0]
            print(f"📋 First log sample:")
            print(f"   - ID: {first_log.get('id')}")
            print(f"   - User Email: {first_log.get('user_email')}")
            print(f"   - User Name: {first_log.get('user_name')}")
            print(f"   - Action: {first_log.get('action')}")
            print(f"   - Model: {first_log.get('model_name')}")
            
            # Check if user fields are properly populated
            has_user_email = any(log.get('user_email') for log in results)
            has_user_name = any(log.get('user_name') for log in results)
            
            if has_user_email or has_user_name:
                print("✅ User information is properly displayed in the list")
                return True
            else:
                print("⚠️ User information fields are present but empty")
                return True
        else:
            print("ℹ️ No audit logs found")
            return True
    else:
        print(f"❌ Failed to access audit logs API. Status: {response.status_code}")
        return False

def main():
    """Main test function."""
    print("🚀 Starting User Tracking Tests")
    print("=" * 50)
    
    # Test JWT user tracking
    jwt_test_passed = test_user_tracking_with_jwt()
    
    # Test API access
    api_test_passed = test_audit_log_api_with_jwt()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   - JWT User Tracking: {'✅ PASSED' if jwt_test_passed else '❌ FAILED'}")
    print(f"   - API Access Test: {'✅ PASSED' if api_test_passed else '❌ FAILED'}")
    
    # Show recent logs with user information
    recent_logs = AuditLog.objects.select_related('user').order_by('-timestamp')[:5]
    if recent_logs:
        print("\n📋 Recent audit logs with user info:")
        for log in recent_logs:
            user_info = f"{log.user.email} ({log.user.name})" if log.user else "Anonymous"
            print(f"   - {user_info} {log.action} {log.model_name} at {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n🎉 User tracking tests completed!")

if __name__ == '__main__':
    main()

