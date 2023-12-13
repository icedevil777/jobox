from payment import models
from industrial import models as in_models


def get_company_payment_invoices(company: in_models.Company):
    """
    Получить счета на оплату по компании
    :param company:
    :return: Список счётов на оплату
    """
    return models.PaymentInvoice.objects.filter(company=company).order_by('-created_at')


def get_invoice_by_id(invoice_id) -> models.PaymentInvoice:
    """
    Получить счет на оплату по ID
    :param invoice_id:
    :return:
    """
    return models.PaymentInvoice.objects.filter(id=invoice_id).select_related('company').prefetch_related(
        'tinkoff_card_payment').first()
