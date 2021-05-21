import hashlib
import json
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from . import models
from django.core.mail import send_mail


def timeCompare(ormTime):
    from datetime import datetime
    if ormTime.year > datetime.now().year:
        return True
    elif ormTime.year == datetime.now().year:
        if ormTime.month > datetime.now().month:
            return True
        elif ormTime.month == datetime.now().month:
            if ormTime.day > datetime.now().day:
                return True
            elif ormTime.day == datetime.now().day:
                if ormTime.hour > datetime.now().hour:
                    return True
                elif ormTime.hour == datetime.now().hour:
                    if ormTime.minute > datetime.now().minute:
                        return True
                    elif ormTime.minute == datetime.now().minute:
                        if ormTime.second > datetime.now().second:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'template.html', {'info': 'index'})

    def post(self, request, *args, **kwargs):
        return JsonResponse({
            'code': 0,
            'message': "Index test"
        })


class ControlView(object):
    def dispatch(self, request, *args, **kwargs):
        if request.COOKIES.get('token'):
            from user import models as u_model
            if u_model.User.objects.filter(token=request.COOKIES.get('token')).first():
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


class Respondents(ControlView, View):
    def get(self, request, *args, **kwargs):
        userlist = []
        token = request.COOKIES.get('token')
        for i in models.Respondent.objects.filter(muid__token=token):
            userlist.append(
                {'id': i.sid, 'name': i.name, 'school': i.school, 'phone': i.phone, 'email': i.email, 'sex': i.sex})
        return JsonResponse({
            'code': 0,
            'data': userlist,
            'message': 'user list'
        })

    def post(self, request, *args, **kwargs):
        files = request.FILES
        if files:
            try:
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
                        muid = u_models.User.objects.filter(token=token).first()
                        for ii in data:
                            models.Respondent.objects.update_or_create(sid=ii[0], muid = muid, defaults={
                                'name': ii[1], 'school': ii[2],
                                'major': ii[3], 'classn': ii[4], 'sex': ii[5],
                                'phone': ii[6], 'email':    ii[7],
                            })
                        os.remove('./files/' + i)
                        return JsonResponse({
                            'code': 0,
                            'message': "Received"
                        })
            except Exception as e:
                return JsonResponse({
                    'code': 7,
                    'message': str(e)
                })
            return JsonResponse({
                'code': 2,
                'message': "File transfer but did not receive"
            })
        else:
            return JsonResponse({
                'code': 2,
                'message': "No file transfer"
            })

    def delete(self, request, *args, **kwargs):
        try:
            for i in json.loads(request.body):
                models.Respondent.objects.filter(sid=i).delete()
            return JsonResponse({
                'code': 0,
                'message': "delete successfully"
            })
        except Exception as e:
            return JsonResponse({
                'code': 7,
                'message': str(e),
            })

    def put(self, request, *args, **kwargs):
        return JsonResponse({
            'code': 2,
            'message': "None questions to delete"
        })


