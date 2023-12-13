import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlite3 import IntegrityError

from decouple import config
import requests, json
from dadata import Dadata
from datetime import datetime
from core_base import models as cb_models, models
from core_base.models import IndividualTag

# from core_base.models import AdditionalSalaryCondition, Experience, \
#     EmploymentType, Location, WorkSchedule

# token = "0996f14ef4ffe73a0a9453fb7361d4d0a1e1c831"
# secret = "0051f05ba15e4e38355e337380ad706ff57eb9a3"

token = config('TOKEN')
secret = config('SECRET')


class SearchInfoBase:
    pass


class DaDataCompany(SearchInfoBase):
    source = 'DaData'

    def __init__(self, search_query):
        self.dadata = Dadata(token)
        self.search_query = search_query

        self.result_data = None

    def do_search(self):
        """Запустить процесс поиска"""
        self.result_data = self.dadata.find_by_id("party", self.search_query)

    @property
    def result(self):
        """Результать поиска"""

        # open('analiz.json', 'w', encoding='utf-8').write(
        #     json.dumps(self.result_data, ensure_ascii=False)
        # )
        return self.result_data

    @property
    def searching_company_info(self):
        """Инфо искомой компании"""

        if len(self.result_data) > 0:
            cmp_data: dict = self.result_data[0]['data']

            company_kpp = None
            company_inn = None
            company_ogrn = None

            company_status = None
            company_registration_date = None

            company_director_name = None
            company_director_post = None

            company_opf_full = None
            company_opf_short = None

            company_name_full = None
            company_name_full_with_opf = None

            company_name_short = None
            company_name_short_with_opf = None

            company_address = None

            company_kpp = cmp_data.get('kpp')
            company_inn = cmp_data.get('inn')
            company_ogrn = cmp_data.get('ogrn')

            if cmp_data.get('state'):
                company_status = cmp_data['state'].get('status')
                company_registration_date = cmp_data['state'].get('registration_date')

                print('company_registration_date: ', company_registration_date)

                if company_registration_date:
                    company_registration_date = datetime.fromtimestamp(company_registration_date / 1000)

            if cmp_data.get('management'):
                company_director_name = cmp_data['management'].get('name')
                company_director_post = cmp_data['management'].get('post')

            if cmp_data.get('opf'):
                company_opf_full = cmp_data['opf'].get('full')
                company_opf_short = cmp_data['opf'].get('short')

            if cmp_data.get('name'):
                company_name_short = cmp_data['name'].get('short')
                company_name_full = cmp_data['name'].get('full')

                company_name_full_with_opf = cmp_data['name'].get('full_with_opf')
                company_name_short_with_opf = cmp_data['name'].get('short_with_opf')

            if cmp_data.get('address'):
                company_address = cmp_data['address']['unrestricted_value']

            return {
                'inn': company_inn,
                'kpp': company_kpp,
                'ogrn': company_ogrn,

                'status': company_status,
                'registration_date': company_registration_date,

                'director_name': company_director_name,
                'director_post': company_director_post,

                'opf_full': company_opf_full,

                'name_full_with_opf': company_name_full_with_opf,
                'name_short_with_opf': company_name_short_with_opf,

                'address': company_address

            }


def get_app_info_from_post_request(request):
    """Получить информацию о антете из POST запроса"""

    inf = {
        'first_name': request.POST.get('first_name'),
        'second_name': request.POST.get('second_name'),
        'middle_name': request.POST.get('middle_name'),
        'name_app': request.POST.get('name_app'),
        'qualification': request.POST.get('qualification'),
        'date_of_birth': request.POST.get('date_of_birth'),
        'experience': cb_models.Experience.objects.get(id=request.POST.get('experience')),
        'employment_type': cb_models.EmploymentType.objects.get(id=request.POST.get('employment_type')),
        'work_schedule': cb_models.WorkSchedule.objects.get(id=request.POST.get('work_schedule')),
        'location': cb_models.Location.objects.get(id=request.POST.get('location')),
        'salary': request.POST.get('salary'),
        'salary_condition': cb_models.AdditionalSalaryCondition.objects.get(
            id=request.POST.get('salary_condition')),

        'about_app': request.POST.get('about_app'),
        'tel': request.POST.get('tel'),
        'tags': [],

    }

    for key, val in request.POST.items():
        if key.startswith('selected_tag_'):
            inf['tags'].append(val)

    inf['tags'] = cb_models.Tag.objects.filter(id__in=inf['tags']).all()

    return inf


