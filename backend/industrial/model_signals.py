from . import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .services import create_new_company_finance_transaction


@receiver(post_save, sender=models.Company)
def company_created(sender, instance: models.Company, created, **kwargs):
    if created:
        bonus_transaction = create_new_company_finance_transaction(
            company=instance,
            currency=models.CompanyFinanceTransaction.CURRENCIES.bonus_point,
            action=models.CompanyFinanceTransaction.ACTIONS.bonus_debiting,
            amount=1,
            comment='Бонус за регистрацию',
            technical_comment='Bonus for registration'
        )
