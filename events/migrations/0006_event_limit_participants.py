# Generated by Django 3.2.16 on 2024-04-09 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_rename_time_program_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='limit_participants',
            field=models.BooleanField(default=False),
        ),
    ]