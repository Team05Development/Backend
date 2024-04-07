from datetime import datetime

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


from .models_application import Application
from .models_event import Event
from .models_auxiliary import ApplicationStatus
from .serializers_application import ApplicationSerializer, ApplicationResponseSerializer
from .serializers_event import EventResponseSerializer
from . import constants as const


User = get_user_model()

class ApplicationCreateView(CreateAPIView):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.current_user.id
        return super().create(request, *args, **kwargs)
    
class ApplicationAPIview(APIView):
    """
    Add or remove application to event.
    """
    # permission_classes = (IsAuthenticated, )
    
    def post(self, request, pk):
        self.check_permissions(request)
        user = request.user
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                {'детали': 'Событие не существует.'},
                status=status.HTTP_400_BAD_REQUEST)
        if Application.objects.filter(user=user, event=event).exists():
            return Response(
                {'детали': 'Заявка уже подана'},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            default_status, created = ApplicationStatus.objects.get_or_create(
                slug=const.DEFAULT_APPLICATION_STATUS_SLUG,
                name=const.DEFAULT_APPLICATION_STATUS_NAME)
            application = Application.objects.create(
                user=user,
                event=event,
                status=default_status)

        serializer = ApplicationResponseSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        self.check_permissions(request)
        user = request.user
        event = get_object_or_404(Event, pk=pk)
        try:
            Application.objects.get(user=user, event=event).delete()
        except Application.DoesNotExist:
            return Response(
                {'детали': 'Заявки нет'},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
