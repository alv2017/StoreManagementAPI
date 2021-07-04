from django_filters import rest_framework as filters
from .models import Order


class OrderFilter(filters.FilterSet):
    created_from = filters.DateTimeFilter(
        field_name='created', lookup_expr='gte'
    )
    created_to = filters.DateTimeFilter(
        field_name='created', lookup_expr='lte'
    )

    class Meta:
        model = Order
        fields = (
            'last_name',
            'email',
            'country',
            'created',
            'created_from',
            'created_to'
        )
