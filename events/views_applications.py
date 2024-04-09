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
from .serializers_application import ApplicationSerializer
from . import constants as const


User = get_user_model()


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
        status_id = request.data.get("status")
        if status_id is None:
            if event.unlimited==False:
                status_obj, created = ApplicationStatus.objects.get_or_create(
                    slug=const.DEFAULT_APPLICATION_STATUS_SLUG,
                    name=const.DEFAULT_APPLICATION_STATUS_NAME)
            else:
                status_obj, created = ApplicationStatus.objects.get_or_create(
                    slug=const.UNLIMITED_APPLICATION_STATUS_SLUG,
                    name=const.UNLIMITED_APPLICATION_STATUS_NAME)
        else:
            status_obj = get_object_or_404(ApplicationStatus, pk=status_id)
        application = Application.objects.create(
            user=user,
            event=event,
            status=status_obj)

        serializer = ApplicationSerializer(application)
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
    
    def put(self, request, pk):
        self.check_permissions(request)
        user = request.user
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                {'детали': 'Событие не существует.'},
                status=status.HTTP_400_BAD_REQUEST)
        try:
            application = Application.objects.get(user=user, event=event)
        except Application.DoesNotExist:
            return Response(
                {'детали': 'Заявки не существует'},
                status=status.HTTP_400_BAD_REQUEST)
        status_id = request.data.get("status")
        if status_id is None:
            return Response(
                {'детали': 'Поле status обязательное.'},
                status=status.HTTP_400_BAD_REQUEST)
        try:
            status_obj = ApplicationStatus.objects.get(pk=status_id)
        except ApplicationStatus.DoesNotExist:
                return Response(
                    {'детали': 'Такого статуса не существует'},
                    status=status.HTTP_400_BAD_REQUEST)
        application.status=status_obj
        application.save()
        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)
