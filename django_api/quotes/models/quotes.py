"""Factura model."""


# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from django_api.utils.models import DateBaseModel


class Quotation(DateBaseModel):
    """Quotation model.

    Invoicing of services or services consumed by a client.
    """
    class StatusChoices(models.TextChoices):
        INVOICED = 1, _('INVOICED')
        PENDING = 2, _('PENDING')

    client = models.IntegerField('Client')
    issuance_date = models.DateTimeField('Issuance date', null=True)
    billing_date = models.DateTimeField('Billing date', null=True)
    invoice_number = models.CharField(max_length=15, null=True)
    status = models.CharField(max_length=1, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    total_purchase = models.IntegerField('Total purchase', default=0)
    total_sale = models.IntegerField('Total sale', default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Quotation {}".format(self.id)

    class Meta(DateBaseModel.Meta):
        db_table = 'quotations'
        managed = True
        verbose_name = 'Quotation'
        verbose_name_plural = 'Quotation'

class QuoteDetail(DateBaseModel):

    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    provider = models.IntegerField()
    item = models.IntegerField()
    purchase_price = models.FloatField('Purchase price')
    quantity = models.IntegerField('Current consumption')
    selling_price = models.FloatField('Selling price')
    total_purchase = models.FloatField('Total Purchase')
    total_sale = models.FloatField('Total Sale')
    profit = models.IntegerField('Profit')

    def __str__(self):
        return "Quote detail {}".format(self.quotation_id)

    class Meta(DateBaseModel.Meta):
        db_table = 'quote_detail'
        managed = True
        verbose_name = 'Quote detail'
        verbose_name_plural = 'Quotes detail'
