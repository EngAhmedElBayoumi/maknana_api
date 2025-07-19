from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .permission_group_apis import *

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'user_profiles', UserProfileViewSet, basename='user_profile')
router.register(r'permissions-groups', PermissionGroupViewSet, basename='permissions-groups')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set_new_password'),
    path('send-verification-email/', SendVerificationEmailView.as_view(), name='send_verification_email'),
    path('send-reset-password-email/', SendResetPasswordEmailView.as_view(), name='send_reset_password_email'),
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('technicians/', TechnicianListView.as_view(), name='technician-list'),
    path('resend-reset-code/', ResendResetCodeView.as_view(), name='resend_reset_code'),
    path('confirm-reset-code/', ConfirmResetCodeView.as_view(), name='confirm_reset_code'),
]

urlpatterns += router.urls