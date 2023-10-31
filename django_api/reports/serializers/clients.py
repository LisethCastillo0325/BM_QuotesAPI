""" Reporte clientes serializer """

# Django REST Framework
from rest_framework import serializers

# Models
from django_api.quotes.models import Quotation

# Serializers
from django_api.utils.serializers import  DataChoiceSerializer


class ReportClientQuoteSerializer(serializers.ModelSerializer):
    status = DataChoiceSerializer()
    
    class Meta:
        model = Quotation
        fields = '__all__'

class FiltersReportClientQuoteSerializer(serializers.Serializer):
    created__gte = serializers.DateField(required=False)
    created__lte = serializers.DateField(required=False)
    clients = serializers.CharField(required=False)
