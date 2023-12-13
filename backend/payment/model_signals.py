from . import models
from industrial import models as in_models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from industrial import services as in_services


@receiver(post_save, sender=models.PaymentInvoice)
def payment_invoice_saved(sender, instance: models.PaymentInvoice, created, **kwargs):
    # Если платеж успешный
    if instance.status == models.PaymentInvoice.Statuses.succeed:
        if not hasattr(instance, 'transaction'):
            in_services.create_new_company_finance_transaction(
                company=instance.company,
                currency=in_models.CompanyFinanceTransaction.CURRENCIES.ruble,
                action=in_models.CompanyFinanceTransaction.ACTIONS.balance_replenishment,
                amount=instance.amount,
                comment=instance.comment,
                technical_comment=instance.comment,
                payment_invoice=instance
            )
        else:
            # Если сумма платежа поменялось
            if instance.transaction.amount != instance.amount:
                instance.transaction.amount = instance.amount
                instance.transaction.save()

            if instance.transaction.comment != instance.comment:
                instance.transaction.comment = instance.comment
                instance.transaction.save()

    # Если не завершен
    if instance.status != models.PaymentInvoice.Statuses.succeed:
        if hasattr(instance, 'transaction'):
            instance.transaction.delete()


@receiver(post_save, sender=models.TinkoffCardPayment)
def tinkoff_card_payment_saved(sender, instance: models.TinkoffCardPayment, created, **kwargs):

    # Если платеж успешный
    if instance.status == "CONFIRMED":
        if instance.payment_invoice.status != models.PaymentInvoice.Statuses.succeed:
            instance.payment_invoice.status = models.PaymentInvoice.Statuses.succeed
            instance.payment_invoice.save()
    else:
        instance.payment_invoice.status = models.PaymentInvoice.Statuses.waiting
        instance.payment_invoice.save()
