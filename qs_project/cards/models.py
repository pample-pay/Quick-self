from .choices import *
from django.db import models
from django.conf import settings


class Card_Info(models.Model):
    card_token = models.CharField(max_length=50, verbose_name="카드토큰")

    oiling_type = models.CharField(choices=TYPE_CHOICES, max_length=10, verbose_name="유종")
    oiling_price = models.CharField(choices=PRICE_CHOICES, max_length=10, verbose_name="금액")

    point_token = models.CharField(max_length=50, verbose_name="포인트카드토큰", null=True, blank=True)

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