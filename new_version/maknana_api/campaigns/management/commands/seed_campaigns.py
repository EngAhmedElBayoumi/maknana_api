from django.core.management.base import BaseCommand
from campaigns.models import Campaign
from machine_and_factory.models import machine, factory, market_product
from service.models import service
from django.utils import timezone
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with Campaign data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting campaign seeder...'))

        machines = list(machine.objects.all())
        factories = list(factory.objects.all())
        markets = list(market_product.objects.all())
        services = list(service.objects.all())

        for _ in range(10):  # You can increase or reduce the number
            Campaign.objects.create(
                name=fake.company(),
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=random.randint(1, 30)),
                status=random.choice(['active', 'inactive', 'completed']),
                target_audience=fake.paragraph(nb_sentences=2),
                description=fake.text(),
                on_click=random.choice([
                    'market_page', 'service_page', 'factory_page',
                    'machine_page', 'other_page', 'external_link'
                ]),
                external_link=fake.url() if random.choice([True, False]) else None,
                machine=random.choice(machines) if machines and random.choice([True, False]) else None,
                factory=random.choice(factories) if factories and random.choice([True, False]) else None,
                service=random.choice(services) if services and random.choice([True, False]) else None,
                market=random.choice(markets) if markets and random.choice([True, False]) else None,
                other=fake.domain_name() if random.choice([True, False]) else None,
            )

        self.stdout.write(self.style.SUCCESS('Campaigns seeded successfully!'))
