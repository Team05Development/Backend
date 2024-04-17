from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from .models_auxiliary import (
    Direction, Format,
    EventStatus, ApplicationStatus, )

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
