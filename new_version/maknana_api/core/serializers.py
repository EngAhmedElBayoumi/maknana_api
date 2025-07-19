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


class CustomerWithFactoriesSerializer(serializers.Serializer):
    from machine_and_factory.serializers import Factory2Serializer
    
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    first_phone = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True, required=True)
    second_phone = serializers.CharField(max_length=15, required=False, allow_blank=True, allow_null=True)
    location = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    factories = serializers.ListField(child=Factory2Serializer(exclude_user=True), required=True, allow_empty=False)

    def create(self, validated_data):
        from django.db import transaction
        from machine_and_factory.models import factory, machine
        factories_data = validated_data.pop('factories')
        with transaction.atomic():
            user = User.objects.create_user(
                email=validated_data['email'],
                name=validated_data['name'],
                first_phone=validated_data['first_phone'],
                password=validated_data['password'],
                second_phone=validated_data.get('second_phone'),
                location=validated_data.get('location'),
                type='client'
            )
            for factory_data in factories_data:
                machines_data = factory_data.pop('machines', [])
                print("factory_data:", factory_data)
                print("machines_data:", machines_data)
                factory_instance = factory.objects.create(user=user, **factory_data)
                for machine_data in machines_data:
                    machine.objects.create(factory=factory_instance, **machine_data)
        return user

    def to_representation(self, instance):
        return UserSerializer(instance).data