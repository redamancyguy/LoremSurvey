import hashlib
import json
import os

from django.http import JsonResponse, HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.views import View
from . import models
from django.core.mail import send_mail


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'template.html', {'info': 'index'})

    def post(self, request, *args, **kwargs):
        return JsonResponse({
            'code': 0,
            'message': "Index test"
        })


class AddUser(View):
    def dispatch(self, request, *args, **kwargs):
        if request.COOKIES.get('token'):
            from user.models import User
            if User.objects.filter(token=request.COOKIES.get('token')).first():
                return super().dispatch(request, *args, **kwargs)
            return JsonResponse({
                'code': 1,
                'message': 'wrong token && please Log in again'
            })
        else:
            obj = JsonResponse({
                'code': 1,
                'message': 'you do not have token,please login'
            })
            # obj.set_cookie('token','eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InN1bndlbmxpMSJ9.YlXoG6W9va_akPZitVYsN8I26tR_y2LpAcNSG2rFUiI')
            return obj

    def get(self, request, *args, **kwargs):
        userlist = []
        token = request.COOKIES.get('token')
        import user.models as u_models
        muid = u_models.User.objects.filter(token=token).first().id
        for i in  models.User.objects.filter(muid=muid):
            userlist.append({'id':i.sid,'name':i.name,'school':i.school,'phone':i.phone,'email':i.email})
        return render(request, 'file.html',{'userlist':userlist})

    def post(self, request, *args, **kwargs):
        files = request.FILES
        if files:
            for i in files:
                file = request.FILES[i]
                if file:
                    f = open('./files/' + i, 'wb')
                    for chunk in file.chunks():
                        f.write(chunk)
                    f.close()
                    import pandas as pd
                    data = pd.read_excel('./files/' + i).values
                    token = request.COOKIES.get('token')
                    import user.models as u_models
                    muid = u_models.User.objects.filter(token=token).first().id
                    if muid:
                        for i in data:
                            models.User.objects.create(sid=i[0], name=i[1], school=i[2],
                                                       major=i[3], classn=i[4], sex=i[5],
                                                       phone=i[6], email=i[7], muid=muid)
                        os.remove('./files/' + i)
                        return JsonResponse({
                            'code': 0,
                            'message': "Received"
                        })
            return JsonResponse({
                'code': 7,
                'message': "File transfer but did not receive"
            })
        else:
            return JsonResponse({
                'code': 7,
                'message': "No file transfer"
            })


class ManageQuestion(View):
    def dispatch(self, request, *args, **kwargs):
        if request.COOKIES.get('token'):
            from user.models import User
            if User.objects.filter(token=request.COOKIES.get('token')).first():
                return super().dispatch(request, *args, **kwargs)
            return JsonResponse({
                'code': 1,
                'message': 'wrong token && please Log in again'
            })
        else:
            return JsonResponse({
                'code': 1,
                'message': 'you do not have token,please login'
            })

    def get(self, request, *args, **kwargs):
        try:
            result = []
            token = request.COOKIES.get('token')
            import user.models as u_models
            muid = u_models.User.objects.filter(token=token).first().id
            print(muid)
            ps = models.Page.objects.filter(muid=muid)
            for i in ps:
                result.append({'title':i.title,'desc':i.desc,'stime':i.stime,'etime':i.etime,'isopen':i.isopen})
            return JsonResponse({
                'code': 0,
                'data': result,
                'message': 'get success'
            })
        except Exception as e:
            return JsonResponse({
                'code': 0,
                'data': str(e),
                'message': 'error'
            })

    def post(self, request, *args, **kwargs):
        print('args', args)
        print('kwargs', kwargs)
        try:
            token = request.COOKIES.get('token')
            import user.models as u_models
            muid = u_models.User.objects.filter(token=token).first().id
            data = json.loads(request.body.decode())
            models.Page.objects.create(title=data['title'], isopen=data['isopen'], desc=data['desc'],
                                       stime=data['stime'], etime=data['etime'],muid=muid)
            pid = models.Page.objects.filter(title=data['title'], desc=data['desc'],
                                             stime=data['stime'], etime=data['etime'])[0]
            for i in data['problemSet']:
                if i['type'] == 1:
                    models.Cquestion.objects.create(index=i['index'], title=i['title'], need=i['need'], pid=pid)
                    cqid = models.Cquestion.objects.filter(title=i['title'], need=i['need'])[0]
                    for j in i['options']:
                        models.Choice.objects.create(option=str(j['value']), text=j['label'], cqid=cqid)
                elif i['type'] == 0:
                    models.Fquestion.objects.create(index=i['index'], need=i['need'], title=i['title'], pid=pid)
        except Exception as e:
            return JsonResponse({
                'code': 0,
                'message': 'Error'+str(e)
            })
        return JsonResponse({
            'code': 0,
            'message': "Receive questions success"
        })

    def delete(self, request, *args, **kwargs):
        print('args', args)
        print('kwargs', kwargs)
        import user.models as u_models
        token = request.COOKIES.get('token')
        muid = u_models.User.objects.filter(token=token).first().id
        print(muid)
        print('title:',request.DELETE.get('title'))
        for i in models.Page.objects.filter(title=request.DELETE.get('title'),muid=muid):
            print(i.id)
            i.delete()
            return JsonResponse({
                'code': 0,
                'message': "Delete questions success"
            })
        return JsonResponse({
        'code': 0,
        'message': "None questions to delete"
    })

    def put(self, request, *args, **kwargs):
        return JsonResponse({
            'code': 1,
            'message': 'Someone has already answered the question, so you can not change the answer'
        })


