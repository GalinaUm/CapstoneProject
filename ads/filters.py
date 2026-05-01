from django_filters import rest_framework as filters
from .models import Ad

class AdFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    author = filters.CharFilter(field_name='author__email', lookup_expr='icontains')

    created_after = filters.DateTimeFilter(field_name='created_date', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_date', lookup_expr='lte')

    class Meta:
        model = Ad
        fields = ('title', 'description', 'price', 'author', 'created_at')