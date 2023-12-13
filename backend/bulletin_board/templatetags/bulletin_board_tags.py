from django import template
from bulletin_board import services as bb_services

register = template.Library()


@register.inclusion_tag('bulletin_board/components/template_part.html')
def for_company_template_part_1(*args, **kwargs):
    _template = bb_services.get_template_part_by_name(
        name='for_companies_template_part_1')
    return {'template_content': _template.content}


@register.inclusion_tag('bulletin_board/components/template_part.html')
def doc_1_body(*args, **kwargs):
    _template = bb_services.get_template_part_by_name(name='doc_1_body')
    return {'template_content': _template.content}


@register.inclusion_tag('bulletin_board/components/template_part.html')
def doc_2_body(*args, **kwargs):
    _template = bb_services.get_template_part_by_name(name='doc_2_body')
    return {'template_content': _template.content}


@register.inclusion_tag('bulletin_board/components/template_part.html')
def industrial_instruction(*args, **kwargs):
    _template = bb_services.get_template_part_by_name(
        name='industrial_instruction')
    return {'template_content': _template.content}


@register.inclusion_tag('bulletin_board/components/template_part.html')
def industrial_afferta(*args, **kwargs):
    _template = bb_services.get_template_part_by_name(
        name='industrial_afferta')
    return {'template_content': _template.content}


@register.inclusion_tag('bulletin_board/components/template_part.html')
def yandex_metric(*args, **kwargs):
    _template = bb_services.get_template_part_by_name(name='yandex_metric')
    return {'template_content': _template.content}


@register.inclusion_tag('bulletin_board/components/template_part.html')
def inside_head(*args, **kwargs):
    _template = bb_services.get_template_part_by_name(name='inside_head')
    return {'template_content': _template.content}


@register.inclusion_tag('bulletin_board/components/template_part.html')
def inside_body(*args, **kwargs):
    _template = bb_services.get_template_part_by_name(name='inside_body')
    return {'template_content': _template.content}


@register.inclusion_tag('bulletin_board/components/social_links_v1.html')
def social_links_v1(*args, **kwargs):
    _social_links = bb_services.get_all_social_links()
    return {'social_links': _social_links}


@register.inclusion_tag('bulletin_board/components/page_custom_metas.html')
def page_custom_metas(request, *args, **kwargs):
    metas = bb_services.get_seo_metas(request.path)
    title_ = None
    keywords_ = None
    description_ = None
    image_ = None

    for meta in metas:
        if meta.meta_type == "title":
            title_ = meta.content

        if meta.meta_type == "keywords":
            keywords_ = meta.content

        if meta.meta_type == "description":
            description_ = meta.content

        if meta.meta_type == "image":
            image_ = meta.image

    context = {
        "title": title_,
        "keywords": keywords_,
        "description": description_,
        "image": image_
    }
    return context
