from .choices import *
from django.db import models


class Card_Info(models.Model):
    card_token = models.CharField(max_length=50, verbose_name="카드토큰")

    oiling_type = models.CharField(choices=TYPE_CHOICES, max_length=10, verbose_name="유종")
    oiling_price = models.CharField(choices=PRICE_CHOICES, max_length=10, verbose_name="금액")

    point_token = models.CharField(max_length=50, verbose_name="포인트카드토큰", null=True, blank=True)

    oiling_receipt = models.CharField(choices=RECEIPT_CHOICES, max_length=10, verbose_name="영수증발행여부")

    def __str__(self):
        return str(self.card_token)
    
    class Meta:
        db_table = "CARDINFO_TB"
        verbose_name = "카드정보"
        verbose_name_plural = "카드정보"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)