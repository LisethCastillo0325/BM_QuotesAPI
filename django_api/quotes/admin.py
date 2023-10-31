from django.contrib import admin

from .models.quotes import Quotation, QuoteDetail


class QuotationAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'total_purchase', 'total_sale', 'created')


class QuoteDetailAdmin(admin.ModelAdmin):
    list_display = ('quotation', 'provider', 'item', 'purchase_price', 'quantity', 
                    'selling_price', 'total_purchase', 'total_sale', 'profit')


# Register your models here.
admin.site.register(Quotation, QuotationAdmin)
admin.site.register(QuoteDetail, QuoteDetailAdmin)
