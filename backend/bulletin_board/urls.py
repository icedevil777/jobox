from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page

from . import views

app_name = 'bulletin_board'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('for-company/', views.ForCompany.as_view(), name='for_company'),

    path('blog/', views.BlogList.as_view(), name='blog_list'),
    path('blog/<int:blog_id>', views.BlogView.as_view(), name='blog_view'),

    path('companies/', views.CompaniesList.as_view(), name='companies_list'),
    path('companies/<int:company_id>', views.CompanyView.as_view(), name='company_view'),

    path('orders/', views.JobsCatalog.as_view(), name='jobs_catalog'),
    path('orders/<int:job_id>/', views.JobView.as_view(), name='job_view'),
    path('orders/<int:job_id>/apply', csrf_exempt(views.ApplyJob.as_view()), name='apply_job'),

    path('summary/', views.SummaryCatalog.as_view(), name='sum_catalog'),
    path('summary/<int:sum_id>/', views.SummaryView.as_view(), name='sum_view'),

    path('application_to_admin', views.ApplicationToAdmin.as_view(), name='application_to_admin'),

    path('doc-1', views.Doc1.as_view(), name='doc_1'),
    path('doc-2', views.Doc2.as_view(), name='doc_2'),

    path('delete_education/',
         csrf_exempt(views.DeleteSummaryEducation.as_view()),
         name='delete_education'),

    path('delete_experience/',
         csrf_exempt(views.DeleteSummaryExperience.as_view()),
         name='delete_experience'),

    path('robots.txt', views.get_robots_txt, name='robots_txt'),
    # path('sitemap.xml', views.get_sitemap_xml, name='sitemap_xml')
]
