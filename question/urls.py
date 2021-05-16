from django.urls import path, include
from . import views

app_name = 'question'


urlpatterns = [
    path(r'', views.Index.as_view(), name='index'),
    path(r'respondents', views.Respondents.as_view(), name='respondents'),
    path(r'manage', views.ManageQuestion.as_view(), name='manage'),
    path(r'answer', views.AnswerQuestion.as_view(), name='answer'),
    path(r'result', views.QuestionResult.as_view(), name='result'),
    path(r'generate', views.Generate.as_view(), name='generate'),
]
