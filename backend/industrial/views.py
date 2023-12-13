import json
import logging
import re
import secrets
from django.template.defaultfilters import lower
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, reverse, redirect
from django.template.defaultfilters import lower
from django.views import View
from django.http.response import HttpResponse, HttpResponseRedirect, \
    JsonResponse
from django.db.models import Count, Q

from backend.settings import env
from core_base import utils as core_utils
from core_base import services as cb_services
from core_base.logger import get_logger
from core_base.models import Tag, TagApp, EducationPlace, JobExperience
from . import forms
from . import utils
from . import services
from . import mixins
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout

from core_base import models as cb_models
from industrial import models as in_models

from payment.selectors import get_company_payment_invoices, get_invoice_by_id
from payment import services as py_services

from django.conf import settings

from .models import Applicant, CompanyReferralChain, Company
# --- Функции для администратора ---------------
from .redis import r
from .services import password_reset, get_job_by_id, del_job_by_id, \
    del_response_by_id, find_user_in_base, add_or_update_app, \
    search_company_in_base, add_education, add_experience, delete_experience, \
    delete_education, do_tab, delete_ind_tags

logger = get_logger('myjobox_log', level=logging.INFO)


class AdminPublishJob(mixins.IsAdminMixin, View):
    def get(self, request, job_id: int):
        job_instance = services.get_job_by_id(job_id)

        if job_instance.status != 'published':
            # Если это ваканcия публикуется в первые
            if job_instance.published_at is None:
                job_instance.published_at = timezone.now()
                job_instance.expire_at = timezone.now() + timezone.timedelta(
                    days=30)

            job_instance.status = "published"
            job_instance.save()

        # Если прошло время
        if job_instance.expire_at < timezone.now():
            job_instance.status = "closed"

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class AdminRejectJob(mixins.IsAdminMixin, View):
    def get(self, request, job_id: int):
        job_instance = services.get_job_by_id(job_id)

        job_instance.status = "rejected"
        job_instance.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class AdminCloseJob(mixins.IsAdminMixin, View):
    def get(self, request, job_id: int):
        job_instance = services.get_job_by_id(job_id)

        job_instance.status = "closed"
        job_instance.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# --- Добавление Реферала в Cookies ------------
class RefLinkView(View):
    def get(self, request, user_ref_code):
        response = HttpResponseRedirect(reverse('industrial:sign_up'))
        response.set_cookie('ref_code', user_ref_code)
        print('user_ref_code', user_ref_code)
        return response


class SignInAppView(View):
    """Авторизация соискателя"""

    def get(self, request):
        return render(request, 'industrial/pages/signinapp.html', {})

    def post(self, request):
        sing_in_form = forms.SignInForm(request.POST)
        if sing_in_form.is_valid():
            username = lower(sing_in_form.cleaned_data['email'])
            password = sing_in_form.cleaned_data['password']
            try:
                user_ty = cb_models.User.objects.get(
                    email=lower(username)).user_type
            except:
                return render(request, 'industrial/pages/signinapp.html',
                              {'sing_in_error': True})

            user = authenticate(username=lower(username), password=password)
            if user is not None and user_ty == 'APPLICANT':
                login(request, user)
                return HttpResponseRedirect(reverse('industrial:dashboardapp'))
        return render(request, 'industrial/pages/signinapp.html',
                      {'sing_in_error': True})


class SignUpAppView(View):
    """Регистрация соискателя"""

    def get(self, request):
        return render(request, 'industrial/pages/signupapp.html', {})

    def post(self, request):
        errors = {
            "applicant_not_found": False,
            "different_passwords": False,
            "wrong_password": False,
            "tel_already_registered": False,
            "wrong_email": False,
            'applicant_already_registered': False,
        }
        rd = utils.dump_post_to_dict(request.POST)
        sign_upapp_form = forms.SignUpappForm(request.POST)
        req = request.POST
        print('rd', rd)

        if sign_upapp_form.is_valid():

            if find_user_in_base(lower(sign_upapp_form.cleaned_data['email'])):
                errors["applicant_already_registered"] = True

            if len(sign_upapp_form.cleaned_data['password']) < 8:
                errors["wrong_password"] = True

            if sign_upapp_form.cleaned_data['password'] != \
                    sign_upapp_form.cleaned_data['password_repeat']:
                errors["different_passwords"] = True

            if sign_upapp_form.cleaned_data['tel'] is None:
                errors["wrong_tel"] = True

            if not (errors["wrong_password"]
                    or errors["different_passwords"]
                    or errors["applicant_not_found"]
                    or errors["applicant_already_registered"]):

                registration_res = services.register_new_applicant(
                    email=lower(sign_upapp_form.cleaned_data['email']),
                    password=sign_upapp_form.cleaned_data['password'],
                    tel=sign_upapp_form.cleaned_data['tel']
                )
                print('registration_res', registration_res)

                if registration_res.email is not None:
                    return render(
                        request,
                        'industrial/pages/signinapp.html',
                        {'show_success_sign_up_message': True}
                    )
            else:
                return render(
                    request,
                    'industrial/pages/signupapp.html',
                    {
                        'errors': errors,
                        'rd': rd
                    }
                )
        return render(request, 'industrial/pages/signupapp.html',
                      {'sing_up_error': True})


