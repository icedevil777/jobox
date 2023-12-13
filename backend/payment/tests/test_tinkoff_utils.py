from django.test import TestCase
from payment.services import create_payment_by_tinkoff_card
from industrial.models import Company


class TinkoffUtilsTestCase(TestCase):

    def test_create_new_tinkoff_card_payment(self):
        company = Company.objects.create(
            inn="00007777"
        )
        print(company)
        tinkoff_card_payment = create_payment_by_tinkoff_card(
            company=company,
            amount=40000  # 400 руб
        )

        print(tinkoff_card_payment)
        print(tinkoff_card_payment.__dict__)
