from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from uuid import uuid4
from jsonfield import JSONField
from .querysets.job import CustomJobManager, CustomAppManager


def uuid4_generator():
    return str(uuid4())


class ModelBase(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Company(models.Model):
    """Компания"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='company_user', )

    ref_code = models.CharField(max_length=40, default=uuid4)
    name = models.CharField(max_length=1024, null=True, blank=True)
    opf_full = models.CharField(max_length=250, null=True, blank=True)
    director_name = models.CharField(max_length=128, null=True, blank=True)
    director_post = models.CharField(max_length=128, null=True, blank=True)

    registration_date = models.DateField(null=True, blank=True)

    address = models.TextField(null=True, blank=True)
    about_company = models.TextField(null=True, blank=True, default='')
    company_description = models.TextField(null=True, blank=True, default='')

    inn = models.CharField(max_length=20, null=True, blank=True, unique=True)
    ogrn = models.CharField(max_length=20, null=True, blank=True, unique=True)
    kpp = models.CharField(max_length=20, null=True, blank=True)

    dadata_date = JSONField(default=dict)

    show_on_main_page = models.BooleanField(
        verbose_name="на гл стр",
        default=False)

    brand_name = models.CharField(max_length=150, null=True, blank=True, default='')
    brand_logo = models.ImageField(upload_to='company/brand_logos', null=True,
                                   blank=True)

    @property
    def personal_account(self):
        """Лицевой счет"""

        pa = 36000000 + self.id
        return str(pa)

    @property
    def registration_date_normal_view(self):
        if self.registration_date:
            return self.registration_date.strftime('%m.%d.%Y')
        else:
            return '-'

    def __str__(self):
        return f'{self.address} | {self.name} '

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"


class Applicant(ModelBase):
    STATUSES = (
        ('published', 'Опубликована'),
        ('not_published', 'Не опубликована'),

    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='app_user')

    have_resume = models.BooleanField(default=False)
    have_tabel = models.BooleanField(default=False)
    have_education = models.BooleanField(default=False)
    have_experience = models.BooleanField(default=False)

    status = models.CharField(max_length=20, default=STATUSES[0][1],
                              choices=STATUSES)

    name_app = models.CharField(max_length=128, null=True, blank=True)
    date_of_birth = models.DateField('%г-%м-%д', null=True, blank=True)

    first_name = models.CharField(max_length=64, null=True, blank=True)
    second_name = models.CharField(max_length=64, null=True, blank=True)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    is_agree_with_agreement = models.BooleanField(default=False)
    qualification = models.CharField(max_length=64, default='')

    user_email = models.CharField(max_length=64, unique=True, blank=True,
                                  null=True, )
    tel = models.CharField(max_length=64, null=True, blank=True)

    salary = models.IntegerField(blank=True, null=True, default=0)
    salary_condition = models.ForeignKey('core_base.AdditionalSalaryCondition',
                                         on_delete=models.PROTECT,
                                         blank=True, null=True,
                                         related_name='app_salary_condition')

    about_app = models.TextField(max_length=1000, blank=True, null=True)
    about_experience = models.TextField(max_length=1000, blank=True, null=True)
    about_education = models.TextField(max_length=1000, blank=True, null=True)

    experience = models.ForeignKey('core_base.Experience',
                                   null=True, blank=True,
                                   on_delete=models.PROTECT,
                                   related_name='apps')
    employment_type = models.ForeignKey('core_base.EmploymentType',
                                        null=True, blank=True,
                                        on_delete=models.PROTECT,
                                        related_name='apps')
    work_schedule = models.ForeignKey('core_base.WorkSchedule',
                                      null=True, blank=True,
                                      on_delete=models.PROTECT,
                                      related_name="apps")
    location = models.ForeignKey('core_base.Location',
                                 null=True, blank=True,
                                 on_delete=models.PROTECT,
                                 related_name='apps')
    tags_app = models.ManyToManyField('core_base.TagApp',
                                      related_name='tags_app')
    ind_tags = models.ForeignKey('core_base.IndividualTag',
                                 on_delete=models.RESTRICT,
                                 null=True, blank=True,
                                 related_name='ind_app_tegs')

    show_on_main_page = models.BooleanField(verbose_name="на стр вакансий",
                                            default=True)

    def __str__(self):
        return f'{self.first_name} | {self.second_name} | {self.middle_name}'

    class Meta:
        verbose_name = "Соискатель"
        verbose_name_plural = "Соискатели"


class CompanyNotifications(ModelBase):
    """Уведомдления компании"""

    company = models.ForeignKey(Company, on_delete=models.RESTRICT,
                                related_name='notifications')


class CompanyWorker(models.Model):
    """Работник компании / Администратор"""

    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                related_name='workers')
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='industrial_worker')

    email = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    position = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=250, null=True, blank=True)

    is_agree_with_agreement = models.BooleanField(default=False)

    is_administrator = models.BooleanField(default=False)


class Job(ModelBase):
    """Вакансии"""
    STATUSES = (
        ('moderation', 'На модерации'),
        ('need_to_paid', 'Ждёт оплаты'),
        ('rejected', 'Отклонена'),
        ('expired', 'Истек срок публикации'),
        ('closed', 'Closed'),
        ('published', 'Опубликована'),
    )

    is_paid = models.BooleanField(default=False)

    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                related_name='jobs')

    status = models.CharField(max_length=20, default=STATUSES[0][0],
                              choices=STATUSES)
    published_at = models.DateTimeField(null=True, blank=False)
    expire_at = models.DateTimeField(null=True, blank=False)

    seo_title = models.CharField(max_length=250, null=True, blank=True)
    seo_description = models.CharField(max_length=4000, null=True, blank=True)
    seo_keywords = models.CharField(max_length=4000, null=True, blank=True)
    seo_image = models.FileField(upload_to='meta_images', null=True, blank=True)

    title = models.CharField(max_length=250)
    qualification = models.CharField(max_length=250, blank=True, default='')

    category = models.ForeignKey('core_base.JobCategory',
                                 on_delete=models.PROTECT, related_name='jobs')
    experience = models.ForeignKey('core_base.Experience',
                                   on_delete=models.PROTECT,
                                   related_name='jobs')
    employment_type = models.ForeignKey('core_base.EmploymentType',
                                        on_delete=models.PROTECT,
                                        related_name='jobs')
    work_schedule = models.ForeignKey('core_base.WorkSchedule',
                                      on_delete=models.PROTECT,
                                      related_name="jobs")
    location = models.ForeignKey('core_base.Location',
                                 on_delete=models.PROTECT, related_name='jobs')
    salary = models.IntegerField(blank=True, null=True, default=0)
    salary_condition = models.ForeignKey('core_base.AdditionalSalaryCondition',
                                         default='В месяц',
                                         on_delete=models.PROTECT,
                                         related_name='salary_additional_condition')

    tags = models.ManyToManyField('core_base.Tag', related_name='job_tegs', blank=True)
    ind_tags = models.ManyToManyField('core_base.IndividualTag', related_name='ind_job_tegs', blank=True)
    all_ind_tags = models.ManyToManyField('core_base.IndividualTag', related_name='all_ind_job_tegs', blank=True)

    about_job = models.TextField(max_length=4000)
    company_offers = models.TextField(max_length=4000)
    requirements = models.TextField(max_length=4000)

    recruiter_name = models.CharField(max_length=250)
    recruiter_position = models.CharField(max_length=250)
    recruiter_phone = models.CharField(max_length=250)
    recruiter_communication_method = models.ForeignKey(
        'core_base.CommunicationMethod', on_delete=models.PROTECT,
        related_name='jobs')
    recruiter_email = models.CharField(max_length=100)

    show_on_main_page = models.BooleanField(
        verbose_name="на гл стр",
        default=False)

    @property
    def expires_after_days(self):
        if self.status == 'published' and self.expire_at is not None:
            return (self.expire_at - timezone.now()).days
        return 0

    @property
    def published_at_simple(self):
        if self.published_at:
            return self.published_at.strftime("%d.%m.%Y")

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.is_paid:
            if self.status != 'published' and self.status != 'rejected' and \
                    self.status != 'closed':
                self.status = 'moderation'
        else:
            self.status = 'need_to_paid'

        return super(Job, self).save()

    objects = CustomJobManager()


class ResponseToJob(ModelBase):
    """Отклик на вакансию"""

    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name='responses')
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    communication_method = models.ForeignKey(
        'core_base.CommunicationMethod', on_delete=models.PROTECT,
        related_name='responses', null=True, blank=True)

    class Meta:
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"


class CompanyFinanceTransaction(ModelBase):
    """Финансовые транзакции"""

    class CURRENCIES(models.TextChoices):
        bonus_point = 'bonus_point', "Бонус"
        ruble = 'ruble', "Рубль"

    class ACTIONS(models.TextChoices):
        balance_replenishment = 'balance_replenishment', 'Пополнение баланса'
        publication = 'publication', 'Публикация'
        bonus_credit = 'bonus_credit', 'Списание бонуса'
        bonus_debiting = 'bonus_debiting', 'Зачисление бонуса'

    uniq_uuid = models.CharField(max_length=40, default=uuid4_generator)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,
                                related_name='transactions',
                                null=True, blank=True)

    currency = models.CharField(max_length=20, choices=CURRENCIES.choices)
    action = models.CharField(max_length=30, choices=ACTIONS.choices)

    amount = models.FloatField()

    comment = models.TextField(max_length=1024, null=True, blank=True)
    technical_comment = models.TextField(max_length=1024)

    payment_for_job = models.OneToOneField(Job, on_delete=models.SET_NULL,
                                           related_name="payment",
                                           null=True, blank=True)

    payment_invoice = models.OneToOneField('payment.PaymentInvoice',
                                           on_delete=models.SET_NULL,
                                           null=True, blank=True,
                                           related_name='transaction')

    # time_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Финансовая транзакция"
        verbose_name_plural = "Финансовые транзакции"


class CompanyReferralChain(ModelBase):
    """Реферальная система"""

    affiliate = models.ForeignKey(Company, on_delete=models.SET_NULL,
                                  related_name='affiliate',
                                  null=True, blank=True)

    referral = models.OneToOneField(Company, on_delete=models.SET_NULL,
                                    related_name='referral',
                                    null=True, blank=True)

    ref_code = models.CharField(max_length=50, null=True, blank=True)
    bonus_transaction = models.ForeignKey(CompanyFinanceTransaction,
                                          on_delete=models.SET_NULL,
                                          related_name='referral_chain',
                                          null=True, blank=True)