class SignInView(View):
    """Авторизация компании"""

    def get(self, request):
        return render(request, 'industrial/pages/signin.html', {})

    def post(self, request):
        sing_in_form = forms.SignInForm(request.POST)
        if sing_in_form.is_valid():
            username = lower(sing_in_form.cleaned_data['email'])
            password = sing_in_form.cleaned_data['password']
            user = authenticate(username=lower(username), password=password)
            # user_ty = cb_models.User.objects.filter(email=username).first().user_type
            try:
                user_ty = cb_models.User.objects.get(
                    email=lower(username)).user_type
            except:
                return render(request, 'industrial/pages/signin.html',
                              {'sing_in_error': True})
            if user is not None and user_ty == 'INT':
                login(request, user)
                return HttpResponseRedirect(reverse('industrial:dashboard'))

        return render(request, 'industrial/pages/signin.html',
                      {'sing_in_error': True})


class SignUpView(View):
    """Регистрация компании"""

    def get(self, request):
        return render(request, 'industrial/pages/signup.html', {})

    def add_to_ref_chain(self, ref_code, referral_company):
        """ Добавить запись про рефералство"""

        affiliate_company = services.get_company_by_ref_code(ref_code)
        if affiliate_company:
            services.add_new_referral_chain(
                affiliate=affiliate_company,
                referral=referral_company,
                code=ref_code
            )

    def post(self, request):
        errors = {
            "company_not_found": False,
            "different_passwords": False,
            "wrong_password": False,
            "wrong_inn": False,
            'not_active': False,
            'company_already_registered': False,
            'email_already_registered': False,
        }
        rd = utils.dump_post_to_dict(request.POST)
        sign_up_form = forms.SignUpForm(request.POST)
        if sign_up_form.is_valid():

            clear_inn = sign_up_form.cleaned_data['inn']

            da_search = utils.DaDataCompany(search_query=int(clear_inn))
            da_search.do_search()
            company_info = da_search.searching_company_info

            if find_user_in_base(sign_up_form.cleaned_data['email']):
                errors["email_already_registered"] = True

            if search_company_in_base(sign_up_form.cleaned_data['inn']):
                errors['company_already_registered'] = True

            try:
                if clear_inn != company_info['inn']:
                    errors['company_not_found'] = True
            except:
                errors['company_not_found'] = True

            if len(sign_up_form.cleaned_data['password']) < 8:
                errors["wrong_password"] = True
            if sign_up_form.cleaned_data['password'] != \
                    sign_up_form.cleaned_data['password_repeat']:
                errors["different_passwords"] = True
            if company_info is None or sign_up_form.cleaned_data[
                'inn'] is None:
                errors["company_not_found"] = True
            if sign_up_form.cleaned_data['inn'] is None:
                errors["wrong_inn"] = True
            elif company_info and company_info['status'] == 'LIQUIDATED':
                errors["not_active"] = True

            if not (errors["wrong_password"] or errors["different_passwords"]
                    or errors["company_not_found"] or errors["not_active"]
                    or errors['company_already_registered'] or errors[
                        "wrong_inn"]
                    or errors['email_already_registered']):

                registration_res = services.register_new_industrial(
                    email=lower(sign_up_form.cleaned_data['email']),
                    password=sign_up_form.cleaned_data['password'],
                    inn=sign_up_form.cleaned_data['inn'],
                    company_info=company_info,
                    dadata_date=da_search.result[0]['data']
                )

                if (registration_res['company'] is not None) and (
                        registration_res['worker'] is not None):
                    # Добавим пользователя в реф систему
                    ref_code = request.COOKIES.get('ref_code')
                    if ref_code:
                        self.add_to_ref_chain(
                            ref_code=ref_code,
                            referral_company=registration_res['company']
                        )
                    return render(
                        request,
                        'industrial/pages/signin.html',
                        {'show_success_sign_up_message': True}
                    )
            else:
                return render(
                    request,
                    'industrial/pages/signup.html',
                    {
                        'errors': errors,
                        'rd': rd

                    }
                )
        return render(request, 'industrial/pages/signup.html',
                      {'sing_up_error': True})


