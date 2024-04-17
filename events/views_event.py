from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework import viewsets
from rest_framework import filters
from rest_framework import status
# from rest_framework.permissions import IsAuthenticated, AllowAny

from django.db.models import F, Count, Q, Case, When, BooleanField
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from .pagination import CustomPageNumberPagination
from .filters import EventFilter
# from .permissions import ReadOnly

from .models_event import Event
from .serializers_event import (
    EventPostSerializer,
    EventFullResponseSerializer,
    EventShortResponseSerializer)

User = get_user_model()


@extend_schema(tags=["Events"])
@extend_schema_view(
    list=extend_schema(
            summary="Show list of events with short description",
        ),
    create=extend_schema(
        summary="Create new event",
        responses={
            status.HTTP_200_OK: EventFullResponseSerializer,
        },
    ),
    retrieve=extend_schema(
            summary="Show full description of event (with program)",
            responses={
                status.HTTP_200_OK: EventFullResponseSerializer,
                },
        ),
    partial_update=extend_schema(
            summary="Update info about event",
            responses={
                status.HTTP_200_OK: EventFullResponseSerializer,
                },
        ),
    destroy=extend_schema(
            summary="Delete event",
        ),
)
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'option']
    # permission_classes = (ReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter)
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
        return self.serializer_classes.get(
            self.action, self.default_serializer_class)

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
        queryset = queryset.annotate(
            application_status=F('applications__status__name'))
        return queryset.order_by('date')
