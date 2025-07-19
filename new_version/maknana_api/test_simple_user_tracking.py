#!/usr/bin/env python3
"""
Simple test to verify user tracking in the notification system.
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
from notification.signals import set_current_user

User = get_user_model()

def test_direct_user_tracking():
    """Test user tracking by directly setting the user."""
    print("🔐 Testing Direct User Tracking...")
    
    # Create or get a test user
    user, created = User.objects.get_or_create(
        email='direct_test@example.com',
        defaults={
            'name': 'Direct Test User',
            'first_phone': '1234567890',
            'type': 'admin'
        }
    )
    
    if created:
        print(f"✅ Created test user: {user.email}")
    else:
        print(f"✅ Using existing test user: {user.email}")
    
    # Set the current user manually
    set_current_user(user)
    
    # Create a service (this should trigger audit logging with the user)
    print("\n📝 Creating service with user set...")
    
    test_service = service.objects.create(
        name="Direct Test Service",
        name_ar="خدمة اختبار مباشر",
        short_description="Test service with direct user tracking",
        short_description_ar="خدمة تجريبية مع تتبع مباشر للمستخدم",
        long_description="Detailed description for direct test",
        long_description_ar="وصف مفصل للاختبار المباشر",
        price="300.00",
        price_ar="300.00 ريال"
    )
    
    print(f"✅ Service created: {test_service.name}")
    
    # Check if audit log was created with correct user
    audit_logs = AuditLog.objects.filter(
        model_name='service',
        object_id=test_service.id,
        action='created'
    ).order_by('-timestamp')
    
    if audit_logs.exists():
        log = audit_logs.first()
        print(f"✅ Audit log created:")
        print(f"   - Log ID: {log.id}")
        print(f"   - User: {log.user.email if log.user else 'None'}")
        print(f"   - Action: {log.action}")
        print(f"   - Model: {log.model_name}")
        print(f"   - Object ID: {log.object_id}")
        print(f"   - Timestamp: {log.timestamp}")
        
        if log.user and log.user.email == user.email:
            print("✅ User tracking is working correctly!")
            success = True
        else:
            print("❌ User tracking failed - user is not set correctly")
            success = False
    else:
        print("❌ No audit log found")
        success = False
    
    # Clear the user
    set_current_user(None)
    
    # Clean up - delete the test service
    test_service.delete()
    print(f"🗑️ Cleaned up test service")
    
    return success

def test_api_response_format():
    """Test the API response format for audit logs."""
    print("\n🌐 Testing API Response Format...")
    
    from notification.serializers import AuditLogListSerializer
    
    # Get recent audit logs
    recent_logs = AuditLog.objects.select_related('user').order_by('-timestamp')[:3]
    
    if recent_logs:
        print(f"📋 Found {len(recent_logs)} recent logs")
        
        # Serialize the logs
        serializer = AuditLogListSerializer(recent_logs, many=True)
        data = serializer.data
        
        print("📊 Serialized data sample:")
        for i, log_data in enumerate(data):
            print(f"   Log {i+1}:")
            print(f"     - ID: {log_data.get('id')}")
            print(f"     - User Email: {log_data.get('user_email')}")
            print(f"     - User Name: {log_data.get('user_name')}")
            print(f"     - Action: {log_data.get('action')}")
            print(f"     - Model: {log_data.get('model_name')}")
            print(f"     - Object ID: {log_data.get('object_id')}")
            print(f"     - Timestamp: {log_data.get('timestamp')}")
            print()
        
        # Check if user fields are properly included
        has_user_email_field = 'user_email' in data[0]
        has_user_name_field = 'user_name' in data[0]
        
        print(f"🔍 Checking fields in first log: {list(data[0].keys())}")
        
        if has_user_email_field and has_user_name_field:
            print("✅ User fields are properly included in serializer")
            return True
        else:
            print("❌ User fields are missing from serializer")
            print(f"   - user_email present: {has_user_email_field}")
            print(f"   - user_name present: {has_user_name_field}")
            return False
    else:
        print("ℹ️ No audit logs found")
        return True

def main():
    """Main test function."""
    print("🚀 Starting Simple User Tracking Tests")
    print("=" * 50)
    
    # Test direct user tracking
    direct_test_passed = test_direct_user_tracking()
    
    # Test API response format
    api_format_test_passed = test_api_response_format()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   - Direct User Tracking: {'✅ PASSED' if direct_test_passed else '❌ FAILED'}")
    print(f"   - API Format Test: {'✅ PASSED' if api_format_test_passed else '❌ FAILED'}")
    
    # Show all audit logs with user information
    all_logs = AuditLog.objects.select_related('user').order_by('-timestamp')[:10]
    if all_logs:
        print("\n📋 All recent audit logs:")
        for log in all_logs:
            user_info = f"{log.user.email} ({log.user.name})" if log.user else "Anonymous"
            print(f"   - ID {log.id}: {user_info} {log.action} {log.model_name}({log.object_id}) at {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n🎉 Simple user tracking tests completed!")

if __name__ == '__main__':
    main()