class ForgotPasswordView(View):
    """Забыли пароль"""

    def get(self, request):
        return render(request, 'industrial/pages/forgot_password.html', {})

    def post(self, request):
        print(request.POST)
        forgot_email = forms.ForgotPasswordForm(request.POST)
        if forgot_email.is_valid():
            secret_key = secrets.token_urlsafe(6)
            email = lower(forgot_email.cleaned_data['email'])
            r.mset({'secret_key': secret_key})
            r.mset({'username': email})
            core_utils.send_forgot_pass(email, secret_key)
            return HttpResponseRedirect(reverse('industrial:enter_key'))
        return render(request, 'industrial/pages/forgot_password.html',
                      {'sing_in_error': True})


class EnterKeyView(View):
    """Ввести ключ активации"""

    def get(self, request):
        return render(request, 'industrial/pages/enter_key.html', {})

    def post(self, request):
        key_int = forms.ForgotPasswordFormKey(request.POST)
        if key_int.is_valid():
            key = key_int.cleaned_data['key']
            secret_key = str(r.get('secret_key'))[2:-1]
            if key == secret_key:
                return HttpResponseRedirect(reverse('industrial:signre'))
        return render(request, 'industrial/pages/enter_key.html',
                      {'wrong_key': True})


class SignReView(View):
    """Сброс пароля"""

    def get(self, request):
        return render(request, 'industrial/pages/signre.html', {})

    def post(self, request):
        print(request.POST)
        pass_form = forms.SignReForm(request.POST)
        if pass_form.is_valid():

            password1 = pass_form.cleaned_data['password1']
            password2 = pass_form.cleaned_data['password2']
            if password1 == password2 and password1 is not None:
                username = str(r.get('username'))[2:-1]
                password_reset(username, password1)
                return HttpResponseRedirect(reverse('industrial:sign_in'))

        return render(request, 'industrial/pages/signre.html',
                      {'sing_re_error': True})


class GetCompanyByInn(View):
    def post(self, request):
        js = json.loads(request.body)
        company = in_models.Company.objects.filter(inn=js['inn']).first()
        if company:
            return JsonResponse(
                {
                    'company': {
                        'inn': company.inn
                    }
                }
            )
        else:
            return JsonResponse({}, safe=False)


class Logout(View):
    def get(self, request):
        try:
            logout(request)
            return HttpResponseRedirect(reverse('bulletin_board:index'))
        except:
            return redirect('bulletin_board:index')


class ConfirmEmailAppView(mixins.OnlyIndustrialWorkerMixin, View):
    """Подтверждение почты"""

    view_uniq_name = 'confirm_email_view'

    def get(self, request):
        core_utils.send_user_email_confirmation_code(request.user)
        _confirmation_code = request.GET.get('confirmation_code')
        is_code_correct = cb_services.confirm_user_email_by_code(
            request.user, _confirmation_code)

        print('_confirmation_code: ', _confirmation_code)
        print('is_code_correct: ', is_code_correct)
        print('request.user: ', request.user)

        return render(request, 'industrial/pages/confirm_emailapp.html')

    def post(self, request):
        _confirmation_code = request.POST.get('confirmation_code')
        is_code_correct = cb_services.confirm_user_email_by_code(
            request.user, _confirmation_code)

        print('_confirmation_code: ', _confirmation_code)
        print('is_code_correct: ', is_code_correct)
        print('request.user: ', request.user)

        if is_code_correct:
            return redirect('industrial:user_agreementapp')
        else:
            return render(
                request,
                'industrial/pages/confirm_emailapp.html',
                context={'is_code_wrong': True}
            )


class ConfirmEmailView(mixins.OnlyIndustrialWorkerMixin, View):
    """Подтверждение почты"""

    view_uniq_name = 'confirm_email_view'

    def get(self, request):
        core_utils.send_user_email_confirmation_code(request.user)
        _confirmation_code = request.GET.get('confirmation_code')
        is_code_correct = cb_services.confirm_user_email_by_code(
            request.user, _confirmation_code)
        #
        return render(request, 'industrial/pages/confirm_email.html')

    def post(self, request):
        _confirmation_code = request.POST.get('confirmation_code')
        is_code_correct = cb_services.confirm_user_email_by_code(
            request.user, _confirmation_code)

        print('_confirmation_code: ', _confirmation_code)
        print('is_code_correct: ', is_code_correct)

        if is_code_correct:
            return redirect('industrial:dashboard')
        else:
            return render(
                request,
                'industrial/pages/confirm_email.html',
                context={'is_code_wrong': True}
            )


