from django.db import models
from django.utils import timezone


class Respondent(models.Model):
    sid = models.BigIntegerField()
    name = models.CharField(max_length=32, default=None)
    school = models.CharField(max_length=32, default=None)
    major = models.CharField(max_length=32, default=None)
    classn = models.CharField(max_length=32, default=None)
    sex = models.CharField(max_length=8, default=None)
    phone = models.CharField(max_length=32, default=None)
    email = models.CharField(max_length=64, default=None)
    muid = models.BigIntegerField(default=None)

    class Meta:
        unique_together = ("sid", "muid")


class Page(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=128, blank=True,null=True)
    desc = models.CharField(max_length=128, blank=True,null=True)
    stime = models.DateTimeField('startTime', blank=True,null=True)
    etime = models.DateTimeField('startTime', blank=True,null=True)
    isopen = models.CharField(max_length=8, default=None)
    muid = models.BigIntegerField(default=None)


class Cquestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    index = models.IntegerField(default=None)
    title = models.CharField(max_length=128, default=None)
    desc = models.CharField(max_length=128, default=None)
    need = models.CharField(max_length=8, default=None)
    pid = models.ForeignKey('Page', on_delete=models.CASCADE, default=None)


class Choice(models.Model):  # 问题答案
    id = models.BigAutoField(primary_key=True)
    option = models.CharField(max_length=8, default=None)  # A B C D
    text = models.CharField(max_length=128, default=None)
    score = models.IntegerField(default=1)
    cqid = models.ForeignKey('Cquestion', on_delete=models.CASCADE)


class Fquestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    index = models.IntegerField(default=None)
    title = models.CharField(max_length=128, default=None)
    desc = models.CharField(max_length=128, default=None)
    need = models.CharField(max_length=8, default=None)
    exampleAnswer = models.TextField(max_length=1024, default=None)
    score = models.IntegerField(default=1)
    pid = models.ForeignKey('Page', on_delete=models.CASCADE, default=None)


class Canswer(models.Model):  # 问卷结果
    id = models.BigAutoField(primary_key=True)
    cqid = models.ForeignKey('Cquestion', on_delete=models.CASCADE, default=None)
    option = models.CharField(max_length=8, default=None)  # A B C D
    uid = models.ForeignKey('Respondent', on_delete=models.CASCADE, default=None)
    pid = models.ForeignKey('Page', on_delete=models.CASCADE, default=None)


class Fanswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    fqid = models.ForeignKey('Fquestion', on_delete=models.CASCADE, default=None)
    answer = models.TextField(max_length=1024, default=None)
    uid = models.ForeignKey('Respondent', on_delete=models.CASCADE, default=None)
    pid = models.ForeignKey('Page', on_delete=models.CASCADE, default=None)


class U_P(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=4, default=None)
    pid = models.ForeignKey('Page', on_delete=models.CASCADE, default=None)
    uid = models.ForeignKey('Respondent', on_delete=models.CASCADE, default=None)
    sessionid = models.UUIDField(max_length=64, default=None)
    status = models.CharField(default=None,max_length=16)

    class Meta:
        unique_together = ("pid", "uid")
