import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models_event import Event
from .models_auxiliary import Direction, Format, EventStatus
from users.serializers import CustomUserSerializer
from .serializers_auxiliary import (
    DirectionSerializer,
    FormatSerializer,
    EventStatusSerializer)
from . import constants as const

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class EventSerializer(serializers.ModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(
        required=True,
        many=False,
        queryset=User.objects.all(),
        read_only=False)
    direction = serializers.PrimaryKeyRelatedField(
        required=True,
        many=True,
        queryset=Direction.objects.all(),
        read_only=False)
    image = Base64ImageField()
    format = serializers.PrimaryKeyRelatedField(
        required=True,
        many=False,
        queryset=Format.objects.all(),
        read_only=False)
    status = serializers.PrimaryKeyRelatedField(
        required=True,
        many=False,
        queryset=EventStatus.objects.all(),
        read_only=False)
    host = serializers.PrimaryKeyRelatedField(
        required=True,
        many=False,
        queryset=User.objects.all(),
        read_only=False)

    class Meta:
        model = Event
        fields = (
            'admin', 'title', 'limit', 'date', 'address',
            'direction', 'description', 'format', 'status', 'host',
            'image', 'presentation', 'recording')

    def validate_direction(self, value):
        if len(value) == 0:
            raise serializers.ValidationError('Это поле обязательное')
        if len(value) != len(set([direction.id for direction in value])):
            raise serializers.ValidationError('Направления должны быть уникальными')
        return value

    def create(self, validated_data):
        directions = validated_data.pop('direction')
        event = Event.objects.create(**validated_data)
        event.direction.set(directions)
        event.is_favorited = False
        event.is_applied = False
        return event

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.limit = validated_data.get('text', instance.limit)
        instance.date = validated_data.get('date', instance.date)
        instance.address = validated_data.get('address', instance.address)
        instance.format = validated_data.get('format', instance.format)
        instance.status = validated_data.get('status', instance.status)
        instance.image = validated_data.get('image', instance.image)
        instance.presentation = validated_data.get('presentation', instance.presentation)
        instance.recording = validated_data.get('recording', instance.recording)
        
        if 'direction' in validated_data:
            directions = validated_data.pop('direction')
            instance.direction.clear()
            instance.direction.set(directions)

        instance.save()
        return instance

    def to_representation(self, instance):
        return (EventResponseSerializer(context=self.context).
                to_representation(instance))


class EventResponseSerializer(serializers.ModelSerializer):
    admin = CustomUserSerializer()
    direction = DirectionSerializer(many=True)
    format = FormatSerializer()
    status = EventStatusSerializer()
    host = CustomUserSerializer()
    image = serializers.CharField(source='image.url')
    is_favorited = serializers.BooleanField(read_only=True)
    is_applied = serializers.BooleanField(read_only=True)

    class Meta:
        model = Event
        fields = (
            'id', 'admin', 'title', 'limit', 'date', 'address',
            'direction', 'description', 'format', 'status', 'host',
            'image', 'presentation', 'recording',
            'is_favorited', 'is_applied')       