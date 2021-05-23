# _*_ coding: utf-8 _*_
import json
import os
import random
from io import BytesIO

from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
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
                obj['Access-Control-Allow-Origin'] = '*'
                obj['Access-Control-Allow-Headers'] = "content-type"
                obj['Access-Control-Allow-Methods'] = "DELETE,PUT,GET,POST"
                # obj.set_cookie('token', token, max_age=3600,httponly=True,secure=True,samesite='None')
                obj.set_cookie('token', token, max_age=3600)
                obj.set_cookie('username', info.username, max_age=3600)
                return obj
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

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data['username']
        if not username:
            return JsonResponse({
                'code': 2,
                'message': 'I do not know your username'
            })
        uid = models.User.objects.filter(username=username).first()
        if not uid:
            return JsonResponse({
                'code': 2,
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
                'code': 2,
                'message': 'do not receive emailcode'
            })
        uid = models.User.objects.filter(emailcode=emailcode).first()
        if not uid:
            return JsonResponse({
                'code': 2,
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
                                           email=data['email'], emailcode='')
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


from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw


def generate_code():
    source = "0123456789qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM"
    code = ""
    for i in range(4):
        code += random.choice(source)
    return code


def getCAPTCHA(request):
    mode = "RGB"  # 颜色模式
    size = (200, 100)  # 画布大小

    red = random.randrange(255)
    green = random.randrange(255)
    blue = random.randrange(255)
    color_bg = (red, green, blue)  # 背景色

    image = Image.new(mode=mode, size=size, color=color_bg)  # 画布
    imagedraw = ImageDraw(image, mode=mode)  # 画笔
    verify_code = generate_code()  # 内容
    imagefont = ImageFont.truetype(os.getcwd() + '/files/Roboto-Regular.ttf', 100)
    # 字体 颜色
    for i in range(len(verify_code)):
        fill = (random.randrange(255), random.randrange(255), random.randrange(255))
        imagedraw.text(xy=(50 * i, 0), text=verify_code[i], fill=fill, font=imagefont)
    # 噪点
    for i in range(1000):
        fill = (random.randrange(255), random.randrange(255), random.randrange(255))
        xy = (random.randrange(201), random.randrange(100))
        imagedraw.point(xy=xy, fill=fill)
    fp = BytesIO()
    image.save(fp, 'png')
    id = models.CAPTCHA.objects.create(content=verify_code)
    with open(os.getcwd() + '/static/files/'+str(id.id)+'.png','wb') as f:
        f.write(fp.getvalue())
    return JsonResponse({
        'code':0,
        'message':'generate captcha success',
        'data':{'url':'/static/files/'+str(id.id)+'.png'}
    })
