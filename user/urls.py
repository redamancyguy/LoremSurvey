from django.urls import path
from . import views

app_name = 'question'

urlpatterns = [
    path(r'', views.Index.as_view(), name='index'),

    path(r'login', views.Login.as_view(), name='login'),
    path(r'logout', views.Logout.as_view(), name='logout'),
    path(r'register', views.Register.as_view(), name='register'),
    path(r'changepassword', views.ChangePassword.as_view(), name='changepassword'),
]
