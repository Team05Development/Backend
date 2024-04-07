from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers

from events.serializers_event import EventResponseSerializer
from users.serializers import CustomUserSerializer

from .models_auxiliary import ApplicationStatus
from .models_application import Application
from .models_event import Event

User = get_user_model()


class ApplicationStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationStatus
        fields = ('name',)


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
    created_at = serializers.DateTimeField(required=False)

    class Meta:
        model = Application
        fields = ('user', 'event', 'status', 'created_at')

    def create(self, validated_data):
        application = Application.objects.create(**validated_data)
        created_at = datetime.now().isoformat()
        application.created_at = created_at
        return application

    def to_representation(self, instance):
        return (ApplicationResponseSerializer(context=self.context).
                to_representation(instance))


class ApplicationResponseSerializer(serializers.ModelSerializer):
    event = EventResponseSerializer()
    status = ApplicationStatusSerializer()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Application
        fields = ('id', 'event', 'status')
