# Generated by Django 3.2.4 on 2021-08-19 11:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serverinfo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualserver',
            name='service_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, related_name='service_type_vm', to='serverinfo.servicetype'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='physicalserver',
            name='service_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='service_type_physical', to='serverinfo.servicetype'),
        ),
        migrations.AlterField(
            model_name='physicalserver',
            name='warranty_expiry_date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 8, 18, 17, 31, 42, 876822), null=True, verbose_name='Warranty Expiry Date'),
        ),
    ]
