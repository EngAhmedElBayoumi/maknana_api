from django.core.management.base import BaseCommand
from machine_and_factory.models import market_category
from django.core.files import File
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Seed market categories with sample data'

    def handle(self, *args, **kwargs):
        categories_data = [
            {
                'name': 'Industrial Mixers',
                'description': 'High-quality industrial mixing equipment',
                'image': 'category1.jpg'
            },
            {
                'name': 'Packaging Machines',
                'description': 'Automated packaging solutions',
                'image': 'category2.jpg'
            },
            {
                'name': 'CNC Machines',
                'description': 'Precision CNC machinery',
                'image': 'category3.jpg'
            },
            {
                'name': 'Assembly Lines',
                'description': 'Complete assembly line solutions',
                'image': 'category4.jpg'
            },
            {
                'name': 'Welding Equipment',
                'description': 'Professional welding machinery',
                'image': 'category5.jpg'
            }
        ]

        static_image_path = os.path.join(settings.BASE_DIR, 'static', 'categories')

        for category_data in categories_data:
            category = market_category(
                name=category_data['name'],
                description=category_data['description']
            )
            
            image_path = os.path.join(static_image_path, category_data['image'])
            if os.path.exists(image_path):
                with open(image_path, 'rb') as img_file:
                    category.image.save(
                        category_data['image'],
                        File(img_file),
                        save=False
                    )
            
            category.save()

        self.stdout.write(self.style.SUCCESS('Successfully created market categories'))