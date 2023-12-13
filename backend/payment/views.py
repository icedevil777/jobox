import logging
import json
from django.views import View
from django.http import JsonResponse
from django.shortcuts import reverse
from django.http.request import HttpRequest

from core_base.logger import get_logger
from industrial.mixins import OnlyIndustrialWorkerMixin
from payment.models import PaymentInvoice
from payment import selectors as py_selectors
from payment import services as py_services

logger = get_logger('pay_views_log', level=logging.INFO)


class NewTinkoffCardPayment(OnlyIndustrialWorkerMixin, View):
    def post(self, request: HttpRequest):
        company_instance = request.user.industrial_worker.company
        js = json.loads(request.body)
        amount = int(js['amount'])
        if company_instance and amount:
            tf_card_payment_instance = py_services.create_payment_by_tinkoff_card(
                company=company_instance,
                amount=amount
            )
            return JsonResponse(
                {
                    'invoice_url': reverse(
                        'industrial:payment_invoice',
                        kwargs={
                            'invoice_id': tf_card_payment_instance.payment_invoice.id}
                    ),
                    'payment_url': tf_card_payment_instance.tinkoff_payment_url
                }
            )
