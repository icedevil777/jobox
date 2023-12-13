import logging
import re

from django.template.defaultfilters import lower, upper

from core_base.logger import get_logger
from core_base.models import User, EducationPlace, EducationLevel, \
    JobExperience, IndividualTag
from . import models
from django.db import transaction

from django.db.models import Q, Count, Sum
#

from core_base import models as cb_models

from typing import List
from django.conf import settings

from .models import Applicant, Company, Job

logger = get_logger('indast_serv_logs', level=logging.INFO)


def add_new_company(
        name, opf_full, director_name, director_post, registration_date,
        address, inn, ogrn, kpp, user, dadata_date=None) -> models.Company:
    """Добавить новую компанию """

    company_instance = models.Company.objects.create(
        name=name,
        opf_full=opf_full,
        director_name=director_name,
        director_post=director_post,
        registration_date=registration_date,
        address=address,
        inn=inn,
        ogrn=ogrn,
        kpp=kpp,
        user=user,
        dadata_date=dadata_date
    )

    return company_instance


def get_company_by_ref_code(ref_code):
    """Получить компанию по """
    instance = models.Company.objects.filter(ref_code=ref_code).first()
    return instance


def add_new_company_worker(company_instance: models.Company, email,
                           password, user) -> models.CompanyWorker:
    """Создать нового работника для компании"""

    # new_system_user = User.objects.create_user(
    #     username=email,
    #     email=email,
    #     password=password
    # )
    #
    # # Тип пользователя Industrial
    # new_system_user.user_type = 'INT'
    # new_system_user.save()

    company_worker = models.CompanyWorker.objects.create(
        company=company_instance,
        user=user
    )
    return company_worker


def password_reset(email, password):
    """Сброс пароля"""

    user = User.objects.get(email=email)
    user.set_password(password)
    user.save()


def check_none_in_data(company_info):
    """
    Функция проверяет что бы из базы не пришел None
    """
    for i in company_info:
        if company_info[i] is None:
            company_info[i] = 'None'
    return company_info


@transaction.atomic
def register_new_industrial(email, password, inn, company_info,
                            dadata_date=None):
    """Регистрации новой компании"""

    if company_info['inn'] != inn:
        raise Exception("Разные ИНН")

    new_system_user = User.objects.create_user(
        username=email,
        email=email,
        password=password
    )
    # Тип пользователя Industrial
    new_system_user.user_type = 'INT'
    new_system_user.save()
    company_info = check_none_in_data(company_info)

    if company_info['name_short_with_opf'] is None or \
            company_info['name_short_with_opf'] == 'None':
        company_name = company_info['name_full_with_opf']
    else:
        company_name = company_info['name_short_with_opf']

    new_company = add_new_company(
        name=company_name,
        opf_full=company_info['opf_full'],
        director_name=company_info['director_name'],
        director_post=company_info['director_post'],
        registration_date=company_info['registration_date'],
        address=company_info['address'],
        inn=company_info['inn'],
        ogrn=company_info['ogrn'],
        kpp=company_info['kpp'],
        user=new_system_user,
        dadata_date=dadata_date  # Сырая версия данных о компании с DaData
    )

    new_company_worker = add_new_company_worker(new_company, email,
                                                password, new_system_user)

    return {'company': new_company, 'worker': new_company_worker}


@transaction.atomic
def register_new_applicant(email, password, tel):
    """Регистрация нового пользователя"""

    new_system_user = User.objects.create_user(
        username=email,
        email=email,
        password=password
    )
    new_system_user.user_type = 'APPLICANT'
    new_system_user.save()

    new_applicate = models.Applicant.objects.create(
        user=new_system_user,
        tel=tel,
        user_email=email
    )

    return new_system_user


def find_user_in_base(email):
    return User.objects.filter(email=email).exists()


def search_company_in_base(inn):
    return Company.objects.filter(inn=inn).exists()


def add_or_update_job(company, job_data):
    """Добавить или обновить работу новую работу"""

    _is_new_job = False

    job_instance: models.Job = job_data.get('job_instance')

    if job_instance is None:  # Если нужно добавить новую работу
        job_instance = models.Job(company=company)
        _is_new_job = True

    job_instance.title = lower(job_data.get('title')).capitalize()
    job_instance.qualification = lower(job_data.get('qualification'))
    job_instance.category = job_data.get('category')
    job_instance.experience = job_data.get('experience')
    job_instance.employment_type = job_data.get('employment_type')
    job_instance.work_schedule = job_data.get('work_schedule')
    job_instance.location = job_data.get('location')
    job_instance.salary = job_data.get('salary')
    job_instance.salary_condition = job_data.get('salary_condition')

    job_instance.about_job = job_data.get('about_job')
    job_instance.company_offers = job_data.get('company_offers')
    job_instance.requirements = job_data.get('requirements')

    job_instance.recruiter_name = lower(job_data.get('recruiter_name')).capitalize()
    job_instance.recruiter_position = lower(job_data.get('recruiter_position')).capitalize()
    job_instance.recruiter_phone = job_data.get('recruiter_phone')
    job_instance.recruiter_communication_method = job_data.get(
        'recruiter_communication_method')
    job_instance.recruiter_email = job_data.get('recruiter_email')
    job_instance.save()

    job_instance.tags.set(job_data['tags'])
    job_instance.ind_tags.set(job_data['ind_tags'])

    for q in job_data['ind_tags']:
        job_instance.all_ind_tags.add(q)

    return job_instance


