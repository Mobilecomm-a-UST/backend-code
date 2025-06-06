# Generated by Django 4.1.3 on 2025-02-05 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IntegrationTracker', '0021_relocation_tracker_ix_unique_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='relocation_tracker',
            old_name='deviation',
            new_name='allocated_vs_deployed_tech_deviation',
        ),
        migrations.RemoveField(
            model_name='relocation_tracker',
            name='no_of_deviated_tech',
        ),
        migrations.AddField(
            model_name='relocation_tracker',
            name='old_vs_deployed_tech_deviation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
