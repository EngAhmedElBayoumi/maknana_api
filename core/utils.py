from django.db.models import CharField, TextField, DateField, DateTimeField, EmailField

def get_model_search_fields(model):
    """
    Utility function to get all searchable fields from a model.
    Returns a list of field names that are character-based and can be used with icontains.
    """
    search_fields = []
    for field in model._meta.get_fields():
        if isinstance(field, (CharField, TextField, EmailField)) and not field.primary_key:
            search_fields.append(field.name)
    return search_fields



from django.core.mail import send_mail
from django.conf import settings
import random

class EmailService:
    @staticmethod
    def send_verification_email(email, code):
        subject = 'Verify Your Account'
        message = f'Your verification code is: {code}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

    @staticmethod
    def send_reset_password_email(email, code):
        subject = 'Reset Your Password'
        message = f'Your password reset code is: {code}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

class CodeGenerator:
    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))