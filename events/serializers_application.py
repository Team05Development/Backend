from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers

from events.serializers_auxiliary import ApplicationStatusSerializer

from .models_auxiliary import ApplicationStatus
from .models_application import Application
from .models_event import Event

User = get_user_model()


class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email')
    event = serializers.CharField(source='event.title')
    status = serializers.CharField(source='status.name')

    class Meta:
        model = Application
        fields = ('id', 'user', 'event', 'status', 'created_at')