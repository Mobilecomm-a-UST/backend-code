# Generated by Django 4.1.3 on 2025-02-03 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IntegrationTracker', '0015_relocation_tracker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relocation_tracker',
            name='integration_date',
            field=models.DateField(null=True),
        ),
    ]
