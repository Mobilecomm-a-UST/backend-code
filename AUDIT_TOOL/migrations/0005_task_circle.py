# Generated by Django 4.1.3 on 2025-01-23 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AUDIT_TOOL', '0004_task_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='circle',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
