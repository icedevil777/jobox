from django.contrib import admin
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = "industrial"

urlpatterns = [

    path('admin/request/publish_job_<int:job_id>',
         views.AdminPublishJob.as_view(), name='admin_publish_job'),
    path('admin/request/reject_job_<int:job_id>',
         views.AdminRejectJob.as_view(), name='admin_reject_job'),
    path('admin/request/close_job_<int:job_id>', views.AdminCloseJob.as_view(),
         name='admin_close_job'),

    path('reg-<str:user_ref_code>/', views.RefLinkView.as_view(),
         name='ref_link_view'),

    path('signin/', views.SignInView.as_view(), name='sign_in'),
    path('signinapp/', views.SignInAppView.as_view(), name='sign_in_app'),
    path('signupapp/', views.SignUpAppView.as_view(), name='sign_up_app'),
    path('get_company/', csrf_exempt(views.GetCompanyByInn.as_view()),
         name='get_company_by_inn'),

    path('signup/', views.SignUpView.as_view(), name='sign_up'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('confirm_email/', views.ConfirmEmailView.as_view(),
         name='confirm_email'),  # Поддтвержденые почты

    path('confirm_email_app/', views.ConfirmEmailAppView.as_view(),
         name='confirm_emailapp'),

    path('confirm_email/send_again',
         views.ResendConfirmEmailCodeView.as_view(),
         name='re_confirm_email_code'),  # Поддтвержденые почты

    path('confirm_email/send_againapp',
         views.ResendConfirmEmailCodeAppView.as_view(),
         name='re_confirm_email_codeapp'),  # Поддтвержденые почты

    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),

    path('dashboardapp/', views.DashboardAPP.as_view(), name='dashboardapp'),

    path('summary/', csrf_exempt(views.Summary.as_view()),
         name='summary'),

    path('edit_summary/', csrf_exempt(views.EditSummary.as_view()),
         name='edit_summary'),

    path('edit_summary/education/',
         csrf_exempt(views.EditSummaryEducation.as_view()),
         name='education'),

    path('edit_summary/experience/',
         csrf_exempt(views.EditSummaryExperience.as_view()),
         name='experience'),

    path('delete_tags/',
         csrf_exempt(views.TagsAPI.as_view()),
         name='delete_tags'),

    # path('delete_summary/education/',
    #      csrf_exempt(views.DeleteSummaryEducation.as_view()),
    #      name='delete_education'),
    #
    # path('delete_summary/experience/',
    #      csrf_exempt(views.DeleteSummaryExperience.as_view()),
    #      name='delete_experience'),

    path('profile/', views.Profile.as_view(), name='profile'),

    path('profile/edit_brand_info/', views.ProfileEditBrandInfo.as_view(),
         name='edit_brand_info'),

    path('profile/edit_administrator_info/',
         views.ProfileEditAdministratorInfo.as_view(),
         name='edit_administrator_info'),

    path('profile/edit_company_description/',
         views.ProfileEditCompanyDescription.as_view(),
         name='edit_company_description'),

    path('profile/edit_user_password/',
         views.ProfileEditUserPassword.as_view(), name='edit_user_password'),

    path('jobs/new', csrf_exempt(views.AddNewJob.as_view()), name='add_new_job'),
    path('jobs/list', csrf_exempt(views.JobsList.as_view()), name='jobs_list'),

    path('jobs/list_api', csrf_exempt(views.JobListAPI.as_view()),
         name='jobs_list_api'),
    path('jobs/pay_for_job_api', csrf_exempt(views.PayForJobAPI.as_view()),
         name='pay_for_job_api'),

    path('jobs/<int:job_id>/edit', csrf_exempt(views.EditJob.as_view()), name='edit_job'),
    path('jobs/<int:job_id>/view', views.ViewJob.as_view(), name='view_job'),
    path('jobs/<int:job_id>/delete', views.DeleteJob.as_view(),
         name='delete_job'),

    path('candidates/<int:resp_id>/delete', views.DeleteResponse.as_view(),
         name='delete_resp'),

    path('candidates/', views.CandidatesList.as_view(), name='candidates'),

    path('payment/', views.Payment.as_view(), name='payment'),

    path('user_agreement/', views.UserAgreement.as_view(),
         name='user_agreement'),
    path('instruction/', views.Instruction.as_view(), name='instruction'),
    path('support/', views.Support.as_view(), name='support'),

    path('user_agreementapp/', views.UserAgreementApp.as_view(),
         name='user_agreementapp'),
    path('instructionapp/', views.InstructionApp.as_view(), name='instructionapp'),
    path('supportapp/', views.SupportApp.as_view(), name='supportapp'),


    path('finance/', views.Finance.as_view(), name='finance'),

    path('payment_invoices/', views.PaymentInvoices.as_view(),
         name='payment_invoices'),

    path('payment_invoices/', views.PaymentInvoice.as_view(),
         name='payment_invoice'),
    path('payment_invoices/<int:invoice_id>/', views.PaymentInvoice.as_view(),
         name='payment_invoice'),
    path('payment_invoices/<int:invoice_id>/check',
         views.PaymentInvoiceCheck.as_view(), name='payment_invoice_check'),

    path('forgot_password/', views.ForgotPasswordView.as_view(),
         name='forgot_password'),
    path('enter_key/', views.EnterKeyView.as_view(),
         name='enter_key'),
    path('signre/', views.SignReView.as_view(), name='signre'),

]
