from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index_view, name='index_view'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('api/v1/auth-message', views.AuthView.as_view(), name='auth_message'), 
]