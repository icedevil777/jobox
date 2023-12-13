from import_export.admin import ImportExportModelAdmin
from import_export import resources

from django.contrib import admin
from . import models


@admin.register(models.PaymentInvoice)
class PaymentInvoiceAdmin(ImportExportModelAdmin):
    class PaymentInvoiceResource(resources.ModelResource):
        class Meta:
            model = models.PaymentInvoice

    list_display = ['go_text', 'get_company_name', 'amount', 'status',
                    'get_comment',
                    'created_at']
    list_filter = ['created_at']
    search_fields = ['id', 'company__name', 'amount', 'comment', ]

    def get_company_name(self, obj):
        return obj.company.name[:20]

    def get_comment(self, obj):
        return obj.comment[:30]

    def go_text(self, *args, **kwargs):
        return "GO"


@admin.register(models.TinkoffCardPayment)
class TinkoffCardPaymentAdmin(ImportExportModelAdmin):
    class TinkoffCardPaymentResource(resources.ModelResource):
        class Meta:
            model = models.TinkoffCardPayment

    list_display = ['go_text', 'get_company_name', 'amount', 'description', 'created_at']

    list_filter = ['created_at']

    search_fields = ['id', 'payment_invoice__company__name', 'amount', 'description']

    def get_company_description(self, obj):
        return obj.description[:50]

    def get_company_name(self, obj):
        return obj.payment_invoice.company.name[:20]

    def go_text(self, *args, **kwargs):
        return "GO"
