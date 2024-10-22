# Generated by Django 5.1.2 on 2024-10-21 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='one_time_payment',
            new_name='is_mail_verified',
        ),
        migrations.AddField(
            model_name='customuser',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='verification_attempts',
            field=models.PositiveIntegerField(default=3),
        ),
        migrations.AddField(
            model_name='customuser',
            name='verification_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
