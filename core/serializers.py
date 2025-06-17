from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser as User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'first_phone', 'second_phone', 'type', 'is_verified', 'location', 'specialization', 'photo']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'first_phone', 'second_phone', 'type', 'location', 'specialization', 'photo', 'is_verified']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'first_phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            first_phone=validated_data['first_phone'],
            password=validated_data['password'],
            type='client'
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')
        if not user.is_verified:
            raise serializers.ValidationError('User account is not verified')
        return user

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    
    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if not user:
            raise serializers.ValidationError('User not found')
        if user.is_verified:
            raise serializers.ValidationError('User already verified')
        if user.activation_code != data['code']:
            raise serializers.ValidationError('Invalid code')
        user.is_verified = True
        user.activation_code = None
        user.save()
        return user

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)


