# _*_ coding: utf-8 _*_
import json
import os
import random
from io import BytesIO
import base64
from django.core.mail import send_mail
from django.forms import Form, fields
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from . import models
from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw


class Index(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Index')

    def post(self, request, *args, **kwargs):
        return HttpResponse('Index')


class LoginForm(Form):
    username = fields.CharField(min_length=8, max_length=32, required=True, error_messages={
        'required': 'can not be null',
        'min_length': 'too short'
    })
    password = fields.CharField(min_length=8, max_length=128, required=True)


class Login(View):

    @staticmethod
    def get(request, *args, **kwargs):
        return HttpResponse('Login')

    @staticmethod
    def post(request, *args, **kwargs):
        data = json.loads(request.body)
        if data['username'] and data['password']:
            print(request.POST)
            # obj = LoginForm(request.POST)
            obj = LoginForm(data)
            if obj.is_valid():
                print(obj.cleaned_data)
            else:
                print(obj.errors)
            item = models.User.objects.filter(username=data['username'],
                                              password=data['password']).first()
            if item:
                import jwt
                key = 'LoremSurvey'
                payload = {'username': item.username}
                token = jwt.encode(payload, key, algorithm='HS256')
                # data2 = jwt.decode(token, key, algorithms='HS256')
                item.token = token
                item.save()
                response = JsonResponse({
                    'code': 0,
                    'message': 'login successfully'
                })
                response.set_cookie('token', token, max_age=1800)
                response.set_cookie('username', data['username'])
                return response
            else:
                return JsonResponse({
                    'code': 2,
                    'message': 'wrong username or password'
                })
        return JsonResponse({
            'code': 2,
            'message': 'Nothing input !'
        })


class ChangePassword(View):

    @staticmethod
    def post(request, *args, **kwargs):
        data = json.loads(request.body)
        if not data['username']:
            return JsonResponse({
                'code': 2,
                'message': 'I do not know your username'
            })
        uid = models.User.objects.filter(username=data['username']).first()
        if not uid:
            return JsonResponse({
                'code': 2,
                'message': 'there is none user whose username is ' + data['username']
            })
        import random
        uid.emailcode = str(random.randint(0, 1000000))
        uid.save()
        send_mail('Your Code for CHANGING PASSWORD', 'this is the code for change you password' + uid.emailcode,
                  '1506607292@qq.com',
                  [uid.email], fail_silently=False)
        return JsonResponse({
            'code': 0,
            'message': 'the code have been send to you email'
        })

    @staticmethod
    def put(request, *args, **kwargs):
        data = json.loads(request.body)
        if not data['emailCode']:
            return JsonResponse({
                'code': 2,
                'message': 'do not receive emailCode'
            })
        uid = models.User.objects.filter(emailCode=data['emailCode']).first()
        if not uid:
            return JsonResponse({
                'code': 2,
                'message': 'wrong code'
            })
        uid.password = data['password']
        uid.emailCode = ''
        uid.save()
        return JsonResponse({
            'code': 0,
            'message': 'change successfully'
        })


class Register(View):

    @staticmethod
    def get(request, *args, **kwargs):
        return JsonResponse({
            'code': 0,
            'message': 'register here'
        })

    @staticmethod
    def post(request, *args, **kwargs):
        data = json.loads(request.body)
        if data['username'] and data['password']:
            try:
                models.User.objects.create(username=data['username'],
                                           password=data['password'], token='',
                                           phone=data['phone'],
                                           email=data['email'], emailCode='')
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
                'code': 2,
                'massage': 'None username or password'
            })


class Logout(View):

    @staticmethod
    def get(request, *args, **kwargs):
        return JsonResponse({
            'code': 0,
            'message': 'there is nothing to get'
        })

    @staticmethod
    def post(request, *args, **kwargs):
        if request.COOKIES.get('token'):
            info = models.User.objects.filter(token=request.COOKIES.get('token')).first()
            if info:
                models.User.objects.filter(token=request.COOKIES.get('token')).token = ''
                obj = JsonResponse({
                    'code': 0,
                    'message': 'logout successfully'
                })
                obj.delete_cookie('token')
                return obj
            else:
                return JsonResponse({
                    'code': 2,
                    'massage': 'wrong token'
                })
        return JsonResponse({
            'code': 2,
            'massage': 'Nothing input !'
        })


def generateCode():
    source = '0123456789qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM'
    code = ''
    for i in range(4):
        code += random.choice(source)
    return code


def getCAPTCHA(request):
    mode = 'RGB'
    size = (200, 100)
    red = random.randrange(255)
    green = random.randrange(255)
    blue = random.randrange(255)
    color_bg = (red, green, blue)
    image = Image.new(mode=mode, size=size, color=color_bg)
    imageDraw = ImageDraw(image, mode=mode)
    verify_code = generateCode()  # 内容
    imageFont = ImageFont.truetype(os.getcwd() + '/files/Roboto-Regular.ttf', 100)
    for i, item in enumerate(verify_code):
        fill = (random.randrange(255), random.randrange(255), random.randrange(255))
        imageDraw.text(xy=(50 * i, 0), text=item, fill=fill, font=imageFont)
    for i in range(1000):
        fill = (random.randrange(255), random.randrange(255), random.randrange(255))
        xy = (random.randrange(201), random.randrange(100))
        imageDraw.point(xy=xy, fill=fill)
    fp = BytesIO()
    image.save(fp, 'png')
    base64Data = base64.b64encode(fp.getvalue())
    print(base64Data)
    # id =models.CAPTCHA.objects.create(content=verify_code).id
    return JsonResponse({
        'code': 0,
        'message': 'generate captcha success',
        'data': {'id': 'id',
                 'base64Data': str(base64Data, encoding='utf-8')}
    })
