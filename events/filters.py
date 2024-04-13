import django_filters
from django.utils import timezone

from .models_event import Event


class EventFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(method='filter_city')
    start_date = django_filters.DateTimeFilter(
        field_name='date', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(
        field_name='date', lookup_expr='lte')
    is_favorited = django_filters.NumberFilter(
        field_name='is_favorited',
        method='filter_is_favorited')
    is_applied = django_filters.NumberFilter(
        field_name='is_applied',
        method='filter_is_applied')
    direction = django_filters.CharFilter(method='filter_direction')
    formats = django_filters.CharFilter(method='filter_formats')
    status = django_filters.CharFilter(method='filter_status')

    delete_nearest = django_filters.NumberFilter(
        field_name='delete_nearest',
        method='filter_delete_nearest')

    class Meta:
        model = Event
        fields = ('city', )

    def filter_is_favorited(self, queryset, name, value):
        if value is not None:
            return queryset.filter(is_favorited=value)
        return queryset

    def filter_is_applied(self, queryset, name, value):
        if value is not None:
            return queryset.filter(is_applied=value)
        return queryset

    def filter_city(self, qs, name, value):
        return qs.filter(city__in=self.request.GET.getlist('city'))

    def filter_direction(self, qs, name, value):
        return qs.filter(
            direction__slug__in=self.request.GET.getlist('direction'))

    def filter_formats(self, qs, name, value):
        return qs.filter(format__slug__in=self.request.GET.getlist('formats'))

    def filter_status(self, qs, name, value):
        return qs.filter(status__slug__in=self.request.GET.getlist('status'))

    def filter_delete_nearest(self, queryset, name, value):
        if value is not None:
            now = timezone.now()
            queryset.filter(date__gte=now).order_by('date')
            nearest_events_ids = queryset[:value].values('id')
            return queryset.exclude(id__in=nearest_events_ids)
        return queryset
