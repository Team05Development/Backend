from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from . import constants as const
from .models_auxiliary import Direction, Format, EventStatus


User = get_user_model()


class Event(models.Model):
    admin = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='admin_events',
        blank=True, null=True)
    title = models.CharField(
        max_length=256,
        verbose_name='title of event',
        blank=False, null=False)
    limit = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(const.MAX_EVENT_LIMIT)],
        blank=False, null=False,)
    date = models.DateTimeField()
    address = models.CharField(
        max_length=const.MAX_ADDRESS_LIMIT,
        verbose_name='adress title of event',
        blank=False, null=False)
    direction = models.ManyToManyField(
        Direction, related_name='events', blank=True,
        verbose_name='directions')
    description = models.TextField(
        blank=False, null=False,
        verbose_name='description of event')
    format = models.ForeignKey(
        Format, on_delete=models.CASCADE,
        related_name='events',
        blank=False, null=False)
    status = models.ForeignKey(
        EventStatus, on_delete=models.CASCADE,
        related_name='events',
        blank=False, null=False)
    host = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='host_events',
        blank=True, null=True)
    image = models.ImageField(
        upload_to='users/images/',
        blank=True,
        null=True)
    presentation = models.CharField(
        max_length=const.MAX_LINK_LIMIT,
        verbose_name='event presentation',
        blank=True, null=True)
    recording = models.CharField(
        max_length=const.MAX_LINK_LIMIT,
        verbose_name='event recording',
        blank=True, null=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'event'
        verbose_name_plural = 'events'

    def __str__(self):
        return self.title
    

class Program(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='programs',
        blank=False, null=False)
    section = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(const.MAX_SECTION_LIMIT)],
        blank=False, null=False,)
    time = models.DateTimeField()
    description = models.TextField(
        blank=False, null=False,
        verbose_name='description of event section')
    speaker = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='programs',
        blank=True, null=True)


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        related_name="favorites",
        on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event,
        related_name="favorites",
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'favorites'
        verbose_name_plural = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'event'],
                name="unique_events")
        ]
        ordering = ["-event"]

    def __str__(self):
        f"{self.user} favorites {self.event}"