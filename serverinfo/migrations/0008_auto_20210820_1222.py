# Generated by Django 3.2.4 on 2021-08-20 06:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverinfo', '0007_auto_20210820_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='physicalserver',
            name='delete_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='physicalserver',
            name='warranty_expiry_date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 8, 19, 12, 22, 57, 946870), null=True, verbose_name='Warranty Expiry Date'),
        ),
        migrations.AlterField(
            model_name='project',
            name='delete_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='runningservices',
            name='delete_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='delete_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='virtualserver',
            name='delete_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vmlocationtype',
            name='delete_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='zone',
            name='delete_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
