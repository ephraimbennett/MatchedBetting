"""
URL configuration for house_hedge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.sitemaps.views import sitemap
from guides.sitemaps import GuideSitemap, ArticleSitemap
from home.sitemaps import StaticViewSitemap

sitemaps = {
    "guides": GuideSitemap,
    "articles": ArticleSitemap,
    "static": StaticViewSitemap
}

urlpatterns = [
    path('', include('home.urls')),
    path('', include('finder.urls')),
    path('', include('guides.urls')),
    path('admin/', admin.site.urls),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    )

]
#handler404 = 'home.views.handler404'
LOGIN_REDIRECT_URL = "/"