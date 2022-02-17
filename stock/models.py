from django.db import models
from config.settings import base


# 증권사에 보유한 주식에 대한 종목명과 수량에 대한 모델
class Stock(models.Model):

    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stockname = models.CharField(max_length=50)
    code = models.CharField(max_length=6)
    amount = models.IntegerField(default=0)
    company = models.CharField(max_length=10)
    outstandingShare = models.IntegerField(default=0)


# 증권사에 대한 고객 아이디와 비밀번호에 대한 모델
class Account(models.Model):

    COMPANY_CHOICES = ((1, "나무"), (2, "KB"))

    user = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_id = models.CharField(max_length=255)
    company_secret = models.CharField(max_length=255)
    company = models.CharField(max_length=1, choices=COMPANY_CHOICES)


# 증권사 리서치 자료에 대한 모델
class Research(models.Model):

    code = models.CharField(max_length=6)
    title = models.CharField(db_index=True, max_length=200, verbose_name="제목")
    writer = models.CharField(max_length=10, verbose_name="작성자")
    link = models.URLField(max_length=500)
    day = models.DateField(verbose_name="작성일")
    company = models.CharField(max_length=10)
    documentid = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return (
            "종목 : "
            + self.code
            + ", 제목: "
            + self.title
            + ", 작성자: "
            + self.writer
            + ", 회사: "
            + self.company
        )
