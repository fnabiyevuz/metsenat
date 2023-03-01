from django_filters import rest_framework as filters
from .models import Sponsors


class SponsorsFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Sponsors
        fields = ['summa', 'status', 'created_at']