class ResendConfirmEmailCodeView(mixins.OnlyIndustrialWorkerMixin, View):
    """Повторно отправить код подтвержденя"""

    view_uniq_name = 're_send_confirm_email_view'

    def post(self, request):

        if not request.user.is_email_confirmed:
            if len(request.user.email_confirm_code) > 6:
                cb_services.refresh_email_confirmation_code(request.user)
            core_utils.send_user_email_confirmation_code(request.user)
        return render(request, 'industrial/pages/confirm_email.html',
                      context={'code_is_sent': True})


class ResendConfirmEmailCodeAppView(mixins.OnlyIndustrialWorkerMixin, View):
    """Повторно отправить код подтвержденя"""

    view_uniq_name = 're_send_confirm_email_view'

    def post(self, request):

        if not request.user.is_email_confirmed:
            if len(request.user.email_confirm_code) > 6:
                cb_services.refresh_email_confirmation_code(request.user)
            core_utils.send_user_email_confirmation_code(request.user)
        return render(request, 'industrial/pages/confirm_emailapp.html',
                      context={'code_is_sent': True})


class Dashboard(mixins.OnlyIndustrialWorkerMixin, View):
    def get(self, request):
        try:
            company_id = Company.objects.get(user=request.user).id

            short_statistic_info = services.get_company_short_statistic_info(
                request.user.industrial_worker.company
            )
            _transaction_totals = services.get_company_transaction_totals(
                company=request.user.industrial_worker.company)

            ref_inst = CompanyReferralChain.objects.filter(
                affiliate_id=company_id)
            return render(
                request,
                'industrial/pages/dashboard.html',
                {
                    'current_nav_link': 'dashboard',
                    'short_statistic_info': short_statistic_info,
                    'transaction_totals': _transaction_totals,
                    'ref_inst': ref_inst,
                }
            )
        except:
            return redirect('industrial:sign_in')


class DashboardAPP(mixins.OnlyIndustrialWorkerMixin, View):

    def get_content(self, request):
        try:
            user_email = request.user.email
            app_inst = Applicant.objects.get(user_email=user_email)
            teg_inst = TagApp.objects.filter(tags_app=app_inst.id)
            level = cb_models.EducationLevel.objects.all()
            education_inst = EducationPlace.objects.filter(
                applicant_id=app_inst.id)
            experience_inst = JobExperience.objects.filter(
                applicant_id=app_inst.id)
            content = {'app_id': app_inst.id, 'user_email': user_email,
                       'app_inst': app_inst, 'teg_inst': teg_inst,
                       'data': str(app_inst.date_of_birth),
                       'current_nav_link': 'dashboardapp', 'level': level,
                       'education_inst': education_inst,
                       'experience_inst': experience_inst}
            return content, app_inst
        except:
            return redirect('industrial:sign_in_app')

    def get(self, request):
        content, app_inst = self.get_content(request)
        return render(request,
                      'industrial/pages/dashboardapp.html',
                      {'content': content})

    def post(self, request):
        content, app_inst = self.get_content(request)
        if str(request.POST['show']) == 'Больше не ищу работу':
            app_inst.show_on_main_page = False
        if str(request.POST['show']) == 'Разместить резюме на сайте':
            app_inst.show_on_main_page = True
        app_inst.save()
        return render(request, 'industrial/pages/dashboardapp.html',
                      {'content': content})


class Summary(mixins.OnlyIndustrialWorkerMixin, View):
    """Пока не используется """

    def get(self, request):
        user_email = request.user.email
        app_id = Applicant.objects.get(user_email=user_email).id
        content = {'app_id': app_id, 'user_email': user_email,
                   'current_nav_link': 'summary'}
        return render(request, 'industrial/pages/summary.html', content)


class EditSummaryExperience(View):
    def post(self, request):
        add_experience(request)
        return HttpResponseRedirect(reverse('industrial:edit_summary'))


class EditSummaryEducation(View):
    def post(self, request):
        add_education(request)
        return HttpResponseRedirect(reverse('industrial:edit_summary'))


