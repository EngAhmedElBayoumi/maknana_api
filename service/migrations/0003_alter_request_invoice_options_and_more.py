# Generated by Django 5.1.6 on 2025-07-19 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_alter_request_invoice_invoice_alter_service_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='request_invoice',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='request_report',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='servicerequest',
            options={'ordering': ['-id']},
        ),
    ]
