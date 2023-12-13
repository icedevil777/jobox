from django.contrib import admin
from bulletin_board import models
from import_export.admin import ImportExportModelAdmin
from import_export import resources


@admin.register(models.TemplateParts)
class TemplatePartsAdmin(ImportExportModelAdmin):
    class TemplatePartsResource(resources.ModelResource):
        class Meta:
            model = models.TemplateParts

    list_display = ['title']


@admin.register(models.SocialLink)
class SocialLinkAdmin(ImportExportModelAdmin):
    class SocialLinkResource(resources.ModelResource):
        class Meta:
            model = models.SocialLink

    list_display = ['name', 'url', 'icon_code']


@admin.register(models.IndexFile)
class TemplatePartsAdmin(ImportExportModelAdmin):
    class TemplatePartsResource(resources.ModelResource):
        class Meta:
            model = models.IndexFile

    list_display = ['name']


@admin.register(models.SeoMeta)
class SeoMetaAdmin(ImportExportModelAdmin):
    class SeoMetaResource(resources.ModelResource):
        class Meta:
            model = models.SeoMeta

    list_display = ['path', 'meta_type']
    ordering = ["path", "meta_type"]
