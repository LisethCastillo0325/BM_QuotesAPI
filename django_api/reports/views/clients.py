"""Reportes Clientes."""

# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

# Monitoring
from prometheus_client import Counter

# Métricas personalizadas
prometheus_c = Counter(
    'reports_trafic', 'Number of request received in the Financial Information Report', ['method', 'endpoint'])

# Models
from django_api.quotes.models import Quotation

# Serializers
from ..serializers.clients import ReportClientQuoteSerializer, FiltersReportClientQuoteSerializer

# Filters
from django_api.quotes.filter import QuotationFilter


class ClientReportsViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=['GET'])
    def financial_information(self, request, **kwargs):
        prometheus_c.labels('get', 'financial_information/').inc()
        """Financial Information of Clients

        Report of financial information of clients registered in the system.
        """

        qs = Quotation.objects.all()
        serializer = FiltersReportClientQuoteSerializer(
            data=request.GET,
        )
        serializer.is_valid(raise_exception=True)
        filters = serializer.data
        qs = QuotationFilter(filters, queryset=qs).qs

        if not qs.exists():
            return Response(data={
                'detail': 'No data exists between the dates {} and {}.'.format(
                    filters['created__gte'], filters['created__lte'])
            }, status=status.HTTP_404_NOT_FOUND)

        else:
            data = ReportClientQuoteSerializer(instance=qs, many=True).data
            return Response(data=data, status=status.HTTP_200_OK)
