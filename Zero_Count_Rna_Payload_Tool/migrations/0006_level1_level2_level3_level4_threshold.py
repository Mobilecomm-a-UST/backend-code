# Generated by Django 4.1.3 on 2025-01-28 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Zero_Count_Rna_Payload_Tool', '0005_alter_ticket_counter_table_data_rca_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='level1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('circle', models.CharField(max_length=250)),
                ('person_name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='level2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('circle', models.CharField(max_length=250)),
                ('person_name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='level3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('circle', models.CharField(max_length=250)),
                ('person_name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='level4',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('circle', models.CharField(max_length=250)),
                ('person_name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Threshold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(choices=[('P0', 'P0'), ('P1', 'P1'), ('P2', 'P2'), ('P3', 'P3')], max_length=2, unique=True)),
                ('threshold_aging_level_1', models.IntegerField()),
                ('threshold_aging_level_2', models.IntegerField()),
                ('threshold_aging_level_3', models.IntegerField()),
                ('threshold_aging_level_4', models.IntegerField()),
            ],
        ),
    ]
