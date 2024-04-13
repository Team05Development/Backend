from django.db import models
from django.contrib.auth import get_user_model

from .models_event import Event
from .models_auxiliary import ApplicationStatus

User = get_user_model()


class Application(models.Model):
    user = models.ForeignKey(
        User,
        related_name="applications",
        on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event,
        related_name="applications",
        on_delete=models.CASCADE)
    status = models.ForeignKey(
        ApplicationStatus,
        on_delete=models.CASCADE,
        related_name='applications',
        blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'event'],
                name="unique_applications")
        ]
        ordering = ["-event"]

    def __str__(self):
        return f"{self.user} applied to {self.event}"