class ManageQuestion(ControlView, View):
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        if id is None:
            try:
                result = []
                token = request.COOKIES.get('token')
                ps = models.Page.objects.filter(muid__token=token)
                for i in ps:
                    status = None
                    if i.stime == None:
                        result.append(
                            {'id': i.id, 'title': i.title, 'desc': i.desc, 'stime': i.stime, 'etime': i.etime,
                             'emailTemplate': i.emailTemplate, 'isrunning': i.isrunning,
                             'isopen': i.isopen, 'status': status})
                        continue
                    if timeCompare(i.stime):
                        status = '-1'
                    elif not timeCompare(i.etime):
                        status = '1'
                    else:
                        status = '0'
                    result.append(
                        {'id': i.id, 'title': i.title, 'desc': i.desc, 'stime': i.stime, 'etime': i.etime,
                         'emailTemplate': i.emailTemplate, 'isrunning': i.isrunning,
                         'isopen': i.isopen, 'status': status})
                return JsonResponse({
                    'code': 0,
                    'data': result,
                    'message': 'get success'
                })
            except Exception as e:
                return JsonResponse({
                    'code': 7,
                    'message': str(e)
                })
        else:
            rdata = {}
            try:
                j = models.Page.objects.filter(id=id).first()
                if j is None:
                    return JsonResponse({
                        'code': 0,
                        'message': 'None question page id is :' + request.GET.get('id')
                    })
                rdata['title'] = j.title
                rdata['isopen'] = j.isopen
                rdata['desc'] = j.desc
                rdata['stime'] = j.stime
                rdata['etime'] = j.etime
                rdata['isrunning'] = j.isrunning
                rdata['emailTemplate'] = j.emailTemplate
                rdata['problemSet'] = []
                for k in models.Cquestion.objects.filter(pid=j.id):
                    options = []
                    question = {'index': k.index, 'type': 1, 'title': k.title, 'desc': k.desc, 'need': k.need,
                                'options': options}
                    for l in models.Choice.objects.filter(cqid=k.id):
                        if l.option != '#':
                            options.append({"label": l.text, "value": l.option})
                    rdata['problemSet'].append(question)
                for k in models.Fquestion.objects.filter(pid=j.id):
                    question = {'index': k.index, 'type': 0, 'title': k.title, 'desc': k.desc, 'need': k.need, }
                    rdata['problemSet'].append(question)
                return JsonResponse({
                    'code': 0,
                    'data': rdata,
                    'message': 'send success'
                })
            except Exception as e:
                return JsonResponse({
                    'code': 7,
                    'message': str(e),
                })

    def post(self, request, *args, **kwargs):
        try:
            token = request.COOKIES.get('token')
            data = json.loads(request.body.decode())
            import user.models as u_models
            muid = u_models.User.objects.filter(token=token).first()
            pid = models.Page.objects.create(title=data['title'], isopen=data['isopen'], desc=data['desc'],
                                             emailTemplate=data['emailTemplate'], isrunning=data['isrunning'],
                                             stime=data['stime'], etime=data['etime'], muid = muid)
            for i in data['problemSet']:
                if i['type'] == 1:
                    cqid = models.Cquestion.objects.create(index=i['index'], title=i['title'], need=i['need'], pid=pid,
                                                           desc=i['desc'])
                    for j in i['options']:
                        models.Choice.objects.create(option=str(j['value']), text=j['label'], cqid=cqid)
                    models.Choice.objects.create(option='#', text='others', cqid=cqid)
                elif i['type'] == 0:
                    models.Fquestion.objects.create(index=i['index'], need=i['need'], title=i['title'], pid=pid,
                                                    desc=i['desc'])
        except Exception as e:
            return JsonResponse({
                'code': 7,
                'message': str(e)
            })
        return JsonResponse({
            'code': 0,
            'message': "Receive questions success",
            'data': {'id': pid.id}
        })

    def delete(self, request, *args, **kwargs):
        token = request.COOKIES.get('token')
        data = json.loads(request.body)
        for i in models.Page.objects.filter(id=data['id'], muid__token=token):
            i.delete()
            return JsonResponse({
                'code': 0,
                'message': "Delete questions success"
            })
        return JsonResponse({
            'code': 2,
            'message': "None questions to delete"
        })

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        token = request.COOKIES.get('token')
        import user.models as u_models
        muid = u_models.User.objects.filter(token=token).first()
        id = data['id']
        data = json.loads(request.body.decode())
        try:
            pid = models.Page.objects.update_or_create(id=id, defaults={
                'title': data['title'], 'isopen': data['isopen'],
                'desc': data['desc'],
                'emailTemplate': data['emailTemplate'], 'isrunning': data['isrunning'],
                'stime': data['stime'], 'etime': data['etime'], 'muid': muid, 'id': id,
            })
            pid = pid[0]
            for i in pid.fquestion_set.all():
                i.delete()
            for i in pid.cquestion_set.all():
                i.delete()
            try:
                for i in data['problemSet']:
                    if i['type'] == 1:
                        cqid = models.Cquestion.objects.create(pid=pid, index=i['index'], title=i['title'],
                                                               need=i['need'], desc=i['desc'], )
                        for j in i['options']:
                            models.Choice.objects.create(cqid=cqid, option=str(j['value']), text=j['label'])
                    elif i['type'] == 0:
                        models.Fquestion.objects.create(pid=pid, index=i['index'], need=i['need'], title=i['title'],
                                                        desc=i['desc'])
            except Exception as e:
                return JsonResponse({
                    'code': 7,
                    'message': 'something wrong with problemSet ' + str(e)
                })
        except Exception as e:
            return JsonResponse({
                'code': 7,
                'message': 'something wrong with your question page ' + str(e)
            })
        return JsonResponse({
            'code': 0,
            'message': 'the page ' + str(data['title']) + ' is changed'
        })


