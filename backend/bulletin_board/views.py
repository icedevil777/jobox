from django.shortcuts import render, HttpResponse, HttpResponseRedirect, \
    redirect
from django.urls import reverse
from django.views import View
from django.http.response import JsonResponse

from core_base import models as cb_models
from core_base.models import Tag, TagApp, EducationPlace, JobExperience
from industrial import models as in_models
from industrial import services as in_services
from core_base import services as cb_services
from industrial.services import delete_education, delete_experience
from industrial.utils import send_employer_notification

from bulletin_board.models import IndexFile

from django.db.models import Q, Count
from . import utils

import json

from .utils import translate


# Create your views here.
class IndexView(View):
    def get(self, request):
        context = {
            "locations": cb_models.Location.objects.all(),
            'recomended_jobs': in_models.Job.objects.filter(
                show_on_main_page=True, status='published').all(),
            "recomended_companies": in_models.Company.objects.filter(
                show_on_main_page=True).all(),
            "recomended_blogs": cb_models.Blog.objects.filter(
                show_on_main_page=True).all(),
            "tags_to_show_on_main_page": cb_services.get_tags_to_show_on_main_page(),
            "categories_to_show_on_main_page": cb_services.get_categories_to_show_on_main_page()

        }

        return render(request, 'bulletin_board/pages/index.html', {**context})


class ForCompany(View):
    def get(self, request):
        _slider_blogs = cb_services.get_blogs_for_company_page()
        return render(
            request,
            'bulletin_board/pages/for_company.html',
            {
                'slider_blogs': _slider_blogs
            }
        )


class BlogList(View):
    def get(self, request):
        blogs_list = cb_models.Blog.objects.select_related('author',
                                                           'category').filter(
            show_on_news_page=True)
        return render(
            request,
            'bulletin_board/pages/blog_list.html',
            {
                "blogs_list": blogs_list,
                "blogs_count": len(blogs_list)
            }
        )


class BlogView(View):
    def get(self, request, blog_id):
        try:
            blog_instance = cb_models.Blog.objects.get(id=blog_id)
            return render(
                request,
                'bulletin_board/pages/blog_view.html',
                {
                    'blog_instance': blog_instance
                }
            )
        except:
            return redirect('bulletin_board:blog_list')


class CompaniesList(View):
    def get(self, request):

        rq = {
            'name': request.GET.get('name') or '',
            'page': request.GET.get('page')
        }

        _companies_list = in_models.Company.objects.filter(show_on_main_page=True).all()

        if rq['name']:
            _companies_list = _companies_list.filter(name__icontains=rq['name'])
            if str(_companies_list) == '<QuerySet []>':
                _companies_list = in_models.Company.objects.filter(show_on_main_page=True).all()
                _companies_list = _companies_list.filter(name__icontains=translate(rq['name']))

        if not rq['page']:
            rq['page'] = 1
        else:
            rq['page'] = int(rq['page'])

        rq['pagination_range'] = range(rq['page'] - 4, rq['page'] + 4)
        _per_page = 2
        companies_list = _companies_list.annotate(
            jobs_count=Count('jobs', filter=Q(jobs__status='published'))
        ).all()[0:12]
        # ).all()[(rq['page'] - 1) * _per_page:rq['page'] * _per_page]

        companies_count = 0
        for company in companies_list:
            if company.jobs_count != 0:
                companies_count = companies_count + 1

        return render(
            request,
            'bulletin_board/pages/companies_list.html',
            {
                'companies_list': companies_list,
                'companies_count': companies_count,
                'rq': rq
            }
        )


class CompanyView(View):

    def get(self, request, company_id):
        try:
            company_instance = in_models.Company.objects.get(id=company_id)
            company_jobs = company_instance.jobs.filter(
                status='published').all()

            return render(
                request,
                'bulletin_board/pages/company_single_view.html',

                context={
                    'company_instance': company_instance,
                    'company_job': company_jobs,
                    'company_jobs_count': len(company_jobs)
                }
            )
        except:
            return redirect('bulletin_board:companies_list')


