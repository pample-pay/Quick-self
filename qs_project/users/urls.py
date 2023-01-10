from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('api/example', views.AuthView.as_view(), name='example'), 
]