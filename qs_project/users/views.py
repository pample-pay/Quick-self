from .forms import UserRegisterForm, LoginForm
from .models import User, AuthSMS
from .modules import check_auth, register_errors

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.decorators import *



### 소셜 로그인 사용 위한 url 변수 설정 ###
BASE_URL = '/'
KAKAO_CALLBACK_URI = BASE_URL + 'kakao/callback/'
NAVER_CALLBACK_URI = BASE_URL + 'naver/callback/'


def logout_view(request):
    logout(request)
    return redirect('/')


# @method_decorator(logout_message_required, name='dispatch')
class LoginView(FormView):
    '''
    메인 페이지 view
    로그인 위한 form request 
    '''
    template_name = 'users/index.html'
    form_class = LoginForm
    success_url = '/'


    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=user_id, password=password)

        if user is not None:
            self.request.session['user_id'] = user_id
            login(self.request, user)

        return super().form_valid(form)

    def form_invalid(self, form: LoginForm):
        messages.error(self.request, '아이디 또는 비밀번호를 확인해주세요.')
        return super().form_invalid(form)



class UserRegisterView(CreateView):
    '''
    회원가입 페이지 view
    register_errors 함수를 통해 에러메세지 전달
    check_auth 함수를 통해 휴대폰번호, 인증번호 매칭
    에러메세지 없을시 form 저장하고 메인페이지로 redirect
    '''
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm

    def form_valid(self, form):
        user_hp = form.cleaned_data['hp']
        user_auth = form.cleaned_data['auth']

        if check_auth(user_hp, user_auth) == True:
            errors = register_errors(form)

            if errors == {}:
                self.object = form.save()
                return redirect('/')
            else:
                return self.render_to_response(self.get_context_data(form=form, errors=errors))

        else:
            errors = register_errors(form)
            return self.render_to_response(self.get_context_data(form=form, errors=errors))
    
    def form_invalid(self, form):
        errors = register_errors(form)
        return self.render_to_response(self.get_context_data(form=form, errors=errors))



# For API views
class AuthView(APIView):
    '''
    받은 request data로 휴대폰번호를 통해 AuthSMS에 update_or_create
    인증번호 난수 생성및 저장은 모델 안에 존재.
    '''
    def post(self, request):
        try:
            p_num = request.data['hp']
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            AuthSMS.objects.update_or_create(hp=p_num)
            return Response({'message': 'OK'})
