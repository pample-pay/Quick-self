import os
import hmac
import json
import time
import base64
import random
import datetime
import hashlib
import requests

from .choices import *
from model_utils.models import TimeStampedModel

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone



class UserManager(BaseUserManager):
    def create_user(self, user_id, password, hp, auth, **extra_fields):
        user = self.model(
            user_id = user_id,
            hp = hp,
            auth = auth,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password, hp=None, auth=None):
        user = self.create_user(user_id, password, hp, auth)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.level = 0
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    '''
    회원 정보 테이블, 테이블명 USER_TB
    user_id : 유저 아이디
    password : 비밀번호
    hp : 휴대폰번호
    level : 사용자 권한 등급, 개발자 0, 관리자 1, 유저는 default 2
    auth : 인증번호 6자리
    date_joined : 가입일, auto_now_add 사용
    '''
    
    objects = UserManager()

    user_id = models.CharField(max_length=15, verbose_name="아이디", unique=True)
    password = models.CharField(max_length=256, verbose_name="비밀번호")
    hp = models.CharField(max_length=11, verbose_name="휴대폰번호", null=True, unique=True)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=18, verbose_name="등급", default=2)
    auth = models.CharField(max_length=6, verbose_name="인증번호", null=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['hp']
    
    def __str__(self):
        return self.user_id

    class Meta:
        db_table = "USER_TB"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"


class AuthSMS(TimeStampedModel):
    '''
    회원가입 문자 인증을 위한 model, 테이블명 AUTH_TB
    네이버 sens 서비스를 통해 입력한 휴대폰 번호로 인증 번호를 보냅니다.
    인증 코드는 6자리 숫자입니다.
    '''
    hp = models.CharField(max_length=11, verbose_name='휴대폰번호', primary_key=True)
    auth = models.IntegerField(verbose_name='인증번호')

    class Meta:
        db_table = 'AUTH_TB'

    def save(self, *args, **kwargs):
        self.auth = random.randint(100000, 1000000) # 난수로 6자리 문자 인증 번호 생성
        super().save(*args, **kwargs)
        self.send_sms() # 문자 전송용 함수

    def send_sms(self):

        BASE_DIR = getattr(settings, 'BASE_DIR', None)
        file_path = "naver_cloud_sens.json" # 네이버 sens api key 파일

        with open(os.path.join(BASE_DIR,file_path), encoding='utf-8') as f:
            nc_sens_key = json.load(f)

        ##### 네이버 sens 서비스 이용 위한 json request 형식 #####
        timestamp = str(int(time.time() * 1000))

        url = "https://sens.apigw.ntruss.com"
        uri = "/sms/v2/services/ncp:sms:kr:299525032760:test/messages"
        apiUrl = url + uri

        access_key = nc_sens_key['NAVER_SENS_ACCESS_KEY']
        secret_key = bytes(nc_sens_key['NAVER_SENS_SECRET_KEY'], 'UTF-8')
        message = bytes("POST" + " " + uri + "\n" + timestamp + "\n" + access_key, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        

        body = {
            "type" : "SMS",
            "contentType" : "COMM",
            "from" : "01089833328",
            "subject" : "subject",
            "content" : "[퀵셀프] 인증 번호 [{}]를 입력해주세요.".format(self.auth),
            "messages" : [{"to" : self.hp}]
        }
        body2 = json.dumps(body)
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": access_key,
            "x-ncp-apigw-signature-v2": signingKey
        }

        requests.post(apiUrl, headers=headers, data=body2)


    @classmethod
    def check_timer(cls, p_num, c_num)->bool:
        '''
        문자인증 제한시간을 위한 타이머 설정 함수
        '''
        time_limit = timezone.now() - datetime.timedelta(minutes=5) # minutes 변수를 통해 문자인증 제한시간 설정
        result = cls.objects.filter(
            hp=p_num,
            auth=c_num,
            modified__gte=time_limit
        )

        if result:
            return True
        return False
