from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from backend import settings
from backend.settings import DATE_INPUT_FORMATS
from industrial.models import Applicant
from .querysets.user import CustomUserManager

from uuid import uuid4

USER_TYPES = [
    ('IND', 'Industrial'),
    ('APPLICANT', 'Applicant'),
    ('ADMIN', 'Admin'),
]


def generate_email_confirmation_code():
    """Генерировать код для подтверждения почты"""
    n = 6  # Digits count
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    code = str(randint(range_start, range_end))
    return code


class User(AbstractUser):
    """Пользователь"""

    user_type = models.CharField(max_length=20, choices=USER_TYPES)

    email = models.EmailField(unique=True)

    is_email_confirmed = models.BooleanField(default=False)
    email_confirm_code = models.CharField(max_length=40,
                                          default=generate_email_confirmation_code)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class CustomModelBase(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class JobCategory(CustomModelBase):
    """Категория"""
    title = models.CharField(max_length=100)
    icon_code = models.CharField(max_length=100, blank=True, null=True)

    show_on_main_page = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категория"

    def __str__(self):
        return self.title


class Experience(CustomModelBase):
    """Опыт работы"""
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Опыт работы"
        verbose_name_plural = "Опыт работы"

    @property
    def name_for_form(self):
        return f'Experience_{self.id}'

    def __str__(self):
        return self.title


class EmploymentType(CustomModelBase):
    """Тип занятости"""
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Тип занятости"
        verbose_name_plural = "Тип занятости"

    @property
    def name_for_form(self):
        return f'EmploymentType_{self.id}'

    def __str__(self):
        return self.title


class WorkSchedule(CustomModelBase):
    """График работы"""
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = "График работы"
        verbose_name_plural = "График работы"

    def __str__(self):
        return self.title


class AdditionalSalaryCondition(CustomModelBase):
    """Доп. условие по зарплате"""
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Доп. условие по зарплате"
        verbose_name_plural = "Доп. условие по зарплате"

    def __str__(self):
        return self.title


class SalarySize(CustomModelBase):
    """Размер зарплаты"""
    max_salary = models.IntegerField(default=10000000)
    min_salary = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Мин и мах зарплата"
        verbose_name_plural = "Мин и мах зарплата"

    def __str__(self):
        return self.max_salary


class IndividualTag(models.Model):
    """Персональные теги вакансии"""
    title = models.CharField(max_length=30, unique=True)

    show_on_main_page = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Персональный тег"
        verbose_name_plural = "Персональные теги"

    def __str__(self):
        return self.title


class Tag(CustomModelBase):
    """Теги компании"""
    title = models.CharField(max_length=100)

    show_on_main_page = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Тег компании"
        verbose_name_plural = "Теги компании"

    def __str__(self):
        return self.title


class TagApp(CustomModelBase):
    """Теги соискателя"""
    title = models.CharField(max_length=100)

    show_on_main_page = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Тег соискателя"
        verbose_name_plural = "Теги соискателя"

    def __str__(self):
        return self.title


class CommunicationMethod(CustomModelBase):
    """Способ связи"""
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    icon_code = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name = "Cпособ связи"
        verbose_name_plural = "Cпособ связи"

    def __str__(self):
        return self.title


class Location(models.Model):
    """Локация"""

    region = models.CharField("Регион", max_length=50, db_index=True,
                              null=True, blank=True)
    region_type = models.CharField(max_length=10, db_index=True, null=True,
                                   blank=True)

    city = models.CharField("Город", max_length=150, db_index=True)

    foundation_year = models.IntegerField(null=True, blank=True)
    population = models.IntegerField(null=True, blank=True)
    geo_lon = models.FloatField(null=True, blank=True)
    geo_lat = models.FloatField(null=True, blank=True)
    timezone = models.CharField(max_length=10, null=True, blank=True)
    tax_office = models.CharField(max_length=10, null=True, blank=True)
    oktmo = models.CharField(max_length=20, null=True, blank=True)
    okato = models.CharField(max_length=20, null=True, blank=True)
    capital_marker = models.IntegerField(null=True, blank=True)
    fias_level = models.IntegerField(null=True, blank=True)
    fias_id = models.CharField(max_length=50, null=True, blank=True)
    kladr_id = models.BigIntegerField(null=True, blank=True)

    city_name = models.CharField(max_length=100, null=True, blank=True)
    city_type = models.CharField(max_length=10, null=True, blank=True)

    area = models.CharField(max_length=100, null=True, blank=True)
    area_type = models.CharField(max_length=10, null=True, blank=True)

    federal_district = models.CharField(max_length=100, null=True, blank=True)

    country = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    address = models.CharField("Город", max_length=150, db_index=True,
                               null=True, blank=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.city


class BlogCategory(models.Model):
    """Категория блога"""
    title = models.CharField(max_length=150)

    class Meta:
        verbose_name = "БЛОГ Категория"
        verbose_name_plural = "БЛОГ Категории"

    def __str__(self):
        return self.title


class BlogAuthor(models.Model):
    """Автор блога """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_ad = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = "БЛОГ Автор"
        verbose_name_plural = "БЛОГ Автор"

    def __str__(self):
        return self.name


class Blog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_ad = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(BlogAuthor, on_delete=models.PROTECT,
                               related_name='blogs', null=True)

    title = models.CharField(max_length=250)
    category = models.ForeignKey(BlogCategory, on_delete=models.PROTECT,
                                 related_name='blogs')
    subtitle = models.CharField(max_length=500)

    main_image = models.ImageField(upload_to="blog/images")
    body = models.TextField()

    show_on_main_page = models.BooleanField(
        verbose_name="на главной странице",
        default=False
    )

    show_on_for_company_page = models.BooleanField(
        verbose_name="на страницу для работодателей",
        default=False
    )
    show_sing_in_on_company_page = models.BooleanField(
        verbose_name="Кнопка 'вход в личный кабинет'",
        default=False
    )

    show_on_news_page = models.BooleanField(
        verbose_name="на странице новостей",
        default=False
    )

    class Meta:
        verbose_name = "БЛОГ Пост"
        verbose_name_plural = "БЛОГ Посты"

    def __str__(self):
        return self.title


class ApplicationsToAdmin(models.Model):
    """Зоявки администратору"""

    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    text = models.TextField(max_length=2048)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки Администратору"

    def __str__(self):
        return self.name


class SystemImages(models.Model):
    """Системные картинки"""
    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=150, unique=True)
    file = models.FileField(upload_to='system_images')

    width = models.CharField(max_length=50, null=True, blank=True)
    height = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class JobExperience(models.Model):
    """ Места работы """

    name = models.CharField(max_length=150)
    have_experience = models.BooleanField(default=False)
    position = models.CharField(max_length=150)
    function = models.CharField(max_length=300)
    start_data = models.DateField()
    end_data = models.DateField()
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE,
                                  null=True,
                                  related_name='exp_app')

    class Meta:
        verbose_name = "Место работы"
        verbose_name_plural = "Места работы"

    def __str__(self):
        return f'{self.name} {self.position} {self.function}'


class EducationLevel(models.Model):
    """ Уровень образования """
    title = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Уровень образования"
        verbose_name_plural = "Уровень образования"

    def __str__(self):
        return self.title


class EducationPlace(models.Model):
    """Места учебы"""
    name = models.CharField(max_length=150)
    faculty = models.CharField(max_length=150)
    specialization = models.CharField(max_length=150)
    start_data = models.DateField()
    end_data = models.DateField()
    level = models.ForeignKey(EducationLevel, on_delete=models.PROTECT,
                              null=True, related_name='edu_app')

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE,
                                  null=True, related_name='edu_app')

    class Meta:
        verbose_name = "Место учебы"
        verbose_name_plural = "Места учебы"

    def __str__(self):
        return f'{self.name} {self.faculty} {self.specialization} {self.level}'
