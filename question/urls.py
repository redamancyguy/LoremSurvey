from django.urls import path
from . import views

app_name = 'question'

urlpatterns = [
    path(r'', views.Index.as_view(), name='index'),
    path(r'adduser', views.AddUser.as_view(), name='adduser'),
    path(r'manage', views.ManageQuestion.as_view(), name='manage'),
    path(r'answer', views.AnswerQuestion.as_view(), name='answer'),
    path(r'generate', views.Generate.as_view(), name='generate'),
    path(r'test', views.test, name='test'),
]
