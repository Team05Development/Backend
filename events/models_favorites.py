from django.db import models
from django.contrib.auth import get_user_model

from .models_event import Event

User = get_user_model()


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