class EditSummary(mixins.OnlyIndustrialWorkerMixin, View):
    def get(self, request):
        context = {
            "categories": cb_models.JobCategory.objects.all(),
            "experiences": cb_models.Experience.objects.all(),
            "employment_types": cb_models.EmploymentType.objects.all(),
            "work_schedules": cb_models.WorkSchedule.objects.all(),
            "locations": cb_models.Location.objects.all(),
            "salary_conditions": cb_models.AdditionalSalaryCondition.objects.all(),
            "tags": cb_models.TagApp.objects.all(),
            "communication_methods": cb_models.CommunicationMethod.objects.all(),
            "level": cb_models.EducationLevel.objects.all(),
            'domain_name': env('DOMAIN_NAME'),
        }
        user_email = request.user.email
        app_inst = Applicant.objects.get(user_email=user_email)

        education_inst = EducationPlace.objects.filter(
            applicant_id=app_inst.id)
        experience_inst = JobExperience.objects.filter(
            applicant_id=app_inst.id)
        if app_inst.have_resume:
            app_inst.about_app = do_tab(app_inst.about_app)
            app_inst.save()

        content = {
            'data': str(app_inst.date_of_birth),
            'app_inst': app_inst,
            'education_inst': education_inst,
            'experience_inst': experience_inst,
            'app_id': app_inst.id,
            'user_email': user_email,
            'current_nav_link': 'edit_summary',
            'valid_error': False
        }
        return render(request, 'industrial/pages/edit_summary.html',
                      {'content': content, **context})

    def post(self, request):
        # try:
        app_inst = Applicant.objects.get(user_email=request.user)
        if not app_inst.have_resume:
            add_or_update_app(request)
            return redirect('industrial:edit_summary')
        add_or_update_app(request)
        return redirect('industrial:dashboardapp')
        # except:
        #     context = {
        #         "categories": cb_models.JobCategory.objects.all(),
        #         "experiences": cb_models.Experience.objects.all(),
        #         "employment_types": cb_models.EmploymentType.objects.all(),
        #         "work_schedules": cb_models.WorkSchedule.objects.all(),
        #         "locations": cb_models.Location.objects.all(),
        #         "salary_conditions": cb_models.AdditionalSalaryCondition.objects.all(),
        #         "tags": cb_models.TagApp.objects.all(),
        #         "communication_methods": cb_models.CommunicationMethod.objects.all(),
        #         "level": cb_models.EducationLevel.objects.all()
        #     }
        #     user_email = request.user.email
        #     app_inst = Applicant.objects.get(user_email=user_email)
        #     education_inst = EducationPlace.objects.filter(
        #         applicant_id=app_inst.id)
        #     experience_inst = JobExperience.objects.filter(
        #         applicant_id=app_inst.id)
        #
        #     content = {
        #         'data': str(app_inst.date_of_birth),
        #         'app_inst': app_inst,
        #         'education_inst': education_inst,
        #         'experience_inst': experience_inst,
        #         'app_id': app_inst.id,
        #         'user_email': user_email,
        #         'current_nav_link': 'edit_summary',
        #         'valid_error': True
        #     }
        #     return render(request, 'industrial/pages/edit_summary.html',
        #                   {'content': content, **context})


class Profile(mixins.OnlyIndustrialWorkerMixin, View):
    def get(self, requests, *args, **kwargs):
        _password_was_no_changed = requests.GET.get(
            'password_was_no_changed')
        _password_was_changed = requests.GET.get('password_was_changed')

        return render(
            requests,
            'industrial/pages/company_profile.html',
            {
                'password_was_changed': _password_was_changed,
                'password_was_no_changed': _password_was_no_changed,
                'current_nav_link': 'profile'
            }
        )


class ProfileEditBrandInfo(mixins.OnlyIndustrialWorkerMixin, View):
    def post(self, request):
        _brand_name = request.POST.get('brand_name')
        if _brand_name:
            request.user.industrial_worker.company.brand_name = _brand_name

        if request.FILES.get('brand_logo'):
            print(request.FILES)
            request.user.industrial_worker.company.brand_logo.save(
                request.FILES.get('brand_logo').name,
                request.FILES.get('brand_logo')
            )

        request.user.industrial_worker.company.save()

        return HttpResponseRedirect(reverse('industrial:profile'))


class ProfileEditAdministratorInfo(mixins.OnlyIndustrialWorkerMixin, View):
    def post(self, request):
        upd_adm_form = forms.EditAdministratorInfo(request.POST)
        if upd_adm_form.is_valid():
            request.user.industrial_worker.name = \
                upd_adm_form.cleaned_data[
                    'name']
            request.user.industrial_worker.position = \
                upd_adm_form.cleaned_data['position']
            request.user.industrial_worker.phone = \
                upd_adm_form.cleaned_data[
                    'phone']
            request.user.industrial_worker.email = \
                upd_adm_form.cleaned_data[
                    'email']
            request.user.industrial_worker.save()
        return HttpResponseRedirect(reverse('industrial:profile'))


class ProfileEditCompanyDescription(mixins.OnlyIndustrialWorkerMixin, View):

    def post(self, request):
        des_form = forms.EditCompanyDescription(request.POST)
        if des_form.is_valid():
            request.user.industrial_worker.company.company_description = \
                des_form.cleaned_data['description']
            request.user.industrial_worker.company.save()

        return HttpResponseRedirect(reverse('industrial:profile'))


