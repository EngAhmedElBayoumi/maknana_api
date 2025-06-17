from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import EmailService, CodeGenerator
from .models import CustomUser as User
from .serializers import (
    RegisterSerializer, LoginSerializer, VerifyEmailSerializer,
    ResetPasswordSerializer, SetNewPasswordSerializer, UserSerializer
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.viewsets import ModelViewSet
from .models import CustomUser
from .serializers import UserProfileSerializer
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .utils import get_model_search_fields


class Pagination(PageNumberPagination):
    page_size = 10

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: 'User registered successfully',
            400: 'Invalid data provided'
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            code = CodeGenerator.generate_code()
            user.activation_code = code
            user.save()
            EmailService.send_verification_email(user.email, code)
            return Response({'status_code': 201, 'data': 'User registered successfully. Please verify your email.'}, status=status.HTTP_201_CREATED)
        return Response({'status_code': 400, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: 'Login successful',
            400: 'Invalid credentials, disabled account, or unverified account'
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            # Get permissions
            permissions = {}
            for perm in user.get_all_permissions():
                app_label, codename = perm.split('.')
                permissions[codename] = True

            # Get groups
            groups = [{'id': group.id, 'name': group.name} for group in user.groups.all()]

            # Get photo URL instead of photo field
            photo_url = None
            if user.photo:
                photo_url = request.build_absolute_uri(user.photo.url) if user.photo else None

            return Response({
                'status_code': 200,
                'data': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'name': user.name,
                    'type': user.type,
                    'id': user.id,
                    "first_phone": user.first_phone,
                    "second_phone": user.second_phone,
                    "email": user.email,
                    "is_verified": user.is_verified,
                    "location": user.location,
                    "specialization": user.specialization,
                    "photo": photo_url,  # Return the URL instead of the file field
                    "permissions": permissions,
                    "groups": groups
                }
            }, status=status.HTTP_200_OK)
        return Response({'status_code': 400, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=VerifyEmailSerializer,
        responses={
            200: 'Email verified successfully',
            400: 'User not found, already verified, or invalid code'
        }
    )
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'status_code': 200, 'data': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        return Response({'status_code': 400, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        responses={
            200: 'Password reset email sent',
            404: 'Email does not exist',
            400: 'Invalid data provided'
        }
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if not user:
                return Response({'status_code': 404, 'error': 'Email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            code = CodeGenerator.generate_code()
            user.reset_password_code = code
            user.save()
            EmailService.send_reset_password_email(email, code)
            return Response({'status_code': 200, 'data': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        return Response({'status_code': 400, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Set a new password for the user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="User's email"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="New password"),
                'code': openapi.Schema(type=openapi.TYPE_STRING, description="Reset code sent to the user's email")
            },
            required=['email', 'password', 'code']
        ),
        responses={
            200: openapi.Response(description="Password updated successfully."),
            404: openapi.Response(description="User does not exist."),
            400: openapi.Response(description="Invalid code.")
        }
    )
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('password')
        code = request.data.get('code')

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'status_code': 404, 'error': 'Email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if user.reset_password_code != code:
            return Response({'status_code': 400, 'error': 'Invalid code.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.reset_password_code = None  # Remove the code after password change
        user.save()
        return Response({'status_code': 200, 'data': 'Password updated successfully.'}, status=status.HTTP_200_OK)

class SendVerificationEmailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Send a verification email to the user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="User's email")
            },
            required=['email']
        ),
        responses={
            200: openapi.Response(description="Verification email sent successfully."),
            404: openapi.Response(description="User does not exist."),
            400: openapi.Response(description="User is already verified.")
        }
    )
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            if user.is_verified:
                return Response({'status_code': 400, 'error': 'User is already verified.'}, status=status.HTTP_400_BAD_REQUEST)
            code = CodeGenerator.generate_code()
            user.activation_code = code
            user.save()
            EmailService.send_verification_email(email, code)
            return Response({'status_code': 200, 'data': 'Verification email sent.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'status_code': 404, 'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class SendResetPasswordEmailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Send a password reset email to the user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="User's email")
            },
            required=['email']
        ),
        responses={
            200: openapi.Response(description="Password reset email sent successfully."),
            404: openapi.Response(description="User does not exist.")
        }
    )
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            code = CodeGenerator.generate_code()
            user.reset_password_code = code
            user.save()
            EmailService.send_reset_password_email(email, code)
            return Response({'status_code': 200, 'data': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'status_code': 404, 'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class ResendResetCodeView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Resend the reset password code to the user's email.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="User's email")
            },
            required=['email']
        ),
        responses={
            200: openapi.Response(description="Reset code resent successfully."),
            404: openapi.Response(description="User does not exist."),
        }
    )
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'status_code': 404, 'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        code = CodeGenerator.generate_code()
        user.reset_password_code = code
        user.save()
        EmailService.send_reset_password_email(email, code)
        return Response({'status_code': 200, 'data': 'Reset code resent successfully.'}, status=status.HTTP_200_OK)

class ConfirmResetCodeView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Confirm if the provided reset code is correct.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="User's email"),
                'code': openapi.Schema(type=openapi.TYPE_STRING, description="Reset code sent to the user's email")
            },
            required=['email', 'code']
        ),
        responses={
            200: openapi.Response(description="Reset code is correct."),
            400: openapi.Response(description="Invalid reset code."),
            404: openapi.Response(description="User does not exist."),
        }
    )
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'status_code': 404, 'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if user.reset_password_code != code:
            return Response({'status_code': 400, 'error': 'Invalid reset code.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status_code': 200, 'data': 'Reset code is correct.'}, status=status.HTTP_200_OK)

class AccountViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(User)

    def get_queryset(self):
        # Optionally filter based on user type or other criteria
        return super().get_queryset()

    def perform_create(self, serializer):
        # Additional logic during creation if needed
        serializer.save()

    def perform_update(self, serializer):
        # Additional logic during update if needed
        serializer.save()

    def perform_destroy(self, instance):
        # Additional logic during deletion if needed
        instance.delete()

    # action to retrieve user profile
    @action(detail=False, methods=['get'], url_path='my_account')
    def my_account(self, request):
        user = self.request.user
        serializer = UserProfileSerializer(user)
        return Response({'status_code': 200, 'data': serializer.data}, status=status.HTTP_200_OK)


class ClientListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    
    def get_queryset(self):
        return User.objects.filter(type='client')
    
    def filter_queryset(self, queryset):
        search_query = self.request.query_params.get('search', None)
        if search_query:
            search_fields = get_model_search_fields(User)
            q_objects = Q()
            for field in search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(q_objects)
        return queryset

    @swagger_auto_schema(
        operation_description="Retrieve a list of all clients",
        responses={
            200: openapi.Response(
                description="A list of clients",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'next': openapi.Schema(type=openapi.TYPE_STRING, description="URL for the next page of results"),
                        'previous': openapi.Schema(type=openapi.TYPE_STRING, description="URL for the previous page of results"),
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Client ID"),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING, description="Client name"),
                                    'email': openapi.Schema(type=openapi.TYPE_STRING, description="Client email"),
                                    'type': openapi.Schema(type=openapi.TYPE_STRING, description="User type"),
                                }
                            )
                        )
                    }
                )
            )
        }
    )
    def get(self, request):
        clients = User.objects.filter(type='client')
        # Manually instantiate and use pagination
        paginator = self.pagination_class()
        paginated_clients = paginator.paginate_queryset(clients, request, view=self)
        serializer = UserSerializer(paginated_clients, many=True)
        
        return paginator.get_paginated_response(serializer.data)


class TechnicianListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    
    def get_queryset(self):
        return User.objects.filter(type='technician')
    
    def filter_queryset(self, queryset):
        search_query = self.request.query_params.get('search', None)
        if search_query:
            search_fields = get_model_search_fields(User)
            q_objects = Q()
            for field in search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(q_objects)
        return queryset

    @swagger_auto_schema(
        operation_description="Retrieve a list of all technicians",
        responses={
            200: openapi.Response(
                description="A list of technicians",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status_code': openapi.Schema(type=openapi.TYPE_INTEGER, description="Status code of the response"),
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Technician ID"),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING, description="Technician name"),
                                    'email': openapi.Schema(type=openapi.TYPE_STRING, description="Technician email"),
                                    'type': openapi.Schema(type=openapi.TYPE_STRING, description="User type"),
                                }
                            )
                        )
                    }
                )
            )
        }
    )
    def get(self, request):
        technicians = User.objects.filter(type='technician')
        # Manually instantiate and use pagination
        paginator = self.pagination_class()
        paginated_technicians = paginator.paginate_queryset(technicians, request, view=self)
        serializer = UserSerializer(paginated_technicians, many=True)

        return paginator.get_paginated_response(serializer.data)

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    # pagination class
    pagination_class = Pagination

    @action(detail=True, methods=['get'], url_path='profile')
    def get_profile_by_id(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

