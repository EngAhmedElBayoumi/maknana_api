import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from machine_and_factory.models import factory, machine
from django.utils.timezone import now
from pathlib import Path

class Command(BaseCommand):
    help = "Seed the database with sample data for factories and machines"

    def handle(self, *args, **kwargs):
        # Get the user model
        User = get_user_model()

        # Create a sample user if not exists
        user, created = User.objects.get_or_create(
            email="testuser@example.com",
            defaults={"email": "testuser@example.com", "password": "password123"}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created user: {user.email}"))
        else:
            self.stdout.write(self.style.WARNING(f"User already exists: {user.email}"))

        # Clear existing data
        factory.objects.all().delete()
        machine.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Cleared existing factory and machine data"))

        # Create factories
        factory_names = ["Factory A", "Factory B", "Factory C", "Factory D", "Factory E"]
        locations = ["Cairo", "Alexandria", "Giza", "Aswan", "Luxor"]
        factories = []

        for i in range(5):
            new_factory = factory.objects.create(
                name=factory_names[i],
                location=locations[i],
                user=user,
                phone=f"0123456789{i}",
                responsible_user=f"Responsible User {i + 1}",
            )
            factories.append(new_factory)
            self.stdout.write(self.style.SUCCESS(f"Created factory: {new_factory.name}"))

        # Path to static images
        static_images_path = Path("static/machine_images")
        images = list(static_images_path.glob("*.jpg"))  # Assuming images are in .jpg format

        # Create machines
        statuses = ["good", "bad"]
        warranty_statuses = ["warranty", "not warranty"]

        for i in range(20):  # Create 20 machines
            machine_obj = machine.objects.create(
                name=f"Machine {i + 1}",
                factory=random.choice(factories),
                status=random.choice(statuses),
                warranty_status=random.choice(warranty_statuses),
                last_maintenance=now().date(),
                image=random.choice(images).name if images else None,
                catalog=None,  # No catalog for now
            )
            self.stdout.write(self.style.SUCCESS(f"Created machine: {machine_obj.name}"))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))