class ProfileEditUserPassword(mixins.OnlyIndustrialWorkerMixin, View):

    def post(self, request):
        pass_form = forms.EditUserPasswordForm(request.POST)

        if pass_form.is_valid():

            current_user = authenticate(username=request.user.username,
                                        password=pass_form.cleaned_data[
                                            'password'])
            if (current_user is not None) and (
                    pass_form.cleaned_data['new_password'] ==
                    pass_form.cleaned_data['new_password_repeat']) and \
                    len(pass_form.cleaned_data['new_password']) >= 8:
                request.user.set_password(
                    pass_form.cleaned_data['new_password'])
                request.user.save()

                return HttpResponseRedirect(
                    reverse(
                        'industrial:profile') + '?password_was_changed=1')

        return HttpResponseRedirect(
            reverse('industrial:profile') + '?password_was_no_changed=1')


class AddNewJob(mixins.OnlyIndustrialWorkerMixin, View):
    def get(self, request):
        context = {
            "categories": cb_models.JobCategory.objects.all(),
            "experiences": cb_models.Experience.objects.all(),
            "employment_types": cb_models.EmploymentType.objects.all(),
            "work_schedules": cb_models.WorkSchedule.objects.all(),
            "locations": cb_models.Location.objects.all(),
            "salary_conditions": cb_models.AdditionalSalaryCondition.objects.all(),
            "tags": cb_models.Tag.objects.all(),
            "communication_methods": cb_models.CommunicationMethod.objects.all(),
        }

        return render(
            request,
            'industrial/pages/job_editor.html',
            context={
                'current_nav_link': 'new_job',
                **context
            }
        )

    def post(self, request):
        # try:
        inf = utils.get_job_info_from_post_request(request)
        new_job_instance = services.add_or_update_job(
            company=request.user.industrial_worker.company,
            job_data=inf
        )
        return redirect('industrial:jobs_list')
        # except:
        #     context = {
        #         "categories": cb_models.JobCategory.objects.all(),
        #         "experiences": cb_models.Experience.objects.all(),
        #         "employment_types": cb_models.EmploymentType.objects.all(),
        #         "work_schedules": cb_models.WorkSchedule.objects.all(),
        #         "locations": cb_models.Location.objects.all(),
        #         "salary_conditions": cb_models.AdditionalSalaryCondition.objects.all(),
        #         "tags": cb_models.Tag.objects.all(),
        #         "communication_methods": cb_models.CommunicationMethod.objects.all(),
        #     }
        #
        #     return render(request, 'industrial/pages/job_editor.html',
        #                   {'current_nav_link': 'new_job', 'valid_error': True,
        #                    **context})


class ViewJob(mixins.OnlyIndustrialWorkerMixin, View):
    def get(self, request, job_id):
        job_instance = services.get_company_job_by_id(
            request.user.industrial_worker.company, job_id)
        return render(request, 'industrial/pages/job_view.html',
                      {'job_instance': job_instance})


class DeleteJob(mixins.OnlyIndustrialWorkerMixin, View):
    def get(self, request, job_id):
        del_job_by_id(job_id)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteResponse(mixins.OnlyIndustrialWorkerMixin, View):
    def get(self, request, resp_id):
        del_response_by_id(resp_id)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class JobsList(mixins.OnlyIndustrialWorkerMixin, View):

    def get(self, request):
        company = request.user.industrial_worker.company

        _transaction_totals = services.get_company_transaction_totals(
            company=request.user.industrial_worker.company)
        context = {
            'company': company,
            'current_nav_link': 'jobs_list',
            'payment_ruble_price': settings.JOB_PAYMENT_PRICES['ruble'],
            'payment_bonus_point_price': settings.JOB_PAYMENT_PRICES[
                'bonus_point'],
            'transaction_totals': _transaction_totals}

        return render(request, 'industrial/pages/jobs_list.html', context)


class TagsAPI(mixins.OnlyIndustrialWorkerMixin, View):
    """Удаление индивидуальных тегов"""

    def post(self, request):
        js = json.loads(request.body)
        delete_ind_tags(js['job_id'])
        return HttpResponse('Response')


