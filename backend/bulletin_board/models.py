from django.db import models


class TemplateParts(models.Model):
    """Части шаблонов """

    name = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    content = models.TextField(max_length=50000)

    class Meta:
        verbose_name = "Части шаблонов"
        verbose_name_plural = "Часть шаблона"


class SocialLink(models.Model):
    """Социальные ссылки """

    name = models.CharField(max_length=150)
    url = models.CharField(max_length=150)
    icon_code = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Social links"
        verbose_name_plural = "Social links"


class IndexFile(models.Model):
    name = models.CharField(max_length=150)
    content = models.TextField(max_length=50000)


class SeoMeta(models.Model):
    meta_type = models.CharField(
        max_length=20,
        choices=(
            ("title", "title"),
            ("description", "description"),
            ("keywords", "keywords"),
            ("image", "image")
        )
    )
    path = models.CharField(max_length=150)
    content = models.TextField(max_length=50000)
    image = models.FileField(upload_to='meta_images', null=True, blank=True)
