from rest_framework import serializers

from .models import UserFollowing


class IsAppliedSerializerMixin(serializers.Serializer):
    is_applied = serializers.SerializerMethodField()

    class Meta:
        fields = ('is_applied', )

    def get_is_applied(self, obj):
        current_user = self.context.get('request').user
        is_subscribed = (
            UserFollowing.objects.
            filter(user=current_user.id, following_user=obj.id).exists())
        return is_subscribed