class Generate(ControlView, View):
    def get(self, request, *args, **kwargs):
        try:
            pid = request.GET.get('id')
            userlist = []
            token = request.COOKIES.get('token')
            for i in models.Respondent.objects.filter(muid__token=token).exclude(sid=123456789):
                status = 0
                if models.U_P.objects.filter(pid_id=pid, uid=i).first():
                    status = 1
                userlist.append(
                    {'id': i.sid, 'name': i.name, 'school': i.school, 'phone': i.phone, 'email': i.email, 'sex': i.sex,
                     'status': status})
            return JsonResponse({
                'code': 0,
                'data': userlist,
                'message': 'respondentsList'
            })
        except Exception as e:
            return JsonResponse({
                'code': 0,
                'message': str(e)
            })

    def post(self, request, *args, **kwargs):

        global sessionid
        data = json.loads(request.body)
        pageid = data['id']
        userList = data['userlist']
        # 可以在这里确定一下 是生成那张卷纸，对于那些学生 现在默认为所有   change!
        try:
            for i in models.Page.objects.filter(id=pageid):
                if i.isopen is False:
                    token = request.COOKIES.get('token')
                    flag = False
                    for j in models.Respondent.objects.filter(muid__token=token):
                        if j.sid not in userList:
                            continue
                        flag = True
                        sessionid = hashlib.md5((str(i.id) + str(j.id)).encode('utf-8')).hexdigest()
                        try:
                            models.U_P.objects.create(pid=i, uid=j, sessionid=sessionid, status='0')
                            from .tests import sendEmail
                            send_mail('Answer your question here',
                                      i.emailTemplate + '    http://1506607292.top/survey/' + sessionid,
                                      '1506607292@qq.com',
                                      [j.email], fail_silently=False)
                        except Exception as e:
                            print('error:', e)
                    if flag is False:
                        return JsonResponse({
                            'code': 2,
                            'message': "None people to generate",
                        })
                    return JsonResponse({
                        'code': 0,
                        'message': "Generate Closed source success",
                    })
                elif i.isopen is True:
                    try:
                        token = request.COOKIES.get('token')
                        import user.models as u_models
                        muid = u_models.User.objects.filter(token=token).first()
                        models.Respondent.objects.create(sid=123456789, name='anonymous', muid = muid, school='',
                                                         major='',
                                                         classn='', phone='', email='', sex='')
                    except Exception as e:
                        print('error:', e)
                    uid = models.Respondent.objects.filter(sid=123456789).first()  # 默认都用这个开放用户答题
                    sessionid = hashlib.md5((str(i.id) + '123456789').encode('utf-8')).hexdigest()
                    models.U_P.objects.create(uid=uid, pid=i, sessionid=sessionid)
                    token = request.COOKIES.get('token')
                    send_mail('Answer here', i.emailTemplate + '      http://1506607292.top/survey/' + sessionid,
                              '1506607292@qq.com',
                              [j.email for j in models.Respondent.objects.filter(muid__token=token)] + [i.muid.email],
                              fail_silently=False)
                    return JsonResponse({
                        'code': 0,
                        'message': "Generate open source success",
                        'data': {'link': 'http://1506607292.top/survey/' + sessionid}
                    })
            return JsonResponse({
                'code': 2,
                'message': "Nothing to generate"
            })
        except Exception as e:
            return JsonResponse({
                'code': 7,
                'message': str(e)
            })


