# Generated by Django 4.1.3 on 2024-05-27 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_skills', '0009_alter_employeeskilltable_circle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeskilltable',
            name='uploaded_by',
            field=models.CharField(default='-', max_length=500),
        ),
    ]
