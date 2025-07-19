from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model

User = get_user_model()

def get_user_from_request(request):
    """
    Extract user from request, supporting both session and JWT authentication.
    """
    user = None
    
    # First, try session authentication
    if hasattr(request, 'user') and request.user.is_authenticated:
        user = request.user
        return user
    
    # Then try JWT authentication
    if hasattr(request, 'META') and 'HTTP_AUTHORIZATION' in request.META:
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            try:
                jwt_auth = JWTAuthentication()
                raw_token = jwt_auth.get_raw_token(jwt_auth.get_header(request))
                if raw_token:
                    validated_token = jwt_auth.get_validated_token(raw_token)
                    user = jwt_auth.get_user(validated_token)
            except (InvalidToken, TokenError, Exception):
                # If JWT authentication fails, user remains None
                pass
    
    return user

def extract_user_info(user):
    """
    Extract user information for logging purposes.
    """
    if user and user.is_authenticated:
        return {
            'id': user.id,
            'email': getattr(user, 'email', None),
            'name': getattr(user, 'name', None),
            'is_authenticated': True
        }
    return {
        'id': None,
        'email': None,
        'name': None,
        'is_authenticated': False
    }

