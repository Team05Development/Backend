from rest_framework import serializers

from .models_auxiliary import Direction, Format

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ('id', 'name', 'color', 'slug',)


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ('id', 'name', 'color', 'slug',)


class EventStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ('id', 'name', 'color', 'slug',)


class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ('id', 'name', 'color', 'slug',)