class JobListAPI(mixins.OnlyIndustrialWorkerMixin, View):
    def post(self, request):
        js = json.loads(request.body)
        _jobs_list = in_models.Job.objects.get_selected_all_info_selected().filter(
            company=request.user.industrial_worker.company,
            title__icontains=js['title'],
            status__icontains=js['status']
        ).annotate(
            responses_coun=Count('responses')
        )

        ind_work = request.user.industrial_worker

        if ind_work.phone is None or ind_work.email is None or ind_work.name is None or ind_work.position is None:
            call_modal = 'true'
        else:
            call_modal = 'false'

        jobs_list = []
        for job in _jobs_list:
            if job.expires_after_days == 0 and job.status == 'published':
                job.status = 'need_to_paid'

            jobs_list.append(
                {
                    'id': job.id,
                    'title': job.title,
                    'location': job.location.city,
                    'employment_type': job.employment_type.title,
                    'salary': job.salary,
                    'salary_condition': job.salary_condition.title,
                    'status': job.status,
                    'created_at': job.created_at.isoformat(),
                    'expires_after_days': job.expires_after_days,
                    'responses': job.responses_coun,
                    'call_modal': call_modal,
                    'edit_url': reverse('industrial:edit_job',
                                        kwargs={'job_id': job.id}),
                    'view_url': reverse('industrial:view_job',
                                        kwargs={'job_id': job.id}),
                    'delete_url': reverse('industrial:delete_job',
                                          kwargs={'job_id': job.id}),
                }
            )
        return JsonResponse(
            {
                'jobs_list': jobs_list,
            },
            safe=False
        )


class PayForJobAPI(mixins.OnlyIndustrialWorkerMixin, View):
    def post(self, request):
        js = json.loads(request.body)
        job_id = js['job_id']
        print('job_id', job_id)
        job_instance = services.get_job_by_id(job_id)

        if job_instance.company_id != request.user.industrial_worker.company.id:
            raise Exception("Wrong!!!!!")

        balance_type = js['balance_type']

        services.create_company_transaction_for_job_payment(
            currency=balance_type,
            job=job_instance
        )
        return JsonResponse({}, safe=False)


class EditJob(mixins.OnlyIndustrialWorkerMixin, View):

    def get(self, request, job_id):
        context = {
            "categories": cb_models.JobCategory.objects.all(),
            "experiences": cb_models.Experience.objects.all(),
            "employment_types": cb_models.EmploymentType.objects.all(),
            "work_schedules": cb_models.WorkSchedule.objects.all(),
            "locations": cb_models.Location.objects.all(),
            "salary_conditions": cb_models.AdditionalSalaryCondition.objects.all(),
            "tags": cb_models.Tag.objects.all(),
            "ind_tags": cb_models.IndividualTag.objects.filter(ind_job_tegs=job_id),
            "all_ind_tags": cb_models.IndividualTag.objects.filter(all_ind_job_tegs=job_id),
            "communication_methods": cb_models.CommunicationMethod.objects.all(),
        }

        job_instance = services.get_company_job_by_id(
            request.user.industrial_worker.company, job_id)
        return render(request, 'industrial/pages/job_editor.html',
                      {'job_instance': job_instance, **context})

    def post(self, request, job_id):
        context = {
            "categories": cb_models.JobCategory.objects.all(),
            "experiences": cb_models.Experience.objects.all(),
            "employment_types": cb_models.EmploymentType.objects.all(),
            "work_schedules": cb_models.WorkSchedule.objects.all(),
            "locations": cb_models.Location.objects.all(),
            "salary_conditions": cb_models.AdditionalSalaryCondition.objects.all(),
            "tags": cb_models.Tag.objects.all(),
            "ind_tags": cb_models.IndividualTag.objects.filter(
                ind_job_tegs=job_id),
            "all_ind_tags": cb_models.IndividualTag.objects.filter(
                all_ind_job_tegs=job_id),
            "communication_methods": cb_models.CommunicationMethod.objects.all(),
        }
        # try:
        job_instance = services.get_company_job_by_id(
            request.user.industrial_worker.company, job_id)
        inf = utils.get_job_info_from_post_request(request)
        inf['job_instance'] = job_instance

        update_job_instance = services.add_or_update_job(
            company=request.user.industrial_worker.company,
            job_data=inf
        )
        return redirect('industrial:jobs_list')
        # except:
        #     job_instance = services.get_company_job_by_id(
        #         request.user.industrial_worker.company, job_id)
        #     return render(request, 'industrial/pages/job_editor.html',
        #                   {'job_instance': job_instance, 'valid_error': True,
        #                    **context})


class CandidatesList(mixins.OnlyIndustrialWorkerMixin, View):

    def get(self, request):
        company = request.user.industrial_worker.company
        responses_list = in_models.ResponseToJob.objects.filter(
            job__company_id=company.id).all()
        return render(
            request,
            'industrial/pages/candidates.html',
            {
                'responses_list': responses_list,
                'responses_count': len(responses_list),

                'current_nav_link': 'candidates_list'
            }
        )


