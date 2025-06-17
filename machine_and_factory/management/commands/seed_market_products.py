from django.core.management.base import BaseCommand
from machine_and_factory.models import market_product, market_category
from django.core.files import File
import random
import os
from django.conf import settings
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seed market products with sample data'

    def handle(self, *args, **kwargs):
        categories = list(market_category.objects.all())
        if not categories:
            self.stdout.write(self.style.ERROR('Please run seed_market_categories first'))
            return

        product_names = [
            "Industrial Mixer", "Conveyor Belt", "Packaging Machine", "CNC Machine",
            "Welding Robot", "Assembly Line", "3D Printer", "Laser Cutter",
            "Injection Molder", "Heat Press", "Drilling Machine", "Grinding Machine"
        ]

        static_image_path = os.path.join(settings.BASE_DIR, 'static', 'products')
        sample_images = [f'{i}.png' for i in range(1, 5)]  # product1.jpg to product5.jpg

        for i in range(50):
            name = f"{random.choice(product_names)} {i+1}"
            product_type = random.choice(['new', 'used'])
            price = Decimal(random.uniform(1000, 50000)).quantize(Decimal('0.01'))
            category = random.choice(categories)
            
            product = market_product(
                name=name,
                description=f"Professional {product_type} {name.lower()} for industrial use. "
                           f"High-quality manufacturing equipment from trusted brands.",
                price=price,
                category=category,
                type=product_type
            )

            image_name = random.choice(sample_images)
            image_path = os.path.join(static_image_path, image_name)
            if os.path.exists(image_path):
                with open(image_path, 'rb') as img_file:
                    product.image.save(
                        f"{name.lower().replace(' ', '_')}.jpg",
                        File(img_file),
                        save=False
                    )

            product.save()

        self.stdout.write(self.style.SUCCESS('Successfully created 50 market products'))