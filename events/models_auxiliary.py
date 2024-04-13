from django.db import models
from . import constants as const


class Direction(models.Model):
    name = models.CharField(
        max_length=const.MAX_NAME_LIMIT,
        verbose_name='direction')
    slug = models.SlugField(
        unique=True,
        max_length=const.MAX_SLUG_LIMIT,
        verbose_name='slug'
    )
    color = models.CharField(
        max_length=const.MAX_LENGTH_COLOR,
        blank=True, null=True)

    class Meta:
        verbose_name = 'direction'
        verbose_name_plural = 'directions'

    def __str__(self):
        return self.name


class Format(models.Model):
    name = models.CharField(
        max_length=const.MAX_NAME_LIMIT,
        verbose_name='format')
    slug = models.SlugField(
        unique=True,
        max_length=const.MAX_SLUG_LIMIT,
        verbose_name='slug'
    )
    color = models.CharField(
        max_length=const.MAX_LENGTH_COLOR,
        blank=True, null=True)

    class Meta:
        verbose_name = 'format'
        verbose_name_plural = 'formats'

    def __str__(self):
        return self.name


class EventStatus(models.Model):
    name = models.CharField(
        max_length=const.MAX_NAME_LIMIT,
        verbose_name='event status')
    slug = models.SlugField(
        unique=True,
        max_length=const.MAX_SLUG_LIMIT,
        verbose_name='slug'
    )
    color = models.CharField(
        max_length=const.MAX_LENGTH_COLOR,
        blank=True, null=True)

    class Meta:
        verbose_name = 'event status'
        verbose_name_plural = 'event statuses'

    def __str__(self):
        return self.name


class ApplicationStatus(models.Model):
    name = models.CharField(
        max_length=const.MAX_NAME_LIMIT,
        verbose_name='application status')
    slug = models.SlugField(
        unique=True,
        max_length=const.MAX_SLUG_LIMIT,
        verbose_name='slug'
    )
    color = models.CharField(
        max_length=const.MAX_LENGTH_COLOR,
        blank=True, null=True)

    class Meta:
        verbose_name = 'application status'
        verbose_name_plural = 'application statuses'

    def __str__(self):
        return self.name
