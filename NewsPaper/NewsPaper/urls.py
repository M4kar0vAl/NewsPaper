"""
URL configuration for NewsPaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.views.generic import TemplateView
from rest_framework import routers

from news.views import NewsViewSet, ArticleViewSet

router = routers.DefaultRouter()
router.register('news', NewsViewSet, basename='news')
router.register('articles', ArticleViewSet, basename='articles')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path("account/", include("allauth.urls")),
    path('accounts/', include('accounts.urls')),
    path("i18n/", include("django.conf.urls.i18n")),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger_ui.html',
        extra_context={'schema_url': 'openapi-schema'}
        ), name='swagger-ui'),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls'))
]