class SummaryCatalog(View):

    def get(self, request):

        context = {
            "categories": cb_models.JobCategory.objects.all(),  # .all(),
            "experiences": cb_models.Experience.objects.all(),
            "employment_types": cb_models.EmploymentType.objects.all(),
            "work_schedules": cb_models.WorkSchedule.objects.all(),
            "locations": cb_models.Location.objects.all(),
            "salary_conditions": cb_models.AdditionalSalaryCondition.objects.all(),
            "tags": cb_models.Tag.objects.all(),
            "communication_methods": cb_models.CommunicationMethod.objects.all(),
        }
        # jobs = in_models.Job.objects.get_selected_all_info_selected().filter(status="published")
        summaries = in_models.Applicant.objects.filter(status="published", show_on_main_page=True)

        fs = {
            **request.GET,
            'title': request.GET.get('title'),
            'category': request.GET.get('category'),
            'location': request.GET.get('location'),
            'tag': request.GET.get('tag'),
            'sort_by': request.GET.get('sort_by'),
            'page': request.GET.get('page'),
        }

        if not fs.get('page'):
            fs['page'] = 1
        else:
            fs['page'] = int(fs['page'])

        fs['pagination_range'] = range(fs['page'] - 4, fs['page'] + 4)

        if fs['title']:
            summaries = summaries.filter(name_app__icontains=fs['title'])
            if str(summaries) == '<QuerySet []>':
                summaries = in_models.Applicant.objects.filter(status="published", show_on_main_page=True)
                summaries = summaries.filter(name_app__icontains=translate(fs['title']))

        if fs['category']:
            summaries = summaries.filter(category_id=fs['category'])

        if fs['location']:
            summaries = summaries.filter(location_id=fs['location'])

        if fs['tag']:
            # in_models.Job.objects.
            summaries = summaries.filter(tags__id=fs['tag'])

        if fs['sort_by']:
            if fs['sort_by'] == 'first_new':
                summaries = summaries.order_by('-created_at')
            if fs['sort_by'] == 'first_old':
                summaries = summaries.order_by('created_at')
            if fs['sort_by'] == 'salary':
                summaries = summaries.order_by('-salary')

        # Тип занятности
        employment_types_list = utils.dict_key_parser(request.GET,
                                                      start_text='EmploymentType_')
        if len(employment_types_list) > 0:
            print('employment_types_list', employment_types_list)
            summaries = summaries.filter(employment_type_id__in=employment_types_list)

        # Опыть работы
        experience_list = utils.dict_key_parser(request.GET,
                                                start_text='Experience_')
        if len(experience_list) > 0:
            # print('experience_list', experience_list)
            summaries = summaries.filter(experience_id__in=experience_list)

        _items_per_page = 10
        summaries_count = summaries.count()
        sum_list = summaries.all()[
                   (fs['page'] - 1) * _items_per_page:fs['page'] * _items_per_page]

        context = {'fs': fs, 'summaries_count': summaries_count, 'summaries': sum_list, **context}

        return render(request, 'bulletin_board/pages/summary_catalog.html', context)


class JobsCatalog(View):

    def get(self, request):

        context = {
            "categories": cb_models.JobCategory.objects.all(),  # .all(),
            "experiences": cb_models.Experience.objects.all(),
            "employment_types": cb_models.EmploymentType.objects.all(),
            "work_schedules": cb_models.WorkSchedule.objects.all(),
            "locations": cb_models.Location.objects.all(),
            "salary_conditions": cb_models.AdditionalSalaryCondition.objects.all(),
            "tags": cb_models.Tag.objects.all(),
            "communication_methods": cb_models.CommunicationMethod.objects.all(),
        }

        jobs = in_models.Job.objects.get_selected_all_info_selected().filter(
            status="published")

        fs = {
            **request.GET,
            'title': request.GET.get('title'),
            'category': request.GET.get('category'),
            'location': request.GET.get('location'),
            'tag': request.GET.get('tag'),
            'sort_by': request.GET.get('sort_by'),
            'page': request.GET.get('page'),
        }

        if not fs.get('page'):
            fs['page'] = 1
        else:
            fs['page'] = int(fs['page'])

        fs['pagination_range'] = range(fs['page'] - 4, fs['page'] + 4)

        if fs['title']:
            jobs = jobs.filter(title__icontains=fs['title'])
            if str(jobs) == '<QuerySet []>':
                jobs = in_models.Job.objects.filter(status="published", show_on_main_page=True)
                jobs = jobs.filter(title__icontains=translate(fs['title']))

        # if fs['title']:
        #     summaries = summaries.filter(name_app__icontains=fs['title'])
        #     if str(summaries) == '<QuerySet []>':
        #         summaries = in_models.Applicant.objects.filter(status="published", show_on_main_page=True)
        #         summaries = summaries.filter(name_app__icontains=translate(fs['title']))

        if fs['category']:
            jobs = jobs.filter(category_id=fs['category'])

        if fs['location']:
            jobs = jobs.filter(location_id=fs['location'])

        if fs['tag']:
            # in_models.Job.objects.
            jobs = jobs.filter(tags__id=fs['tag'])

        if fs['sort_by']:
            if fs['sort_by'] == 'first_new':
                jobs = jobs.order_by('-published_at')

            if fs['sort_by'] == 'first_old':
                jobs = jobs.order_by('published_at')

            if fs['sort_by'] == 'salary':
                jobs = jobs.order_by('-salary')

        # Тип занятности
        employment_types_list = utils.dict_key_parser(request.GET,
                                                      start_text='EmploymentType_')
        if len(employment_types_list) > 0:
            jobs = jobs.filter(employment_type_id__in=employment_types_list)

        # Опыть работы
        experience_list = utils.dict_key_parser(request.GET,
                                                start_text='Experience_')
        if len(experience_list) > 0:
            jobs = jobs.filter(experience_id__in=experience_list)

        # print(jobs.all().query)

        _items_per_page = 10
        jobs_count = jobs.count()
        jobs_list = jobs.all()[
                    (fs['page'] - 1) * _items_per_page:fs['page'] * _items_per_page]

        return render(
            request,
            'bulletin_board/pages/jobs_catalog.html',
            context={
                'jobs': jobs_list,
                'jobs_count': jobs_count,
                'fs': fs,
                **context
            }
        )


