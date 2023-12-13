from bulletin_board import models


def get_template_part_by_name(name):
    """Получить шаьлон по названию"""
    return models.TemplateParts.objects.filter(name=name).first()


def get_all_social_links():
    """Получить все социальные ссылки"""
    return models.SocialLink.objects.all()


def get_seo_metas(path):
    """Получить SEO Meta"""
    return models.SeoMeta.objects.filter(path=path).all()
