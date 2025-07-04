from django.contrib.sitemaps import Sitemap
from .models import Guide, Article  # adjust as needed

class GuideSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Guide.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()



class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Article.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()

