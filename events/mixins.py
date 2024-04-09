from rest_framework import serializers

from .models_application import Application
from .models_favorites import Favorites


class ApplicationSerializerMixin(serializers.Serializer):
    is_applied = serializers.SerializerMethodField()
    total_applications = serializers.SerializerMethodField()
    application_status = serializers.SerializerMethodField()

    class Meta:
        fields = ('is_applied', 'total_applications', 'application_status')

    def get_is_applied(self, obj):
        current_user = self.context.get('request').user
        is_applied = (
            Application.objects.
            filter(user=current_user.id, event=obj).exists())
        return is_applied
    
    def get_total_applications(self, obj):
        total_applications = (
            Application.objects.
            filter(event=obj).count())
        return total_applications
    
    def get_application_status(self, obj):
        current_user = self.context.get('request').user
        application = Application.objects.filter(user=current_user.id, event=obj).first()
        return application.status.name if application else None
    

class FavoritesSerializerMixin(serializers.Serializer):
    is_favorited = serializers.SerializerMethodField()
    total_favorites = serializers.SerializerMethodField()
    
    class Meta:
        fields = ('is_favorited', 'total_favorites', )

    def get_is_favorited(self, obj):
        current_user = self.context.get('request').user
        is_favorited = (
            Favorites.objects.
            filter(user=current_user.id, event=obj).exists())
        return is_favorited
    
    def get_total_favorites(self, obj):
        total_favorites = (
            Favorites.objects.
            filter(event=obj).count())
        return total_favorites
    
    

        # queryset = Event.objects.all().prefetch_related('programs').annotate(
        #     total_favorites=Count(
        #         "favorites",
        #         filter=Q(favorites__user_id=user_id)
        #     ),
        #     is_favorited=Case(
        #         When(total_favorite__gte=1, then=True),
        #         default=False,
        #         output_field=BooleanField()
        #     )
        # )
        # queryset = queryset.annotate(
        #     total_applications=Count(
        #         "applications",
        #         filter=Q(applications__user_id=user_id)
        #     ),
        #     is_applied=Case(
        #         When(total_applications__gte=1, then=True),
        #         default=False,
        #         output_field=BooleanField()
        #     )
        # )
        # queryset = queryset.annotate(application_status=F('applications__status__name'))