# Generated by Django 5.1.2 on 2024-10-22 00:01

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_timers', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timersession',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='timersession',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='timersession',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='timersession',
            name='timer_block',
        ),
        migrations.AddField(
            model_name='timerblock',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timerblock',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='timerblock',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='timerblock',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='timerblock',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='timerblock',
            name='is_started',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='timerblock',
            name='last_used',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timerblock',
            name='note_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timerblock',
            name='note_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='timerblock',
            name='number_of_continue',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timerblock',
            name='number_of_stop',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timerblock',
            name='percentage_of_completion',
            field=models.IntegerField(default=0, help_text='Percentage of completion'),
        ),
        migrations.AddField(
            model_name='timerblock',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timerblock',
            name='used_duration',
            field=models.IntegerField(default=0, help_text='Duration in minutes'),
        ),
        migrations.AddField(
            model_name='timersession',
            name='timer_blocks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timersession',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='timerblock',
            name='break_duration',
            field=models.IntegerField(default=0, help_text='Duration in minutes'),
        ),
        migrations.AlterField(
            model_name='timerblock',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='timerblock',
            name='work_duration',
            field=models.IntegerField(default=0, help_text='Duration in minutes'),
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='timerblock',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_timers.label'),
        ),
    ]