def delete_ind_tags(job_id):
    inst = Job.objects.get(id=job_id)
    inst.ind_tags.clear()
    inst.all_ind_tags.clear()


def delete_experience(request):
    app_inst = Applicant.objects.get(user_email=request.user.email)
    JobExperience.objects.filter(applicant=app_inst).first().delete()


def delete_education(request):
    app_inst = Applicant.objects.get(user_email=request.user.email)
    EducationPlace.objects.filter(applicant=app_inst).first().delete()


def add_education(request):
    app_inst = Applicant.objects.get(user_email=request.user.email)
    education = EducationPlace.objects.create(
        name=request.POST['name'],
        faculty=request.POST['faculty'],
        specialization=request.POST['specialization'],
        start_data=request.POST['start_data'],
        end_data=request.POST['end_data'],
        level=EducationLevel.objects.get(id=request.POST['level']),
        applicant=app_inst,
    )
    app_inst.have_tabel = True
    app_inst.have_education = True
    app_inst.save()
    return education


def add_experience(request):
    app_inst = Applicant.objects.get(user_email=request.user.email)
    experience = JobExperience.objects.create(
        name=request.POST['name'],
        position=request.POST['position'],
        function=request.POST['function'],
        start_data=request.POST['start_data'],
        end_data=request.POST['end_data'],
        applicant=app_inst,
    )
    app_inst.have_tabel = True
    app_inst.have_experience = True
    app_inst.save()
    return experience


def add_or_update_app(request):
    """Добавить или обновить работу новую анкету"""

    email = request.user.email
    app_inst = Applicant.objects.get(user_email=email)

    # print(request.POST)

    app_inst.first_name = lower(request.POST['first_name']).capitalize()
    app_inst.second_name = lower(request.POST['second_name']).capitalize()
    app_inst.middle_name = lower(request.POST['middle_name']).capitalize()
    app_inst.name_app = lower(request.POST['name_app']).capitalize()
    app_inst.qualification = lower(request.POST['qualification'])
    app_inst.date_of_birth = request.POST['date_of_birth']
    app_inst.about_app = request.POST['about_app']

    # app_inst.about_experience = request.POST['about_experience']
    # app_inst.about_education = request.POST['about_education']

    app_inst.salary = request.POST['salary']

    app_inst.tel = request.POST['tel']
    app_inst.experience_id = request.POST['experience']
    app_inst.employment_type_id = request.POST['employment_type']
    app_inst.work_schedule_id = request.POST['work_schedule']
    app_inst.location_id = request.POST['location']
    app_inst.salary_condition_id = request.POST['salary_condition']

    inf = {
        'tags_app': []
    }
    for key, val in request.POST.items():
        if key.startswith('selected_tag_'):
            inf['tags_app'].append(val)

    inf['tags_app'] = cb_models.TagApp.objects.filter(
        id__in=inf['tags_app']).all()

    app_inst.have_resume = True
    app_inst.status = 'published'

    text = app_inst.about_app.strip()
    text = re.sub(r'^\s+|\n|\r|\s+$', r'<br>', text)
    # text = re.sub(r' <br><br>', r'<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', text)
    text = re.sub(r'<br><br>', r'<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', text)
    text = f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{text}"
    app_inst.about_app = text

    app_inst.save()
    app_inst.tags_app.set(inf['tags_app'])

    return app_inst


def do_tab(about_app):
    """Функция убирает лишние символы из поля <textarea>"""
    about_app = re.sub(r'<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', r'\n', about_app)
    about_app = re.sub(r'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', r'\n', about_app)
    return about_app


def get_company_all_jobs(company: models.Company):
    """Получить все вакансии компании"""

    return models.Job.objects.filter(company=company).all()


def get_job_by_id(job_id):
    return models.Job.objects.get(id=job_id)


def del_job_by_id(job_id):
    return models.Job.objects.get(id=job_id).delete()


def del_response_by_id(resp_id):
    return models.ResponseToJob.objects.get(id=resp_id).delete()


def get_company_job_by_id(company, job_id):
    return models.Job.objects.get_selected_all_info_selected().get(
        company=company, id=job_id)


