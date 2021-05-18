import json

from django.core.mail import send_mail
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
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if data['username'] and data['password']:
            info = models.User.objects.filter(username=data['username'],
                                              password=data['password']).first()
            if info:
                import jwt
                key = 'LoremSurvey'
                payload = {'username': info.username}
                token = jwt.encode(payload, key, algorithm='HS256')
                # data2 = jwt.decode(token, key, algorithms='HS256')
                info.token = token
                info.save()
                obj = JsonResponse({
                    'code': 0,
                    'message': 'login successfully'
                })
                # obj.set_cookie('token', token, max_age=3600,httponly=True,secure=True,samesite='None')
                obj.set_cookie('token', token, max_age=3600)
                obj.set_cookie('username', info.username, max_age=3600)
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


class ChangePassword(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data['username']
        if not username:
            return JsonResponse({
                'code': 1,
                'message': 'I do not know your username'
            })
        uid = models.User.objects.filter(username=username).first()
        if not uid:
            return JsonResponse({
                'code': 1,
                'message': 'there is none user whose username is ' + username
            })
        import random
        uid.emailcode = str(random.randint(0, 1000000))
        uid.save()
        print(uid.emailcode)
        send_mail('Answer here', 'this is the code for change you password' + uid.emailcode, '1506607292@qq.com',
                  [uid.email], fail_silently=False)
        return JsonResponse({
            'code': 0,
            'message': 'the code have been send to you email'
        })

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        emailcode = data['emailcode']
        if not emailcode:
            return JsonResponse({
                'code': 1,
                'message': 'do not receive emailcode'
            })
        print(emailcode)
        uid = models.User.objects.filter(emailcode=emailcode).first()
        if not uid:
            return JsonResponse({
                'code': 1,
                'message': 'wrong code'
            })
        password = data['password']
        uid.password = password
        uid.emailcode = ''
        uid.save()
        return JsonResponse({
            'code': 0,
            'message': 'change successfully'
        })


class Register(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({
            'code': 0,
            'message': 'register here'
        })

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if data['username'] and data['password']:
            try:
                models.User.objects.create(username=data['username'],
                                           password=data['password'], token='',
                                           phone=data['phone'],
                                           email=data['email'])
                return JsonResponse({
                    'code': 0,
                    'massage': 'Register successfully'
                })
            except Exception as e:
                return JsonResponse({
                    'code': 7,
                    'massage': str(e)
                })
        else:
            return JsonResponse({
                'code': 1,
                'massage': 'None username or password'
            })


class Logout(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({
            'code': 0,
            'message': 'there is nothing to get'
        })

    def post(self, request, *args, **kwargs):
        if request.COOKIES.get('token'):
            info = models.User.objects.filter(token=request.COOKIES.get('token')).first()
            if info:
                models.User.objects.filter(token=request.COOKIES.get('token')).token = ''
                obj = JsonResponse({
                    'code': 0,
                    'message': 'logout successfully'
                })
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
