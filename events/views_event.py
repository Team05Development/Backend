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
from django.db.models import OuterRef, Subquery

from .pagination import CustomPageNumberPagination
from .filters import EventFilter
from .permissions import ReadOnly

from . import constants as const
from .models_event import Event
from .models_favorites import Favorites
from .models_auxiliary import EventStatus
from .models_application import Application

from .serializers_event import (
    EventPostSerializer, EventFullResponseSerializer, EventShortResponseSerializer)
from .decorators import response_schema

User = get_user_model()

@response_schema(serializer=EventFullResponseSerializer)
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'option']
    # serializer_class = EventPostSerializer
    # permission_classes = (ReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_class = EventFilter
    search_fields = ('title', 'description') 
    ordering_fields = ('date', 'total_applications', )

    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         return (ReadOnly(),)
    #     if self.action == 'create':
    #         return (IsAuthenticated(),)
    #     if self.action in ['update', 'partial_update', 'destroy']:
    #         return (IsAuthorOrReadOnly(),)
    #     return (super().get_permissions())
     
    serializer_classes = {
        'list': EventShortResponseSerializer,
        'create': EventPostSerializer,
        'retrieve': EventFullResponseSerializer,
        'update': EventPostSerializer,
        'partial_update': EventPostSerializer,
    }
    default_serializer_class = EventShortResponseSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        user = self.request.user
        user_id = user.id if not user.is_anonymous else None
        queryset = Event.objects.all().prefetch_related('programs').annotate(
            total_favorites=Count(
                "favorites",
                filter=Q(favorites__user_id=user_id)
            ),
            is_favorited=Case(
                When(total_favorites__gte=1, then=True),
                default=False,
                output_field=BooleanField()
            )
        )
        queryset = queryset.annotate(
            total_applications=Count(
                "applications",
                filter=Q(applications__user_id=user_id)
            ),
            is_applied=Case(
                When(total_applications__gte=1, then=True),
                default=False,
                output_field=BooleanField()
            )
        )
        queryset = queryset.annotate(application_status=F('applications__status__name'))
        return queryset.order_by('date')
