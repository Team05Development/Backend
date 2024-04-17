from drf_spectacular.utils import (
    extend_schema, extend_schema_view,
    OpenApiExample)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


from .models_application import Application
from .models_event import Event
from .models_auxiliary import ApplicationStatus
from .serializers_event import EventFullResponseSerializer
from . import constants as const


User = get_user_model()


@extend_schema(tags=["Application"],
               responses=EventFullResponseSerializer
               )
@extend_schema_view(
    post=extend_schema(
            summary="Send application for event",
            description="""When send with no payload assigns default status.
            If event unlimited=True then default status is 'approved'.
            If event unlimited=False then default status is 'sent'.""",
            examples=[
                OpenApiExample(
                    "Application example with explicit status",
                        description="""Payload example for creating
                        application with explicit status.""",
                        value={"status": 1},
                    status_codes=[str(status.HTTP_200_OK)],
                ),
            ],
        ),
    put=extend_schema(
        summary="Change status for send application",
        examples=[
            OpenApiExample(
                "Update application status example",
                description="Payload example for updating application status.",
                value={"status": 1},
                status_codes=[str(status.HTTP_200_OK)],
                ),
            ],

    ),
    delete=extend_schema(
            summary="Delete application for event",
        ),
)
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
            if event.unlimited is False:
                status_obj, created = ApplicationStatus.objects.get_or_create(
                    slug=const.DEFAULT_APPLICATION_STATUS_SLUG,
                    name=const.DEFAULT_APPLICATION_STATUS_NAME)
            else:
                status_obj, created = ApplicationStatus.objects.get_or_create(
                    slug=const.UNLIMITED_APPLICATION_STATUS_SLUG,
                    name=const.UNLIMITED_APPLICATION_STATUS_NAME)
        else:
            status_obj = get_object_or_404(ApplicationStatus, pk=status_id)
        Application.objects.create(user=user, event=event, status=status_obj)

        serializer = EventFullResponseSerializer(
            event, context={'request': request})
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
        application.status = status_obj
        application.save()
        serializer = EventFullResponseSerializer(
            event, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
