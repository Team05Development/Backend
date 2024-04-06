# Generated by Django 3.2.16 on 2024-04-06 17:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='application status')),
                ('slug', models.SlugField(max_length=128, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'application status',
                'verbose_name_plural': 'application statuses',
            },
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='direction')),
                ('slug', models.SlugField(max_length=128, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'direction',
                'verbose_name_plural': 'directions',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='title of event')),
                ('limit', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000)])),
                ('date', models.DateTimeField()),
                ('address', models.CharField(max_length=1024, verbose_name='title of event')),
                ('description', models.TextField(verbose_name='description of event')),
                ('image', models.ImageField(blank=True, null=True, upload_to='users/images/')),
                ('presentation', models.CharField(blank=True, max_length=1024, null=True, verbose_name='event presentation')),
                ('recording', models.CharField(blank=True, max_length=1024, null=True, verbose_name='event recirding')),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='EventStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='event status')),
                ('slug', models.SlugField(max_length=128, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'event status',
                'verbose_name_plural': 'event statuses',
            },
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'ordering': ['-event'],
            },
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='format')),
                ('slug', models.SlugField(max_length=128, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'format',
                'verbose_name_plural': 'formats',
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('time', models.DateTimeField()),
                ('description', models.TextField(verbose_name='description of event section')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programs', to='events.event')),
            ],
        ),
    ]
