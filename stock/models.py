from django.db import models
from config.settings import base

# Create your models here.

#증권사에 보유한 주식에 대한 종목명과 수량에 대한 모델
class Stock(models.Model):

    COMPANY_CHOICES = ((1, '나무'),(2, "KB"))

    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stockname = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    amount = models.IntegerField(default=0)
    company = models.CharField(max_length=1, choices=COMPANY_CHOICES)

#증권사에 대한 고객 아이디와 비밀번호에 대한 모델
class Account(models.Model):
    
    COMPANY_CHOICES = ((1, '나무'),(2, "KB"))
    
    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_id = models.CharField(max_length=255)
    company_secret = models.CharField(max_length=255)
    company = models.CharField(max_length=1, choices=COMPANY_CHOICES)