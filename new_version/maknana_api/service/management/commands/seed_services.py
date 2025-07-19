import random
from django.core.management.base import BaseCommand
from service.models import service
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Seed the database with 20 services'

    def handle(self, *args, **kwargs):
        images = [
            os.path.join('static', '1.png'),
            os.path.join('static', '2.png'),
            os.path.join('static', '3.jpg'),
            os.path.join('static', '4.png'),
            os.path.join('static', '5.png'),
        ]

        for i in range(1, 21):
            service.objects.create(
                name=f'Service {i}',
                name_ar=f'خدمة {i}',
                short_description=f'This is a short description for service {i}',
                short_description_ar=f'هذا وصف قصير للخدمة {i}',
                long_description=f'This is a long description for service {i}',
                long_description_ar=f'هذا وصف طويل للخدمة {i}',
                price=f'{random.randint(100, 1000)} USD',
                price_ar=f'{random.randint(100, 1000)} دولار',
                image=random.choice(images),
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded 20 services'))