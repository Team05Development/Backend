from rest_framework import serializers
from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model
from events.serializers_auxiliary import DirectionSerializer

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    direction = DirectionSerializer(many=True)
    image = serializers.SerializerMethodField()
    experience = serializers.CharField(source='get_experience_display')

    class Meta(UserSerializer.Meta):
        fields = (
            'id', 'email', 'first_name', 'last_name', 'middle_name',
            'phone_number', 'telegram', 'job', 'job_title',
            'experience', 'direction', 'image')

    def get_image(self, obj):
        if not obj.image:
            return None
        else:
            return obj.image.url
