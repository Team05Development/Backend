# Generated by Django 3.2.16 on 2024-04-09 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_event_limit_participants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='limit_participants',
        ),
        migrations.AddField(
            model_name='event',
            name='unlimited',
            field=models.BooleanField(default=True),
        ),
    ]
