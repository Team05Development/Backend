import django_filters
from django_filters import MultipleChoiceFilter
from django_filters.fields import MultipleChoiceField
from django.utils import timezone

from .models_event import Event


class MultipleCharField(MultipleChoiceField):
    def validate(self, _):
        pass


class MultipleCharFilter(MultipleChoiceFilter):
    field_class = MultipleCharField


class EventFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    address = MultipleCharFilter(field_name="address", lookup_expr="contains")
    start_date = django_filters.DateTimeFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='date', lookup_expr='lte')
    is_favorited = django_filters.NumberFilter(
        field_name='is_favorited',
        method='filter_is_favorited')
    is_applied = django_filters.NumberFilter(
        field_name='is_applied',
        method='filter_is_applied')
    direction = django_filters.CharFilter(method='filter_direction')
    formats = django_filters.CharFilter(method='filter_formats')
    status = django_filters.CharFilter(method='filter_status')
    
    most_visited = django_filters.NumberFilter(
        field_name='most_visited',
        method='filter_most_visited')

    class Meta:
        model = Event
        fields = ('address',)

    def filter_is_favorited(self, queryset, name, value):
        if value is not None:
            return queryset.filter(is_favorited=value)
        return queryset

    def filter_is_applied(self, queryset, name, value):
        if value is not None:
            return queryset.filter(is_applied=value)
        return queryset
    
    def filter_direction(self, qs, name, value):
        return qs.filter(direction__slug__in=self.request.GET.getlist('direction'))
    
    def filter_formats(self, qs, name, value):
        return qs.filter(format__slug__in=self.request.GET.getlist('formats'))
    
    def filter_status(self, qs, name, value):
        return qs.filter(status__slug__in=self.request.GET.getlist('status'))
    
    def filter_most_visited(self, queryset, name, value):
        if value is not None:
            now = timezone.now()
            queryset.filter(date__gte=now).order_by('date')
            nearest_events_ids = queryset[:4].values('id')
            return queryset.exclude(id__in=nearest_events_ids).order_by('-total_applications')[:value]
        return queryset