def get_applicant_by_id(email, app_id):
    return models.Applicant.objects.get_selected_all_info_selected().get(
        user_email=email, id=app_id)


def add_response_to_job(job: models.Job, name: str, phone: str,
                        communication_method):
    """Добавить отклик на работу"""

    response_instance = models.ResponseToJob.objects.create(
        job=job,
        name=name,
        phone=phone,
        communication_method=communication_method
    )
    return response_instance


def get_company_jobs_count(company: models.Company):
    """Кол-во вакансий у компании"""
    return models.Job.objects.filter(company=company).count()


def get_company_short_statistic_info(company: models.Company):
    """Информация об количестве работ в компании"""

    return models.Company.objects.filter(id=company.id).aggregate(
        published_jobs=Count('jobs', distinct=True, filter=Q(jobs__status='published')),
        moderation_jobs=Count('jobs', distinct=True, filter=Q(jobs__status='moderation')),
        job_responses_count=Count('jobs__responses__id', distinct=True),
        notifications_count=Count('notifications__id', distinct=True),
    )


def total_published_jobs_count():
    """Количество всех публикованных работ"""

    return models.Job.objects.filter(status='published',
                                     show_on_main_page=True).count()


def total_companies_count():
    """Количество всех компаний"""

    return models.Company.objects.count()


def get_recomended_companies():
    """Получить рекомендованные компании"""

    return models.Company.objects.filter(show_on_main_page=True).annotate(
        published_jobs=Count('jobs', filter=Q(jobs__status='published')),
    ).all()


def get_recomended_jobs():
    """Получить рекомендованные ваканции"""

    return models.Job.objects.get_selected_all_info_selected().filter(
        show_on_main_page=True, status='published').all()


# --- Транзакции компании ---------------------------------------------------

def get_company_transactions(company: models.Company, currency: str = None) -> \
        List[models.CompanyFinanceTransaction]:
    """Получить транзакции компании"""

    query = models.CompanyFinanceTransaction.objects
    query = query.filter(company=company)

    if currency:
        query = query.filter(currency=currency)

    query = query.order_by('-created_at')
    query = query.all()
    return query


def get_company_transaction_totals(company: models.Company):
    """Получить ИТОГИ счетов компании"""

    query = models.CompanyFinanceTransaction.objects.filter(
        company=company).aggregate(
        bonus_point_total=Sum('amount', filter=Q(
            currency=models.CompanyFinanceTransaction.CURRENCIES.bonus_point)),
        ruble_total=Sum('amount', filter=Q(
            currency=models.CompanyFinanceTransaction.CURRENCIES.ruble)),
    )

    return query


def create_new_company_finance_transaction(company, currency, action, amount,
                                           comment, technical_comment,
                                           payment_for_job=None,
                                           payment_invoice=None):
    """Создать финансовую транзакцию компании"""

    new_instance = models.CompanyFinanceTransaction.objects.create(
        company=company,
        currency=currency,
        action=action,
        amount=amount,
        comment=comment,
        technical_comment=technical_comment,
        payment_for_job=payment_for_job,
        payment_invoice=payment_invoice
    )
    logger.info(f'new_instance {new_instance}')
    return new_instance


@transaction.atomic
def create_company_transaction_for_job_payment(currency, job: models.Job):
    totals = get_company_transaction_totals(job.company)
    price = settings.JOB_PAYMENT_PRICES[currency]
    print('totals: ', totals)
    print('price', price)
    try:
        if totals[f'{currency}_total'] >= price:
            print('currency', currency)

            new_transaction = create_new_company_finance_transaction(
                company=job.company,
                currency=currency,
                action=models.CompanyFinanceTransaction.ACTIONS.publication,
                amount=price * -1,
                comment='За публикацию!',
                technical_comment='For vacancy publication!',
                payment_for_job=job
            )
            after_totals = get_company_transaction_totals(job.company)
            print('after_totals: ', after_totals)
            if after_totals[f'{currency}_total'] >= 0:
                job.is_paid = True
                job.save()
            else:
                raise Exception("Not enough MONEY!")
    except:
        pass


# --- Реферальная система -----------------------------------

def add_new_referral_chain(affiliate: models.Company, referral: models.Company,
                           code: str):
    """Добавить реферала"""
    instance, created = models.CompanyReferralChain.objects.get_or_create(
        referral=referral,
        defaults={
            'affiliate_id': affiliate.id,
            'ref_code': code
        }
    )
    if created:
        bonus_transaction = create_new_company_finance_transaction(
            company=affiliate,
            currency=models.CompanyFinanceTransaction.CURRENCIES.bonus_point,
            action=models.CompanyFinanceTransaction.ACTIONS.bonus_debiting,
            amount=1,
            comment='Бонус за привлечение новых пользователей',
            technical_comment='Bonus for new user by referral link!'
        )
        instance.bonus_transaction = bonus_transaction
        instance.save()
