# Generated by Django 3.2.4 on 2022-01-31 02:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgebase', '0018_alter_kbviews_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kbviews',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 31, 2, 53, 48, 529402, tzinfo=utc)),
        ),
    ]
