from rest_framework import serializers
from payment import models


class PaymentInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentInvoice
        fields = '__all__'
