from django_filters import rest_framework as filters
from losb.models import City


class CityFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = City
        fields = ['name']
