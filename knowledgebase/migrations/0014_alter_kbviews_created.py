# Generated by Django 3.2.4 on 2022-01-27 09:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgebase', '0013_auto_20210926_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kbviews',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 27, 9, 46, 49, 163841, tzinfo=utc)),
        ),
    ]
