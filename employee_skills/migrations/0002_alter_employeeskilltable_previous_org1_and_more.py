# Generated by Django 4.1.3 on 2024-05-02 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_skills', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeskilltable',
            name='previous_org1',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='previous_org2',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='previous_org3',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
