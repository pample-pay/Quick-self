from .forms import UserRegisterForm
from .models import User, AuthSMS

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
 

class UserRegisterView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm

    def get_success_url(self):
        messages.success(self.request, "회원가입 성공.")
        return redirect('/')

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())



class AuthView(APIView):

    def post(self, request):
        try:
            p_num = request.data['hp']
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            AuthSMS.objects.update_or_create(hp=p_num)
            return Response({'message': 'OK'})
