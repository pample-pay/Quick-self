from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('api/auth-message', views.AuthView.as_view(), name='auth_message'), 
]