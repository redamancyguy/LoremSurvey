"""LoremSurvey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path, include
from . import views

import question.views

from rest_framework import routers  # 路由配置模块

router = routers.DefaultRouter()
router.register(r'users',question.views.UserViewSet,basename='user')

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])




urlpatterns = [
    path(r'', views.Index.as_view(), name='index'),

    path(r'admin/', admin.site.urls),
    path(r'user/', include('user.urls', namespace="user"), name='user'),
    path(r'question/', include('question.urls', namespace='question'), name='question'),

    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('docs/', schema_view, name='docs'),

    re_path(r'(.+)/', views.NotFound.as_view(), name='notfound'),
]
