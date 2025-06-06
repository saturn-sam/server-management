# Generated by Django 3.2.4 on 2022-12-07 06:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('serverinfo', '0061_auto_20221123_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='LicenseInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_name', models.CharField(max_length=250, verbose_name='License Name')),
                ('license_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='License Number')),
                ('license_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='License Type')),
                ('effective_quantity', models.IntegerField(blank=True, null=True, verbose_name='Effective Quantity')),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('delete_status', models.BooleanField(default=False)),
                ('deleted_date', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(null='True', on_delete=django.db.models.deletion.SET_NULL, related_name='licenseinfo_createdby', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null='True', on_delete=django.db.models.deletion.SET_NULL, related_name='licenseinfo_deleted', to=settings.AUTH_USER_MODEL)),
                ('service_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='licenseinfo_servicegroup', to='serverinfo.servicegroup')),
                ('service_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='licenseinfo_runningservice', to='serverinfo.runningservices')),
                ('update_by', models.ForeignKey(null='True', on_delete=django.db.models.deletion.SET_NULL, related_name='licenseinfo_updatedby', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
