from core_base.logger import get_logger
from . import models
from industrial import models as in_models
from payment.tinkoff_utils import create_new_tinkoff_card_payment, get_tinkoff_card_payment
from django.conf import settings
import uuid
from django.db import transaction
import logging


_terminal_key = '1644315234504'
_terminal_password = '1g15f2evlmgps8pj'

logger = get_logger('pay_serv_logs', level=logging.INFO)


@transaction.atomic
def create_payment_by_tinkoff_card(company: in_models.Company, amount: int):
    new_payment_invoice = models.PaymentInvoice.objects.create(
        status=models.PaymentInvoice.Statuses.waiting,
        amount=amount,
        comment=f"Пополнение лицевого счёта №{company.personal_account}, банковской картой.",
        company=company
    )
    logger.info(f'new_payment_invoice {new_payment_invoice}')
    new_tinkoff_card_payment = models.TinkoffCardPayment.objects.create(
        payment_invoice=new_payment_invoice,
        terminal_key=_terminal_key,
        order_id=new_payment_invoice.invoice_number,  # str(uuid.uuid4()),
        amount=amount,
        description=new_payment_invoice.comment
    )
    tf_res = create_new_tinkoff_card_payment(
        terminal_key='1644315234504',
        password='1g15f2evlmgps8pj',
        amount=new_tinkoff_card_payment.amount,
        order_id=new_tinkoff_card_payment.order_id,
        description=new_tinkoff_card_payment.description,
        success_url=settings.TINKOFF_SUCCESS_URL.format(invoice_id=new_payment_invoice.id)
    )
    logger.info(f'tf_res {tf_res}')
    new_tinkoff_card_payment.tinkoff_payment_id = tf_res['PaymentId']
    new_tinkoff_card_payment.tinkoff_payment_url = tf_res['PaymentURL']
    new_tinkoff_card_payment.status = tf_res['Status']
    new_tinkoff_card_payment.save()
    logger.info(f'new_tinkoff_card_payment {new_tinkoff_card_payment}')
    return new_tinkoff_card_payment


@transaction.atomic
def refresh_tinkoff_card_payment(tinkoff_card_payment: models.TinkoffCardPayment):
    inf = get_tinkoff_card_payment(
        _terminal_key,
        _terminal_password,
        payment_id=tinkoff_card_payment.tinkoff_payment_id
    )
    logger.info(f'inf {inf}')
    tinkoff_card_payment.status = inf['Status']
    tinkoff_card_payment.save()