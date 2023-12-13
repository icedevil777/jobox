from django.contrib.sitemaps import Sitemap
from industrial.models import Job, Company, Applicant
from core_base.models import Blog


class JobSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Job.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, item):
        return f"/orders/{item.id}/"


class CompanySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Company.objects.all()

    def lastmod(self, obj):
        return

    def location(self, item):
        return f"/companies/{item.id}/"


class ApplicantSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Applicant.objects.filter(status="published")

    def lastmod(self, obj):
        return

    def location(self, item):
        return f"/summary/{item.id}/"


class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.updated_ad

    def location(self, item):
        return f"/blog/{item.id}/"


class CustomSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return [
            "/for-company/",
            "/doc-1",
            "/doc-2"
        ]

    def lastmod(self, obj):
        return

    def location(self, item):
        return item
