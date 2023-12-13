from core_base import models
from django.db.models import Q, Count


def add_application_to_admin(name, email, text):
    """Добавит заявку администратору"""

    application_instance = models.ApplicationsToAdmin.objects.create(
        name=name,
        email=email,
        text=text
    )
    return application_instance


def get_tags_to_show_on_main_page():
    """Теги для показа на главной странице"""

    return models.Tag.objects.filter(show_on_main_page=True).all()


def get_categories_to_show_on_main_page():
    """Категории для показа на главной странице"""

    return models.JobCategory.objects.filter(show_on_main_page=True).annotate(
        jobs_count=Count('jobs', filter=Q(jobs__status='published'))
    )


def get_recomended_blogs():
    """Получить рекомендованные блоги"""

    return models.Blog.objects.filter(show_on_main_page=True).all()


def get_blogs_for_company_page():
    """Получить блог для страницы для работадателей"""

    return models.Blog.objects.filter(show_on_for_company_page=True).all()


def get_system_image(name):
    """Получить системную картинку"""
    image = models.SystemImages.objects.filter(name=name)
    # print('image', image)
    return image


# --- Подтвержденые почты -------------------------------------------------------------------------------------------

def refresh_email_confirmation_code(user: models.User):
    """Обносить код для подтвержденя почты"""

    user.email_confirm_code = models.generate_email_confirmation_code()
    user.save()


def confirm_user_email_by_code(user: models.User, code: str):
    """Подтвердить почту по коду"""
    print("con code: ", user.email_confirm_code)

    if code == user.email_confirm_code:
        user.is_email_confirmed = True
        user.save()

    return user.is_email_confirmed
