from os import path
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.contrib import admin
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views import View
from django.contrib import messages
from django.utils.translation import ngettext
from core_base import models
from import_export.admin import ImportExportModelAdmin
from import_export import resources


@admin.register(models.User)
class UserAdmin(ImportExportModelAdmin):
    class UserResource(resources.ModelResource):
        class Meta:
            model = models.User

    list_display = ['go_text', 'id', 'email', 'is_email_confirmed']
    search_fields = ['id', 'email']

    def go_text(self, *args, **kwargs):
        return "GO"


@admin.register(models.JobCategory)
class JobCategoryAdmin(ImportExportModelAdmin):
    class JobCategoryResource(resources.ModelResource):
        class Meta:
            model = models.JobCategory

    list_display = ['title', 'icon_code', 'show_on_main_page']


@admin.register(models.Experience)
class ExperienceAdmin(ImportExportModelAdmin):
    class ExperienceResource(resources.ModelResource):
        class Meta:
            model = models.Experience
    list_display = ['title']


@admin.register(models.EmploymentType)
class EmploymentTypeAdmin(ImportExportModelAdmin):
    class EmploymentTypeResource(resources.ModelResource):
        class Meta:
            model = models.EmploymentType
    list_display = ['title']


@admin.register(models.WorkSchedule)
class WorkScheduleAdmin(ImportExportModelAdmin):
    class WorkScheduleResource(resources.ModelResource):
        class Meta:
            model = models.WorkSchedule
    list_display = ['title']


@admin.register(models.AdditionalSalaryCondition)
class AdditionalSalaryConditionAdmin(ImportExportModelAdmin):
    class AdditionalSalaryConditionResource(resources.ModelResource):
        class Meta:
            model = models.AdditionalSalaryCondition
    list_display = ['title']


@admin.register(models.Tag)
class TagAdmin(ImportExportModelAdmin):
    class TagResource(resources.ModelResource):
        class Meta:
            model = models.Tag
    list_display = ['title', 'show_on_main_page']


@admin.register(models.TagApp)
class TagAppAdmin(ImportExportModelAdmin):
    class TagResource(resources.ModelResource):
        class Meta:
            model = models.TagApp
    list_display = ['title', 'show_on_main_page']


@admin.register(models.IndividualTag)
class IndividualTagAdmin(ImportExportModelAdmin):
    class IndividualTagResource(resources.ModelResource):
        class Meta:
            model = models.IndividualTag
    list_display = ['title', 'show_on_main_page']


@admin.register(models.CommunicationMethod)
class CommunicationMethodAdmin(ImportExportModelAdmin):
    class CommunicationMethodResource(resources.ModelResource):
        class Meta:
            model = models.CommunicationMethod
    list_display = ['title', 'icon_code']


@admin.register(models.Location)
class LocationAdmin(ImportExportModelAdmin):
    class LocationResource(resources.ModelResource):
        class Meta:
            model = models.Location
    list_display = ['region', 'city']


@admin.register(models.BlogCategory)
class BlogCategoryAdmin(ImportExportModelAdmin):
    class BlogCategoryResource(resources.ModelResource):
        class Meta:
            model = models.BlogCategory
    list_display = ['title']


@admin.register(models.BlogAuthor)
class BlogAuthorAdmin(ImportExportModelAdmin):
    class BlogAuthorResource(resources.ModelResource):
        class Meta:
            model = models.BlogAuthor
    list_display = ['name']


@admin.register(models.ApplicationsToAdmin)
class ApplicationsToAdminAdmin(ImportExportModelAdmin):
    class ApplicationsToAdminResource(resources.ModelResource):
        class Meta:
            model = models.ApplicationsToAdmin
    list_display = ['created_at', 'name', 'email']


@admin.register(models.SystemImages)
class SystemImagesAdmin(ImportExportModelAdmin):
    class SystemImagesResource(resources.ModelResource):
        class Meta:
            model = models.SystemImages
    list_display = ['name', 'file']


@admin.register(models.Blog)
class BlogAdmin(ImportExportModelAdmin):
    class BlogResource(resources.ModelResource):
        class Meta:
            model = models.Blog

    list_display = ['title', 'category', 'author', 'created_at',
                    'show_on_main_page', 'show_on_for_company_page',
                    'show_on_news_page']
    actions = [
        'do_show_on_main_page',
        'do_show_on_for_company_page',
        'do_show_on_news_page',
        'dont_show_on_main_page',
        'dont_show_on_for_company_page',
        'dont_show_on_news_page',
    ]

    @admin.action(description='Показывать на главной странице')
    def do_show_on_main_page(self, request, queryset):
        updated = queryset.update(show_on_main_page=True)
        self.message_user(request, ngettext(
            '%d новость будет отображаться.',
            '%d новости будут отображаться.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Показывать на странице для работодателей ')
    def do_show_on_for_company_page(self, request, queryset):
        updated = queryset.update(show_on_for_company_page=True)
        self.message_user(request, ngettext(
            '%d новость будет отображаться.',
            '%d новости будут отображаться.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Показывать на странице новостей ')
    def do_show_on_news_page(self, request, queryset):
        updated = queryset.update(show_on_news_page=True)
        self.message_user(request, ngettext(
            '%d новость будет отображаться.',
            '%d новости будут отображаться.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Не показывать на главной странице')
    def dont_show_on_main_page(self, request, queryset):
        updated = queryset.update(show_on_main_page=False)
        self.message_user(request, ngettext(
            '%d новость больше не будет отображаться.',
            '%d новости больше не будут отображаться.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Не показывать на странице для работодателей ')
    def dont_show_on_for_company_page(self, request, queryset):
        updated = queryset.update(show_on_for_company_page=False)
        self.message_user(request, ngettext(
            '%d новость больше не будет отображаться.',
            '%d новости больше не будут отображаться.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description='Не показывать на странице новостей')
    def dont_show_on_news_page(self, request, queryset):
        updated = queryset.update(show_on_news_page=False)
        self.message_user(request, ngettext(
            '%d новость не будет отображаться.',
            '%d новости больше не будут отображаться.',
            updated,
        ) % updated, messages.SUCCESS)


@admin.register(models.EducationLevel)
class EducationLevelAdmin(ImportExportModelAdmin):
    class EducationLevelResource(resources.ModelResource):
        class Meta:
            model = models.EducationLevel

    list_display = ['id', 'title']


@admin.register(models.EducationPlace)
class EducationPlaceAdmin(ImportExportModelAdmin):
    class EducationPlaceResource(resources.ModelResource):
        class Meta:
            model = models.EducationPlace

    list_display = ['id', 'specialization', 'faculty']


@admin.register(models.JobExperience)
class JobExperienceAdmin(ImportExportModelAdmin):
    class JobExperienceResource(resources.ModelResource):
        class Meta:
            model = models.JobExperience

    list_display = ['id', 'name', 'position']