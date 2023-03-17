from .choices import *
from django.db import models
from django.conf import settings


class Card_Info(models.Model):
    card_token = models.CharField(max_length=256, verbose_name="카드토큰")

    card_uniq = models.CharField(max_length=10, verbose_name="카드구분", default='None')
    card_nickname = models.CharField(max_length=10, verbose_name="카드닉네임", default='None')

    oiling_type = models.CharField(choices=TYPE_CHOICES, max_length=10, verbose_name="유종")
    oiling_price = models.CharField(choices=PRICE_CHOICES, max_length=10, verbose_name="금액")

    point_number = models.CharField(max_length=50, verbose_name="포인트카드번호", null=True, blank=True)

    oiling_receipt = models.CharField(choices=RECEIPT_CHOICES, max_length=10, verbose_name="영수증발행여부", default=0)

    def __str__(self):
        return str(self.card_token)
    
    class Meta:
        db_table = "CARDINFO_TB"
        verbose_name = "카드정보"
        verbose_name_plural = "카드정보"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class User_Card(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='아이디')
    card_token = models.ForeignKey(Card_Info, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        db_table = "USERCARD_TB"
        verbose_name = "유저카드"
        verbose_name_plural = "유저카드"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Card_Receipt(models.Model):
    """
    Foreign key로 받지 않는 이유는, Card_Info는 변동 가능성이 있기 때문에.
    따라서 pos기에서 날아오는 결제 정보를 별도로 저장하는 테이블.
    """

    card_token = models.CharField(max_length=256, verbose_name="카드토큰")
    card_uniq = models.CharField(max_length=10, verbose_name="카드구분", default='None')

    oiling_type = models.CharField(choices=TYPE_CHOICES, max_length=10, verbose_name="유종")
    oiling_price = models.CharField(choices=PRICE_CHOICES, max_length=10, verbose_name="금액")
    point_number = models.CharField(max_length=50, verbose_name="포인트카드번호", null=True, blank=True)
    oiling_receipt = models.CharField(choices=RECEIPT_CHOICES, max_length=10, verbose_name="영수증발행여부", default=0)

    gs_code = models.CharField(max_length=50, verbose_name="주유소코드", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.card_token)
    
    class Meta:
        db_table = "CARDRECEIPT_TB"
        verbose_name = "결제내역"
        verbose_name_plural = "결제내역"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)