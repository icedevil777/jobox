from django import template
from core_base import services as cb_services

register = template.Library()


@register.inclusion_tag('core/components/system_image_logo_big_url.html')
def system_image_logo_big_url(company=None, *args, **kwargs):
    return {
        'image_instance': cb_services.get_system_image('logo_big.svg'),
    }


@register.inclusion_tag('core/components/system_image_logo_big_style.html')
def system_image_logo_big_style(company=None, *args, **kwargs):
    return {
        'image_instance': cb_services.get_system_image('logo_big.svg'),
    }


@register.inclusion_tag('core/components/system_image_company_default_logo_url.html')
def system_image_company_default_logo_url(company=None, *args, **kwargs):
    return {
        'image_instance': cb_services.get_system_image('company_default_logo'),
    }
