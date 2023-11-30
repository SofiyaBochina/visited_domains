from datetime import datetime
from django_filters import rest_framework as filters
from domains.models import Domain


class UnixDateFilter(filters.FilterSet):
    from_timestamp = filters.NumberFilter(
        field_name='created',
        label='From unix timestamp',
        method='filter_from_ts')

    to_timestamp = filters.NumberFilter(
        field_name='created',
        label='To unix timestamp',
        method='filter_to_ts')

    class Meta:
        model = Domain
        fields = ('from_timestamp', 'to_timestamp')

    def filter_from_ts(self, queryset, name, value):
        from_datetime = datetime.fromtimestamp(int(value))
        print(from_datetime)
        return queryset.filter(created__gte=from_datetime)

    def filter_to_ts(self, queryset, name, value):
        to_datetime = datetime.fromtimestamp(int(value))
        return queryset.filter(created__lte=to_datetime)