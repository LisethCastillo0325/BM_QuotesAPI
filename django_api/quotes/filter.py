
# Django
from django_filters.rest_framework import BaseInFilter, NumberFilter, DateFilter
import rest_framework_filters as filters

# Models
from .models.quotes import Quotation


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class QuotationFilter(filters.FilterSet):
    created__gte = DateFilter(field_name='created', lookup_expr='date__gte')
    created__lte = DateFilter(field_name='created', lookup_expr='date__lte')
    client = NumberInFilter(field_name='client', lookup_expr='in')

    class Meta:
        model = Quotation
        fields = ['created__gte', 'created__lte', 'client']


class QuotationViewFilter(filters.FilterSet):
    created__gte = DateFilter(field_name='created', lookup_expr='date__gte')
    created__lte = DateFilter(field_name='created', lookup_expr='date__lte')

    issuance_date = DateFilter(field_name='issuance_date', lookup_expr='date')
    billing_date = DateFilter(field_name='billing_date', lookup_expr='date')

    class Meta:
        model = Quotation
        fields = (
            'client', 'status', 'issuance_date', 'billing_date',
            'created__gte', 'created__lte'
        )


