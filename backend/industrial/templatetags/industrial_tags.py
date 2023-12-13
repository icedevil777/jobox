from django import template
from industrial import services as in_services
from core_base import services as cb_services
from uuid import uuid4

register = template.Library()


@register.simple_tag
def total_published_jobs_count(*args, **kwargs):
    return in_services.total_published_jobs_count()


@register.simple_tag
def total_companies_count(*args, **kwargs):
    return in_services.total_companies_count()


@register.inclusion_tag('bulletin_board/components/recomended_companies.html')
def recomended_companies_list(*args, **kwargs):
    _companies = in_services.get_recomended_companies()
    return {'companies': _companies}


@register.inclusion_tag('bulletin_board/components/recomended_blogs.html')
def recomended_blogs_list(*args, **kwargs):
    _blogs = cb_services.get_recomended_blogs()
    return {'recomended_blogs': _blogs}


@register.inclusion_tag('bulletin_board/components/recomended_jobs.html')
def recomended_jobs_list(*args, **kwargs):
    _jobs = in_services.get_recomended_jobs()
    return {'recomended_jobs': _jobs}


@register.inclusion_tag('industrial/components/new_invoice_button.html')
def new_invoice_button(company=None, *args, **kwargs):
    uniq_id = str(uuid4()).replace('-', '_')

    return {
        'company': company,
        'component_name': f'new_invoice_{uniq_id}'
    }


# @register.inclusion_tag('bulletin_board/components/app_table.html')
# def app_table(*args, **kwargs):
#     _jobs = in_services.get_recomended_jobs()
#     return {'recomended_jobs': _jobs}