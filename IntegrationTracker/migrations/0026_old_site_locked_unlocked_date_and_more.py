# Generated by Django 4.1.3 on 2025-02-05 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('IntegrationTracker', '0025_relocation_tracker_approval_given_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='old_site_locked_unlocked_date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_locked_by', models.CharField(blank=True, max_length=255, null=True)),
                ('approval_given_by', models.CharField(blank=True, max_length=255, null=True)),
                ('date_time', models.DateTimeField(default=None, null=True)),
                ('purpose', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Relocation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IntegrationTracker.relocation_tracker')),
            ],
        ),
        migrations.CreateModel(
            name='New_site_locked_unlocked_date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_locked_by', models.CharField(blank=True, max_length=255, null=True)),
                ('approval_given_by', models.CharField(blank=True, max_length=255, null=True)),
                ('date_time', models.DateTimeField(default=None, null=True)),
                ('purpose', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Relocation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IntegrationTracker.relocation_tracker')),
            ],
        ),
    ]
