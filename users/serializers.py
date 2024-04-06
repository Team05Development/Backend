from rest_framework import serializers
from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = (
            'id', 'email', 'first_name', 'last_name',
            'phone_number', 'job', 'job_title',
            'experience', 'direction', 'image')