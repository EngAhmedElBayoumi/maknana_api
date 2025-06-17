from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, name, first_phone, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, first_phone=first_phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, first_phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # type technician when creating a superuser
        extra_fields.setdefault('type', 'admin')
        # is verified is True by default for superuser
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, first_phone, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('technician', 'Technician'),
    )

    name = models.CharField(max_length=255)
    first_phone = models.CharField(max_length=15)
    second_phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    type = models.CharField(max_length=20, choices=USER_TYPES)
    is_verified = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6, blank=True, null=True)
    reset_password_code = models.CharField(max_length=6, blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'first_phone']

    def __str__(self):
        return self.email
