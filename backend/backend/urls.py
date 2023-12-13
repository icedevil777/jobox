from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers


from django.contrib.sitemaps.views import sitemap
from bulletin_board.sitemaps import JobSitemap, CompanySitemap, ApplicantSitemap, BlogSitemap, CustomSitemap

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bulletin_board.urls')),

    path('industrial/', include('industrial.urls')),

    path('payment/', include('payment.urls')),

    path('api/v1/', include(router.urls)),
    path('api-auth/',
         include('rest_framework.urls', namespace='rest_framework')),

    path('__debug__/', include('debug_toolbar.urls')),

    path('sitemap.xml', sitemap, {
        'sitemaps': {
            "jobs": JobSitemap,
            "companies": CompanySitemap,
            "applicants": ApplicantSitemap,
            "blog": BlogSitemap,
            "custom": CustomSitemap
        }
    },
         name='django.contrib.sitemaps.views.sitemap')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
