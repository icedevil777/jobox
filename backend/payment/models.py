from django.db import models


class ModelBase(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class PaymentInvoice(ModelBase):
    """Счеть на оплату """

    class Statuses(models.TextChoices):
        waiting = 'waiting', "Ожидается"
        succeed = 'succeed', "Успешно"
        canceled = 'canceled', "Отменен"

    status = models.CharField(max_length=20, choices=Statuses.choices)
    amount = models.FloatField()
    comment = models.CharField(max_length=500)

    company = models.ForeignKey("industrial.Company",
                                on_delete=models.RESTRICT,
                                related_name='payment_invoices')

    @property
    def invoice_number(self):
        return 3600000 + self.id

    def __str__(self):
        return f"{self.company}, {self.status}, {self.amount}"


class TinkoffCardPayment(ModelBase):
    """Тинькофф платеж картой"""

    payment_invoice = models.OneToOneField(
        PaymentInvoice,
        on_delete=models.RESTRICT,
        related_name="tinkoff_card_payment"
    )
    terminal_key = models.CharField(max_length=20)
    status = models.CharField(max_length=20, blank=True, null=True)
    tinkoff_payment_id = models.CharField(max_length=20, blank=True, null=True)
    tinkoff_payment_url = models.CharField(max_length=150, blank=True,
                                           null=True)
    order_id = models.CharField(max_length=40)
    amount = models.FloatField()
    description = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.tinkoff_payment_id}, {self.status}, {self.amount}"