class SummaryView(View):

    def get(self, request, sum_id):
        """Резюме"""
        # try:
        app_inst = in_models.Applicant.objects.get(id=sum_id)
        teg_inst = TagApp.objects.filter(tags_app=app_inst.id)
        education_inst = EducationPlace.objects.filter(
            applicant_id=app_inst.id)
        experience_inst = JobExperience.objects.filter(
            applicant_id=app_inst.id)
        content = {'app_inst': app_inst, 'teg_inst': teg_inst,
                   'education_inst': education_inst, 'experience_inst': experience_inst,
                   'data': str(app_inst.date_of_birth)}

        return render(
            request,
            'bulletin_board/pages/sum_single.html', {'content': content})
        # except:
        #     return redirect('bulletin_board:sum_catalog')


class JobView(View):
    def get(self, request, job_id):
        try:
            """вакансия"""
            job_instance = in_models.Job.objects.get_selected_all_info_selected().get(
                id=job_id)
            """предпочтительный метод связи"""
            communication_methods = cb_models.CommunicationMethod.objects.all()
            print(job_instance)
            print('______________________')
            print(communication_methods)
            return render(
                request,
                'bulletin_board/pages/job_single.html',
                {
                    'communication_methods': communication_methods,
                    'job_instance': job_instance
                }
            )
        except:
            return redirect('bulletin_board:jobs_catalog')
            # return HttpResponseRedirect(reverse('bulletin_board:jobs_catalog'))


class ApplyJob(View):
    """
    Класс принимает данные из формы после отклика работника на вакансию
    сохраняет данные в БД, а так же вызывает функцию уведомления работодателя.
    """

    def post(self, request, job_id):
        job_instance = in_models.Job.objects.get(id=job_id)
        js = json.loads(request.body)
        job_email = in_models.Job.objects.get(id=job_id).recruiter_email
        location = in_models.Job.objects.get(id=job_id).location
        communication_method = cb_models.CommunicationMethod.objects.get(id=1)

        response_instance = in_services.add_response_to_job(
            job=job_instance,
            name=js['name'],
            phone=js['phone'],
            communication_method=communication_method
        )

        send_employer_notification(job_instance, js['name'], js['phone'],
                                   communication_method, job_email, location)

        return JsonResponse({'id': response_instance.id}, safe=False)


class ApplicationToAdmin(View):
    def post(self, request):
        _name = request.POST.get('name')
        _email = request.POST.get('email')
        _text = request.POST.get('text')

        cb_services.add_application_to_admin(
            _name, _email, _text
        )

        return redirect('bulletin_board:index')


class Doc1(View):
    def get(self, request):
        return render(request, 'bulletin_board/pages/doc_1.html', {})


class Doc2(View):
    def get(self, request):
        return render(request, 'bulletin_board/pages/doc_2.html', {})


class DeleteSummaryEducation(View):

    def post(self, request):
        delete_education(request)
        return HttpResponseRedirect(reverse('industrial:edit_summary'))


class DeleteSummaryExperience(View):
    def post(self, request):
        delete_experience(request)
        return HttpResponseRedirect(reverse('industrial:edit_summary'))


def get_robots_txt(request):
    return HttpResponse(str(IndexFile.objects.filter(name="robots.txt").first().content), content_type='text/plain')


def get_sitemap_xml(request):
    return HttpResponse(str(IndexFile.objects.filter(name="sitemap.xml").first().content), content_type='text/plain')
