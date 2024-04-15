from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F, Count, Q, Case, When, BooleanField
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from .models_auxiliary import (
    Direction, Format,
    EventStatus, ApplicationStatus, )
from .pagination import CustomPageNumberPagination


from .serializers_auxiliary import (
    DirectionSerializer,
    FormatSerializer,
    EventStatusSerializer,
    ApplicationStatusSerializer,
)

@extend_schema(tags=["Directions"],)               
@extend_schema_view(
    get=extend_schema(summary="List of directions"),
    )
class ListDirectionAPIView(ListAPIView):
    serializer_class = DirectionSerializer
    queryset = Direction.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)


@extend_schema(tags=["Directions"],)               
@extend_schema_view(
    get=extend_schema(summary="One direction"),
    )
class RetrieveDirectionAPIView(RetrieveAPIView):
    serializer_class = DirectionSerializer
    queryset = Direction.objects.all()
    permission_classes = (AllowAny,)


@extend_schema(tags=["Event formats"],)               
@extend_schema_view(
    get=extend_schema(summary="List of event formats"),
    )
class ListFormatAPIView(ListAPIView):
    serializer_class = FormatSerializer
    queryset = Format.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)

@extend_schema(tags=["Event formats"],)               
@extend_schema_view(
    get=extend_schema(summary="One event format"),
    )
class RetrieveFormatAPIView(RetrieveAPIView):
    serializer_class = FormatSerializer
    queryset = Format.objects.all()
    permission_classes = (AllowAny,)

@extend_schema(tags=["Event statuses"],)
@extend_schema_view(
    get=extend_schema(summary="List of event statuses"),
    )
class ListEventStatusAPIView(ListAPIView):
    serializer_class = EventStatusSerializer
    queryset = EventStatus.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)

@extend_schema(tags=["Event statuses"],)
@extend_schema_view(
    get=extend_schema(summary="One event statuse"),
    )
class RetrieveEventStatusAPIView(RetrieveAPIView):
    serializer_class = EventStatusSerializer
    queryset = EventStatus.objects.all()
    permission_classes = (AllowAny,)


@extend_schema(tags=["Application statuses"],)
@extend_schema_view(
    get=extend_schema(summary="List of applications statuses"),
    )
class ListApplicationStatusAPIView(ListAPIView):
    serializer_class = ApplicationStatusSerializer
    queryset = ApplicationStatus.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)


@extend_schema(tags=["Application statuses"],)
@extend_schema_view(
    get=extend_schema(summary="One application status"),
    )
class RetrieveApplicationStatusAPIView(RetrieveAPIView):
    serializer_class = ApplicationStatusSerializer
    queryset = ApplicationStatus.objects.all()
    permission_classes = (AllowAny,)