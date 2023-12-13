from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from datetime import datetime, timedelta
from core_base.models import User
from . import models

from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import Job, ResponseToJob, CompanyWorker


@admin.register(Job)
class JobAdmin(ImportExportModelAdmin):
    class JobResource(resources.ModelResource):
        class Meta:
            model = Job

    change_form_template = "industrial/forms/admin_job_edit_form.html"
    list_display = ["go_text", 'id', 'get_job', 'status', 'company_name',
                    'show_on_main_page', 'created_at']
    list_filter = ('created_at',)
    resource_class = JobResource
    search_fields = ['id', 'title', 'status', 'company__name']

    def go_text(self, *args, **kwargs):
        return "GO"

    def company_name(self, obj):
        return obj.company.name[:30]

    def get_job(self, obj):
        return obj.title[:30]

    actions = [
        'to_publish_job',
        'do_show_on_main_page',
        'dont_show_on_main_page',
        'pay_for_job',
        'to_reject_job',
        'to_close_job',
        'to_expire_job',
        'on_moderation',
        'need_to_paid',
    ]

    @admin.action(description='Полная Публикация вакансий')
    def to_publish_job(self, request, queryset):
        clock_in_half = datetime.now() + timedelta(days=30)
        updated = queryset.update(is_paid=True,
                                  show_on_main_page=True,
                                  status='published',
                                  published_at=datetime.now(),
                                  expire_at=clock_in_half)

        self.message_user(request, ngettext(
            '%d вакансия опубликована.',
            '%d вакансии опубликованы.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Установить статус "ждёт оплаты"')
    def need_to_paid(self, request, queryset):
        updated = queryset.update(is_paid=False,
                                  show_on_main_page=False,
                                  status='need_to_paid',)

        self.message_user(request, ngettext(
            '%d ждёт оплаты.',
            '%d ждут оплаты.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Установить статус "на модерации"')
    def on_moderation(self, request, queryset):
        updated = queryset.update(is_paid=False,
                                  show_on_main_page=False,
                                  status='moderation',)

        self.message_user(request, ngettext(
            '%d на модерации.',
            '%d на модерации.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Сбросить срок публикации')
    def to_expire_job(self, request, queryset):
        updated = queryset.update(is_paid=False,
                                  show_on_main_page=False,
                                  status='expired',)

        self.message_user(request, ngettext(
            '%d срок публикации сброшен.',
            '%d сброс сроков публикации.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Закрыть вакансии')
    def to_close_job(self, request, queryset):
        updated = queryset.update(is_paid=False,
                                  show_on_main_page=False,
                                  status='closed',)

        self.message_user(request, ngettext(
            '%d вакансия закрыта.',
            '%d вакансии закрыты.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Отклонить вакансии')
    def to_reject_job(self, request, queryset):
        updated = queryset.update(is_paid=False,
                                  show_on_main_page=False,
                                  status='rejected',)

        self.message_user(request, ngettext(
            '%d вакансия отклонена.',
            '%d вакансии отклонены.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Оплата вакансий')
    def pay_for_job(self, request, queryset):
        updated = queryset.update(is_paid=True)
        self.message_user(request, ngettext(
            '%d вакансия оплачена.',
            '%d вакансии оплачены.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Показывать на главной странице')
    def do_show_on_main_page(self, request, queryset):
        updated = queryset.update(show_on_main_page=True)
        self.message_user(request, ngettext(
            '%d вакансия будет отображаться.',
            '%d вакансии будут отображаться.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Не показывать на главной странице')
    def dont_show_on_main_page(self, request, queryset):
        updated = queryset.update(show_on_main_page=False)
        self.message_user(request, ngettext(
            '%d вакансия больше не будет отображаться.',
            '%d вакансии больше не будут отображаться.',
            updated,
        ) % updated, messages.SUCCESS)


@admin.register(ResponseToJob)
class ResponseToJobAdmin(ImportExportModelAdmin):
    class ResponseToJobResource(resources.ModelResource):
        class Meta:
            model = ResponseToJob

    resource_class = ResponseToJobResource
    search_fields = ['id', 'name', 'job__title', 'phone', 'job__company__name']
    list_display = ['go_text', 'id', 'company_name', 'get_job', 'name',
                    'phone', 'created_at']
    list_display_links = ['go_text']
    readonly_fields = ['job', 'name', 'phone', 'communication_method']

    list_filter = ('created_at',)

    def go_text(self, *args, **kwargs):
        return "GO"

    def company_name(self, obj):
        return obj.job.company.name[:50]

    def get_job(self, obj):
        return obj.job.title[:30]


@admin.register(models.Company)
class CompanyAdmin(ImportExportModelAdmin):
    class CompanyResource(resources.ModelResource):
        class Meta:
            model = models.Company

    list_display = ['go_text', 'id', 'get_name', 'user', 'inn',
                    'show_on_main_page']
    search_fields = ['id', 'name', 'inn']

    def go_text(self, *args, **kwargs):
        return "GO"

    def get_name(self, obj):
        return obj.name[:50]

    def get_address(self, obj):
        return obj.address[:50]

    actions = [
        'do_show_on_main_page',
        'dont_show_on_main_page',
    ]

    @admin.action(description='Показывать на главной странице')
    def do_show_on_main_page(self, request, queryset):
        updated = queryset.update(show_on_main_page=True)
        self.message_user(request, ngettext(
            '%d компания будет отображаться.',
            '%d компании будут отображаться.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Не показывать на главной странице')
    def dont_show_on_main_page(self, request, queryset):
        updated = queryset.update(show_on_main_page=False)
        self.message_user(request, ngettext(
            '%d компания больше не будет отображаться.',
            '%d компании больше не будут отображаться.',
            updated,
        ) % updated, messages.SUCCESS)


@admin.register(models.CompanyFinanceTransaction)
class CompanyFinanceTransactionAdmin(ImportExportModelAdmin):
    class CompanyFinanceTransactionResource(resources.ModelResource):
        class Meta:
            model = models.CompanyFinanceTransaction

    list_display = ['company_name', 'currency', 'action', 'amount',
                    'company_comment', 'company_technical_comment',
                    'created_at']
    list_filter = ('created_at',)
    search_fields = ['id', 'company__name', 'amount', 'comment',
                     'technical_comment']
    autocomplete_fields = ['company']

    def company_name(self, obj):
        return obj.company.name[:30]

    def company_comment(self, obj):
        return obj.comment[:25]

    def company_technical_comment(self, obj):
        return obj.technical_comment[:25]


@admin.register(models.Applicant)
class ApplicantAdmin(ImportExportModelAdmin):
    class ApplicantResource(resources.ModelResource):
        class Meta:
            model = models.Applicant

    list_display = ['go_text', 'first_name', 'second_name', 'middle_name',
                    'user']

    search_fields = ['id', 'first_name', 'second_name', 'middle_name',
                     'user_email', 'tel']

    def go_text(self, *args, **kwargs):
        return "GO"


@admin.register(models.CompanyReferralChain)
class CompanyReferralChainAdmin(ImportExportModelAdmin):
    class CompanyReferralChainResource(resources.ModelResource):
        class Meta:
            model = models.CompanyReferralChain

    list_display = ['id', 'affiliate', 'referral', 'ref_code',
                    'bonus_transaction']
