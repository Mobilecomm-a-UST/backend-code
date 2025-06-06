# Generated by Django 4.1.3 on 2023-10-07 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OEM', models.CharField(max_length=500)),
                ('Hardware_Type', models.CharField(max_length=500)),
                ('Equipment_description', models.CharField(max_length=500)),
                ('Supported_Cards', models.CharField(max_length=500)),
                ('Technology_Supported', models.CharField(max_length=500)),
                ('Techninal_Description', models.CharField(max_length=500)),
                ('Capacity', models.CharField(max_length=500)),
                ('MAX_POWER', models.CharField(max_length=500)),
                ('Remarks', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment_upload_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_status', models.CharField(blank=True, max_length=500, null=True)),
                ('Remark', models.TextField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
