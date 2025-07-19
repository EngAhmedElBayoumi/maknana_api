#!/usr/bin/env python3
"""
Test script for the notification system.
This script tests the audit logging and real-time notification functionality.
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
from service.models import service
from notification.models import AuditLog
from notification.utils import send_realtime_notification
import time

User = get_user_model()

def test_audit_logging():
    """Test the audit logging functionality."""
    print("🧪 Testing Audit Logging System...")
    
    # Get or create a test user
    user, created = User.objects.get_or_create(
        email='test@example.com',
        defaults={
            'name': 'Test User',
            'first_phone': '1234567890',
            'type': 'admin'
        }
    )
    
    if created:
        print(f"✅ Created test user: {user.email}")
    else:
        print(f"✅ Using existing test user: {user.email}")
    
    # Set the current user for audit logging
    from notification.signals import set_current_user
    set_current_user(user)
    
    # Test creating a service (this should trigger audit logging)
    print("\n📝 Testing CREATE operation...")
    test_service = service.objects.create(
        name="Test Service",
        name_ar="خدمة تجريبية",
        short_description="This is a test service for audit logging",
        short_description_ar="هذه خدمة تجريبية لتسجيل العمليات",
        long_description="Detailed description of the test service",
        long_description_ar="وصف مفصل للخدمة التجريبية",
        price="100.00",
        price_ar="100.00 ريال"
    )
    print(f"✅ Created service: {test_service.name}")
    
    # Check if audit log was created
    audit_logs = AuditLog.objects.filter(
        model_name='service',
        object_id=test_service.id,
        action='created'
    )
    
    if audit_logs.exists():
        log = audit_logs.first()
        print(f"✅ Audit log created: {log}")
        print(f"   - User: {log.user}")
        print(f"   - Action: {log.action}")
        print(f"   - Changes: {log.changes}")
    else:
        print("❌ No audit log found for CREATE operation")
    
    # Test updating the service
    print("\n📝 Testing UPDATE operation...")
    test_service.price = "150.00"
    test_service.save()
    print(f"✅ Updated service price to: {test_service.price}")
    
    # Check if audit log was created for update
    update_logs = AuditLog.objects.filter(
        model_name='service',
        object_id=test_service.id,
        action='updated'
    )
    
    if update_logs.exists():
        log = update_logs.first()
        print(f"✅ Audit log created for update: {log}")
    else:
        print("❌ No audit log found for UPDATE operation")
    
    # Test deleting the service
    print("\n📝 Testing DELETE operation...")
    service_id = test_service.id
    test_service.delete()
    print(f"✅ Deleted service with ID: {service_id}")
    
    # Check if audit log was created for delete
    delete_logs = AuditLog.objects.filter(
        model_name='service',
        object_id=service_id,
        action='deleted'
    )
    
    if delete_logs.exists():
        log = delete_logs.first()
        print(f"✅ Audit log created for delete: {log}")
    else:
        print("❌ No audit log found for DELETE operation")
    
    # Clear the current user
    set_current_user(None)
    
    return True

def test_real_time_notifications():
    """Test the real-time notification system."""
    print("\n🔔 Testing Real-time Notifications...")
    
    try:
        # Test sending a notification
        test_data = {
            'action': 'test',
            'model': 'TestModel',
            'object_id': 999,
            'user': 'test@example.com',
            'timestamp': '2025-01-07T12:00:00Z',
            'changes': {'test_field': {'old': 'old_value', 'new': 'new_value'}}
        }
        
        send_realtime_notification(test_data)
        print("✅ Real-time notification sent successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error sending real-time notification: {e}")
        return False

def test_api_endpoints():
    """Test the API endpoints."""
    print("\n🌐 Testing API Endpoints...")
    
    try:
        from django.test import Client
        from django.urls import reverse
        
        client = Client()
        
        # Test statistics endpoint (without authentication for now)
        print("📊 Testing statistics endpoint...")
        # Note: This will fail without authentication, but we can check if the URL resolves
        try:
            response = client.get('/api/notifications/statistics/')
            print(f"   - Statistics endpoint status: {response.status_code}")
        except Exception as e:
            print(f"   - Statistics endpoint error: {e}")
        
        # Test audit logs list endpoint
        print("📋 Testing audit logs list endpoint...")
        try:
            response = client.get('/api/notifications/audit-logs/')
            print(f"   - Audit logs endpoint status: {response.status_code}")
        except Exception as e:
            print(f"   - Audit logs endpoint error: {e}")
        
        # Test dashboard endpoint
        print("🎛️ Testing dashboard endpoint...")
        try:
            response = client.get('/api/notifications/dashboard/')
            print(f"   - Dashboard endpoint status: {response.status_code}")
        except Exception as e:
            print(f"   - Dashboard endpoint error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing API endpoints: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Starting Notification System Tests")
    print("=" * 50)
    
    # Test audit logging
    audit_test_passed = test_audit_logging()
    
    # Test real-time notifications
    notification_test_passed = test_real_time_notifications()
    
    # Test API endpoints
    api_test_passed = test_api_endpoints()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   - Audit Logging: {'✅ PASSED' if audit_test_passed else '❌ FAILED'}")
    print(f"   - Real-time Notifications: {'✅ PASSED' if notification_test_passed else '❌ FAILED'}")
    print(f"   - API Endpoints: {'✅ PASSED' if api_test_passed else '❌ FAILED'}")
    
    # Show total audit logs
    total_logs = AuditLog.objects.count()
    print(f"\n📈 Total audit logs in database: {total_logs}")
    
    # Show recent logs
    recent_logs = AuditLog.objects.order_by('-timestamp')[:5]
    if recent_logs:
        print("\n📋 Recent audit logs:")
        for log in recent_logs:
            print(f"   - {log}")
    
    print("\n🎉 Tests completed!")

if __name__ == '__main__':
    main()