class Payment(mixins.OnlyIndustrialWorkerMixin, View):
    def get(self, request):
        return render(
            request,
            'industrial/pages/payment.html',
            context={
                'current_nav_link': 'payment'
            }
        )


class UserAgreement(mixins.OnlyIndustrialWorkerMixin, View):
    view_uniq_name = "industrial_user_agreement"

    def get(self, request):
        return render(
            request=request,
            template_name='industrial/pages/user_agreement.html',
            context={
                'current_nav_link': 'user_agreement'
            }
        )

    def post(self, request):
        user_ty = cb_models.User.objects.get(
            email=request.user.email).user_type
        _is_agree = request.POST.get('is_agree')

        if _is_agree:
            request.user.industrial_worker.is_agree_with_agreement = True
            request.user.industrial_worker.save()
            if user_ty == 'INT':
                return redirect('industrial:dashboard')
            elif user_ty == 'APPLICANT':
                return redirect('industrial:dashboardapp')

        print('sing_in_error_TRUE')
        return render(request, 'industrial/pages/user_agreement.html',
                      {'is_agree_error': True})


class Instruction(mixins.OnlyIndustrialWorkerMixin, View):

    def get(self, request):
        return render(
            request=request,
            template_name='industrial/pages/doc_2.html',
            context={
                'current_nav_link': 'instruction'
            }
        )


class Support(mixins.OnlyIndustrialWorkerMixin, View):

    def get(self, request):
        return render(
            request=request,
            template_name='industrial/pages/doc_3.html',
            context={
                'current_nav_link': 'support'
            }
        )


class UserAgreementApp(mixins.OnlyIndustrialWorkerMixin, View):
    view_uniq_name = "industrial_user_agreement"

    def get(self, request):
        return render(
            request=request,
            template_name='industrial/pages/user_agreementapp.html',
            context={
                'current_nav_link': 'user_agreement'
            }
        )

    def post(self, request):
        user_ty = cb_models.User.objects.get(
            email=request.user.email).user_type
        _is_agree = request.POST.get('is_agree')

        if _is_agree:
            request.user.app_user.is_agree_with_agreement = True
            request.user.app_user.save()
            if user_ty == 'APPLICANT':
                return redirect('industrial:dashboardapp')

        print('sing_in_error_TRUE')
        return render(request, 'industrial/pages/user_agreementapp.html',
                      {'is_agree_error': True})


class InstructionApp(mixins.OnlyIndustrialWorkerMixin, View):

    def get(self, request):
        return render(
            request=request,
            template_name='industrial/pages/doc_2app.html',
            context={
                'current_nav_link': 'instructionapp'
            }
        )


class SupportApp(mixins.OnlyIndustrialWorkerMixin, View):

    def get(self, request):
        return render(
            request=request,
            template_name='industrial/pages/doc_3app.html',
            context={
                'current_nav_link': 'supportapp'
            }
        )


class Finance(mixins.OnlyIndustrialWorkerMixin, View):
    def get(self, request):
        _currency = request.GET.get('currency')

        transactions = services.get_company_transactions(
            company=request.user.industrial_worker.company,
            currency=_currency
        )

        _transaction_totals = services.get_company_transaction_totals(
            company=request.user.industrial_worker.company)

        return render(
            request,
            'industrial/pages/finance.html',
            context={
                'current_nav_link': 'finance',
                'transactions': transactions,
                'transaction_totals': _transaction_totals
            }
        )


class PaymentInvoices(mixins.OnlyIndustrialWorkerMixin, View):
    def get(self, request):
        invoices = get_company_payment_invoices(
            company=request.user.industrial_worker.company)

        return render(
            request,
            'industrial/pages/invoices_list.html',
            context={
                'current_nav_link': 'finance',
                'invoices': invoices
            }
        )


class PaymentInvoice(mixins.OnlyIndustrialWorkerMixin, View):
    def get(self, request, invoice_id):
        invoice_instance = get_invoice_by_id(invoice_id)

        if invoice_instance.company_id == request.user.industrial_worker.company.id:
            logger.info(f'invoice_instance status {invoice_instance.status}')
            return render(
                request,
                'industrial/pages/payment_invoice.html',
                context={
                    'invoice': invoice_instance
                }
            )


class PaymentInvoiceCheck(mixins.OnlyIndustrialWorkerMixin, View):
    def get(self, request, invoice_id):
        invoice_instance = get_invoice_by_id(invoice_id)

        if invoice_instance.company_id == request.user.industrial_worker.company.id:

            if invoice_instance.tinkoff_card_payment:
                py_services.refresh_tinkoff_card_payment(
                    invoice_instance.tinkoff_card_payment)

        return redirect('industrial:payment_invoice',
                        invoice_id=invoice_instance.id)
