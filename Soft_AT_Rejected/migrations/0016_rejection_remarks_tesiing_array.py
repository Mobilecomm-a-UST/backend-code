# Generated by Django 4.1.3 on 2024-02-20 12:37

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Soft_AT_Rejected', '0015_alter_rejection_remarks_rejection_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='rejection_remarks',
            name='Tesiing_Array',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), default=list, size=None),
        ),
    ]