def get_job_info_from_post_request(request):
    """Получить информацию о работе из POST запроса"""
    print("request.POST.get('ind_tag_data')", request.POST)
    inf = {
        'title': request.POST.get('title'),
        'qualification': request.POST.get('qualification'),
        'category': cb_models.JobCategory.objects.get(id=request.POST.get('category')),
        'experience': cb_models.Experience.objects.get(id=request.POST.get('experience')),
        'employment_type': cb_models.EmploymentType.objects.get(id=request.POST.get('employment_type')),
        'work_schedule': cb_models.WorkSchedule.objects.get(id=request.POST.get('work_schedule')),
        'location': cb_models.Location.objects.get(id=request.POST.get('location')),
        'salary': request.POST.get('salary'),
        'salary_condition': cb_models.AdditionalSalaryCondition.objects.get(
            id=request.POST.get('salary_condition')),
        'tags': [],
        'ind_tags': [],
        'old_selected_ind_tags': [],
        'about_job': request.POST.get('about_job'),
        'company_offers': request.POST.get('company_offers'),
        'requirements': request.POST.get('requirements'),

        'recruiter_name': request.POST.get('recruiter_name'),
        'recruiter_position': request.POST.get('recruiter_position'),
        'recruiter_phone': request.POST.get('recruiter_phone'),
        'recruiter_email': request.POST.get('recruiter_email'),
        'recruiter_communication_method': cb_models.CommunicationMethod.objects.get(
            id=request.POST.get('recruiter_communication_method')
        )
    }

    for key, val in request.POST.items():
        if key.startswith('selected_tag_'):
            inf['tags'].append(val)
        if key.startswith('selected_ind_tag_'):
            inf['old_selected_ind_tags'].append(val)

    inf['tags'] = cb_models.Tag.objects.filter(id__in=inf['tags']).all()

    inf['new_selected_ind_tags'] = []
    new_ind_tag_data = request.POST.get('new_ind_tag_data')

    if new_ind_tag_data:
        for tag in new_ind_tag_data.split(','):
            if not IndividualTag.objects.filter(title=tag).exists():
                IndividualTag.objects.create(title=tag)
                inf['new_selected_ind_tags'].append(str(IndividualTag.objects.get(title=tag).id))

            else:
                inf['new_selected_ind_tags'].append(str(IndividualTag.objects.get(title=tag).id))
                # print('Данный тег уже существует')

    inf['ind_tags'] = inf['old_selected_ind_tags'] + inf['new_selected_ind_tags']
    #
    # print("inf['old_selected_ind_tags']", inf['old_selected_ind_tags'])
    # print("inf['all_selected_ind_tags']", inf['new_selected_ind_tags'])
    # print("inf['ind_tags']", inf['ind_tags'])

    inf['ind_tags'] = IndividualTag.objects.filter(id__in=inf['ind_tags']).all()

    return inf


def dump_post_to_dict(post):
    di = {}
    for key, value in post.items():
        di[key] = value

    return di


def send_employer_notification(job_instance, name: str, phone: str, communication_method, job_email, location):
    """Отправить забытый пароль на почту"""
    # create message object instance
    try:
        msg = MIMEMultipart()

        message = f'Добрый день! У Вас новый отклик!\n' \
                  f'Вакансия: "{job_instance}", {location}\n' \
                  f'Откликнулся: {name}, тел. {phone}\n' \
                  f'Посмотреть список Ваших откликов можно в личном кабинете: https://myjobox.ru/industrial/candidates/\n' \
                  f'С уважением к Вам и Вашей работе!\n' \
                  f'Администрация Jobox.'

        password = "elV1qaAhm1RF"
        msg['From'] = 'mode@myjobox.ru'
        msg['To'] = job_email
        msg['Subject'] = "Отклик на вакансию"
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        # create server
        server = smtplib.SMTP('connect.smtp.bz: 2525')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("successfully sent email to %s:" % (msg['To']))
    except:
        print('Данные рекрутера не корректны')