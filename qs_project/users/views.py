from .forms import UserRegisterForm
from .models import User, AuthSMS
from .modules import check_auth, register_errors

from django.shortcuts import render, redirect
from django.views.generic import CreateView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


BASE_URL = '/'
KAKAO_CALLBACK_URI = BASE_URL + 'kakao/callback/'
NAVER_CALLBACK_URI = BASE_URL + 'naver/callback/'



def index_view(request):
    return render(request, 'users/index.html')


class UserRegisterView(CreateView):
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



class AuthView(APIView):

    def post(self, request):
        try:
            p_num = request.data['hp']
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            AuthSMS.objects.update_or_create(hp=p_num)
            return Response({'message': 'OK'})