class Generate(View):
    def post(self, request, *args, **kwargs):
        pageid = request.POST.get('id')
        # 可以在这里确定一下 是生成那张卷纸，对于那些学生 现在默认为所有   change!
        try:
            for i in models.Page.objects.filter(id=pageid):
                if i.isopen == '1':
                    import user.models as u_models
                    token = request.COOKIES.get('token')
                    muid = u_models.User.objects.filter(token=token).first().id
                    for j in models.User.objects.filter(muid=muid):
                        sessionid = hashlib.md5((str(i.id) + str(j.id)).encode('utf-8')).hexdigest()
                        models.U_P.objects.create(type='1', pid=i, uid=j, sessionid=sessionid)
                        print(j.id,j.name,j.email,sessionid)
                        from .tests import sendEmail
                        send_mail('Subject here', 'Here is the message.', '1506607292@qq.com',
                                  ['duanjihang@live.com'], fail_silently=False)
                    return JsonResponse({
                        'code': 0,
                        'message': "Generate Closed source success"
                    })
                elif i.isopen == '0':
                    sessionid = hashlib.md5((str(i.id) + 'open').encode('utf-8')).hexdigest()
                    uid = models.User.objects.filter(id=123456789).first() # 默认都用这个开放用户答题
                    models.U_P.objects.create(type='0', uid=uid, pid=i, sessionid=sessionid)
                    from .tests import sendEmail
                    send_mail('Subject here', 'Here is the message.', '1506607292@qq.com',
                              ['duanjihang@live.com'], fail_silently=False)
                    return JsonResponse({
                        'code': 0,
                        'message': "Generate open source success"
                    })
            return JsonResponse({
                'code': 1,
                'message': "Nothing to generate"
            })
        except Exception as e:
            return JsonResponse({
                'code': 0,
                'message': str(e)
            })


class AnswerQuestion(View):
    def get(self, request, *args, **kwargs):
        sessionid = request.GET.get('sessionid')
        if sessionid:
            try:
                data = {}
                for i in models.U_P.objects.filter(sessionid=sessionid):  # 理论上这个循环就一次
                    for j in models.Page.objects.filter(id=i.pid):
                        print('title', j.title)
                        data['title'] = j.title
                        data['desc'] = j.desc
                        data['stime'] = j.stime
                        data['etime'] = j.etime
                        data['problemSet'] = []
                        for k in models.Cquestion.objects.filter(pid=j.id):
                            options = []
                            question = {'index': k.index, 'type': 1, 'title': k.title, 'need': k.need,
                                        'options': options}
                            for l in models.Choice.objects.filter(cqid=k.id):
                                options.append({"label": l.text, "value": l.option})
                            data['problemSet'].append(question)
                        for k in models.Fquestion.objects.filter(pid=j.id):
                            question = {'index': k.index, 'type': 0, 'title': k.title, 'need': k.need, }
                            data['problemSet'].append(question)
                    return JsonResponse({
                        'code': 0,
                        'data': data,
                        'message': 'send success'
                    })
                return JsonResponse({
                    'code': 1,
                    'message': 'Wrong sessionid'
                })
            except Exception as e:
                return JsonResponse({
                    'code': 1,
                    'message': str(e)
                })

        else:
            return JsonResponse({
                'code': 0,
                'message': 'Give me you sessionid and I will give you the questions'
            })

    def post(self, request, *args, **kwargs):
        return JsonResponse({
            'code':0,
            'message':'is ok'
        })
