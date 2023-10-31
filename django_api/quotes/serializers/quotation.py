""" Quotation serializers """

# Django REST Framework
from rest_framework import serializers

# Models
from django_api.quotes.models import Quotation, QuoteDetail

# Serializers
from django_api.utils.serializers import  DataChoiceSerializer

# Services
from django_api.quotes.services.quotation import QuotationServices


class QuoteDetailModelSerializer(serializers.ModelSerializer):

    total_purchase = serializers.ReadOnlyField()
    total_sale = serializers.ReadOnlyField()
    profit = serializers.ReadOnlyField()
   
    class Meta:
        model = QuoteDetail
        exclude = ('quotation',)


class QuotationModelSerializer(serializers.ModelSerializer):
    status = DataChoiceSerializer()
    quotation_details = serializers.SerializerMethodField()
    total_purchase = serializers.SerializerMethodField()
    total_sale = serializers.SerializerMethodField()
    issuance_date = serializers.SerializerMethodField()
    billing_date = serializers.SerializerMethodField()

    def get_issuance_date(self, obj):
        return obj.issuance_date.strftime('%Y-%m-%d')

    def get_billing_date(self, obj):
        if obj.billing_date:
            return obj.billing_date.strftime('%Y-%m-%d')
        return None

    def get_quotation_details(self, obj):
        try:
            queryset = QuoteDetail.objects.filter(quotation_id=obj.id)
            return QuoteDetailModelSerializer(instance=queryset, many=True).data
        except Exception:
            return None
    
    def get_total_purchase(self, obj):
        total = 0
        queryset = QuoteDetail.objects.filter(quotation_id=obj.id)
        for detail in queryset:
            total += detail.total_purchase
        return total
    
    def get_total_sale(self, obj):
        total = 0
        queryset = QuoteDetail.objects.filter(quotation_id=obj.id)
        for detail in queryset:
            total += detail.total_sale
        return total

    class Meta:
        model = Quotation
        fields = ('__all__')




class AddQuotationSerializer(serializers.ModelSerializer):

    quotation_details = QuoteDetailModelSerializer(many=True)
    
    class Meta:
        model = Quotation
        fields = '__all__'

    def create(self, validated_data):
        service = QuotationServices()
        quotation = service.create_quotation(data=validated_data)
        return quotation

    def update(self, instance, validated_data):
        """ TEST """
        pass