from rest_framework.generics import ListAPIView
from rest_framework.mixins import RetrieveModelMixin

from events.models_auxiliary import (
    ApplicationStatus,
    Direction,
    EventStatus,
    Format
)
from events.serializers_auxiliary import (
    DirectionSerializer,
    FormatSerializer,
    EventStatusSerializer,
    ApplicationStatusSerializer
)


class ListRetrieveAPIView(RetrieveModelMixin, ListAPIView):
    pass


class DirectionAPIView(ListRetrieveAPIView):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer


class FormatAPIView(ListRetrieveAPIView):
    queryset = Format.objects.all()
    serializer_class = FormatSerializer


class EventStatusAPIView(ListRetrieveAPIView):
    queryset = EventStatus.objects.all()
    serializer_class = EventStatusSerializer


class ApplicationStatusAPIView(ListRetrieveAPIView):
    queryset = ApplicationStatus.objects.all()
    serializer_class = ApplicationStatusSerializer
