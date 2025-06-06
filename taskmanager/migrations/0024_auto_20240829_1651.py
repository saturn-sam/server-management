# Generated by Django 3.2.4 on 2024-08-29 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taskmanager', '0023_alter_taskmanager_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmanager',
            name='task_steps_commentary',
            field=models.ManyToManyField(blank=True, related_name='tmcommentary', to='taskmanager.TaskStepComentary'),
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasktype_created_by_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='taskmanager',
            name='task_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tm_task_type', to='taskmanager.tasktype'),
        ),
    ]