class AnswerQuestion(View):
    def get(self, request, *args, **kwargs):
        sessionid = request.GET.get('sessionid')
        if sessionid:
            try:
                data = {}
                i = models.U_P.objects.filter(sessionid=sessionid).first()
                if not i:
                    return JsonResponse({
                        'code': 2,
                        'data': {'statusCode': 105},
                        'message': "Invalid sessionid"
                    })
                if i.status is True:
                    return JsonResponse({
                        'code': 2,
                        'data': {'statusCode': 104},
                        'message': 'you have answer this question'
                    })
                j = i.pid
                data['title'] = j.title
                data['isopen'] = j.isopen
                data['desc'] = j.desc
                data['stime'] = j.stime
                data['etime'] = j.etime
                data['emailTemplate'] = j.emailTemplate
                data['isrunning'] = j.isrunning
                data['problemSet'] = []
                if data['isrunning'] is False:
                    return JsonResponse({
                        'code': 2,
                        'data': {'statusCode': 100},
                        'message': 'is not running'
                    })
                if j.etime is not None or j.stime is not None:
                    if not timeCompare(j.etime):
                        return JsonResponse({
                            'code': 2,
                            'data': {'statusCode': 101},
                            'message': 'The questionnaire time is over'
                        })
                    if timeCompare(j.stime):
                        return JsonResponse({
                            'code': 2,
                            'data': {'statusCode': 102},
                            'message': 'The questionnaire has not started yet'
                        })
                for k in models.Cquestion.objects.filter(pid=j.id):
                    options = []
                    question = {'index': k.index, 'type': 1, 'title': k.title, 'need': k.need,
                                'options': options}
                    for l in models.Choice.objects.filter(cqid=k.id):
                        if l.option != '#':
                            options.append({"label": l.text, "value": l.option})
                    data['problemSet'].append(question)
                for k in models.Fquestion.objects.filter(pid=j.id):
                    question = {'index': k.index, 'type': 0, 'title': k.title, 'need': k.need, }
                    data['problemSet'].append(question)
                data['statusCode'] = 103
                return JsonResponse({
                    'code': 0,
                    'data': data,
                    'message': 'send success'
                })
            except Exception as e:
                return JsonResponse({
                    'code': 7,
                    'message': str(e)
                })
        else:
            return JsonResponse({
                'code': 2,
                'message': 'Give me you sessionid and I will give you the questions'
            })

    def post(self, request, *args, **kwargs):
        sessionid = request.GET.get('sessionid')
        data = json.loads(request.body.decode())
        u_q_id = models.U_P.objects.filter(sessionid=sessionid).first()
        if not u_q_id:
            return JsonResponse({  # 'Invalid sessionid'
                'code': 2,
                'message': 'Invalid sessionid'
            })
        pid = u_q_id.pid
        uid = u_q_id.uid
        if pid:
            for i in data['problemSet']:
                for j in models.Cquestion.objects.filter(index=i['index'], pid=pid):
                    models.Canswer.objects.create(cqid=j, option=i['option'], uid=uid, pid=pid)
                for j in models.Fquestion.objects.filter(index=i['index'], pid=pid):
                    models.Fanswer.objects.create(fqid=j, answer=i['answer'], uid=uid, pid=pid)
            item = models.U_P.objects.filter(sessionid=sessionid).first()
            item.status = True
            item.save()
            return JsonResponse({
                'code': 0,
                'message': 'Submit successfully'
            })
        return JsonResponse({
            'code': 2,
            'message': 'Invalid sessionid'
        })


class QuestionResult(ControlView, View):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES.get('token')
        try:
            result = []
            for pid in models.Page.objects.filter(muid__token=token):
                global ii
                ii = 0
                page = {}
                for cqid in models.Cquestion.objects.filter(pid=pid):
                    cquestion = {"title": cqid.title}
                    cquestion['option'] = {}
                    for cid in models.Choice.objects.filter(cqid=cqid):
                        cquestion['option'][cid.text] = models.Canswer.objects.filter(option=cid.option,
                                                                                      cqid=cqid).count()
                    ii += 1
                    page['question' + str(ii)] = cquestion
                for fqid in models.Fquestion.objects.filter(pid=pid):
                    fquestion = {'title': fqid.title}
                    answer = []
                    for faid in models.Fanswer.objects.filter(fqid=fqid):
                        answer.append(faid.answer)
                    fquestion['answers'] = answer
                    ii += 1
                    page['question' + str(ii)] = fquestion
                result.append(page)
                ii = 0
            return JsonResponse({
                'code': 0,
                'message': 'get it',
                'data': result
            })
        except Exception as e:
            return JsonResponse({
                'code': 7,
                'message': str(e)
            })

    def post(self, request, *args, **kwargs):
        return JsonResponse({
            'code': 0,
            'message': 'You can get result here'
        })
