
# Django
from django.utils import timezone

# Models
from ..models.quotes import Quotation, QuoteDetail


class QuotationServices:

    def create_quotation(self, data):
        total_purchase = 0
        total_sale = 0

        # Create quote header
        quotation = self.__create_quotation_header(data['client'])

        # Create quote detail
        quotation_details = data['quotation_details']
        for data_detail in quotation_details:
            quotation_detail = self.__create_quotation_detail(quotation, data_detail)
            total_purchase += quotation_detail.total_purchase
            total_sale += quotation_detail.total_sale

        # Update quot totals
        quotation.total_purchase = total_purchase
        quotation.total_sale = total_sale
        quotation.save()

        return quotation

    def __create_quotation_header(self, client: int):
        today = timezone.now()
        data = {
            'client': client,
            'issuance_date': today,
            'total_purchase': 0,
            'total_sale': 0,
            'is_active': True,
            'status': Quotation.StatusChoices.PENDING,
        }
        return Quotation.objects.create(**data)

    def __create_quotation_detail(self, quotation: Quotation, detalle):
        total_purchase = detalle['purchase_price'] * detalle['quantity']
        total_sale = detalle['selling_price'] * detalle['quantity']
        profit = (total_sale - total_purchase)

        data = {
            'quotation_id': quotation.id,
            'provider': detalle['provider'],
            'item': detalle['item'],
            'purchase_price': detalle['purchase_price'],
            'quantity': detalle['quantity'],
            'selling_price': detalle['selling_price'],
            'total_purchase': total_purchase,
            'total_sale': total_sale,
            'profit': profit
        }
        return QuoteDetail.objects.create(**data)
