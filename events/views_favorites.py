from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models_event import Event
from .models_favorites import Favorites
from .serializers_event import EventFullResponseSerializer
# from .permissions import ReadOnly, IsAuthorOrReadOnly, EventPermission

User = get_user_model()


@extend_schema(tags=["Favorites"],
               responses=EventFullResponseSerializer)
@extend_schema_view(
    post=extend_schema(
            summary="Add event to favorites",
        ),
    delete=extend_schema(
            summary="Delete event from favorites",
        ),
)
class FavoritesAPIView(APIView):
    """
    Add or remove event from favorites.
    """
    # permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        self.check_permissions(request)
        user = request.user
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                {'детали': 'События не существует.'},
                status=status.HTTP_400_BAD_REQUEST)
        if Favorites.objects.filter(user=user, event=event).exists():
            return Response(
                {'детали': 'Уже в избранном'},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            Favorites.objects.create(user=user, event=event)

        serializer = EventFullResponseSerializer(
            event, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        self.check_permissions(request)
        user = request.user
        event = get_object_or_404(Event, pk=pk)
        try:
            Favorites.objects.get(user=user, event=event).delete()
        except Favorites.DoesNotExist:
            return Response(
                {'детали': 'Событие не в избранном'},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
