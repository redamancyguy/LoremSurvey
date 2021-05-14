from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from . import models


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'template.html', {'info': 'index'})

    def post(self, request, *args, **kwargs):
        return JsonResponse({
            'code': 0,
            'message': "Index test"
        })


class Login(View):

    def get(self, request, *args, **kwargs):
        return render(request,'login.html')

    def post(self, request, *args, **kwargs):
        if request.POST.get('username') and request.POST.get('password'):
            info = models.User.objects.filter(username=request.POST.get('username'),
                                              password=request.POST.get('password')).first()
            if info:
                import jwt
                key = 'LoremSurvey'
                payload = {'username': info.username}
                token = jwt.encode(payload, key, algorithm='HS256')
                # data2 = jwt.decode(token, key, algorithms='HS256')
                print(token)
                info.token = token
                info.save()
                obj = JsonResponse({
                    'code': 0,
                    'message': 'login successfully'
                })
                obj.set_cookie('token', token, max_age=3600)
                return obj
            else:
                return JsonResponse({
                    'code': 1,
                    'massage': 'wrong username or password'
                })
        return JsonResponse({
            'code': 1,
            'massage': 'Nothing input !'
        })


class Register(View):

    def get(self, request, *args, **kwargs):
        return render(request,'register.html')

    def post(self, request, *args, **kwargs):
        if request.POST.get('username') and request.POST.get('password'):
            try:
                models.User.objects.create(username=request.POST.get('username'),
                                           password=request.POST.get('password'), token='',
                                           phone=request.POST.get('phone'),
                                           email=request.POST.get('email'))
                return JsonResponse({
                    'code': 0,
                    'massage': 'Register successfully'
                })
            except Exception as e:
                return JsonResponse({
                    'code': 1,
                    'massage': str(e)
                })
        else:
            return JsonResponse({
                'code': 1,
                'massage': 'None username or password'
            })


class Logout(View):

    def get(self, request, *args, **kwargs):
        return render(request,'logout.html')

    def post(self, request, *args, **kwargs):
        if request.COOKIES.get('token'):
            info = models.User.objects.filter(token=request.COOKIES.get('token')).first()
            if info:
                models.User.objects.filter(token=request.COOKIES.get('token')).token = ''
                obj = JsonResponse({
                    'code': 0,
                    'message': 'logout successfully'
                })
                # obj.set_cookie('token', '', max_age=3600)
                obj.set_cookie('token', '')
                return obj
            else:
                return JsonResponse({
                    'code': 1,
                    'massage': 'wrong token'
                })
        return JsonResponse({
            'code': 7,
            'massage': 'Nothing input !'
        })