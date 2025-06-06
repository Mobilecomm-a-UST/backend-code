# Generated by Django 4.1.3 on 2024-05-21 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_skills', '0008_employeeskilltable_delete_remark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeskilltable',
            name='circle',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='current_circle',
            field=models.CharField(default='-', max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='current_designation',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='current_role',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='deleted_by',
            field=models.CharField(default='-', max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='designation',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='domain',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='employee_name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='manager_emp_code',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='oem',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='previous_org1',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='previous_org2',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='previous_org3',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='project',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='project_name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='reporting_manager_name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='team_category',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='employeeskilltable',
            name='working_status',
            field=models.CharField(max_length=500),
        ),
    ]
