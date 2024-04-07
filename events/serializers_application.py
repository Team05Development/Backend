from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers

from events.serializers_event import EventResponseSerializer
from events.serializers_auxiliary import ApplicationStatusSerializer

from .models_auxiliary import ApplicationStatus
from .models_application import Application
from .models_event import Event

User = get_user_model()

class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=User.objects.all()
    )
    event = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Event.objects.all()
    )
    status = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=ApplicationStatus.objects.all()
    )

    class Meta:
        model = Application
        fields = ('user', 'event', 'status')

    def to_representation(self, instance):
        return (ApplicationResponseSerializer(context=self.context).
                to_representation(instance))


class ApplicationResponseSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email')
    event = serializers.CharField(source='event.title')
    status = serializers.CharField(source='status.name')

    class Meta:
        model = Application
        fields = ('id', 'user', 'event', 'status', 'created_at')


