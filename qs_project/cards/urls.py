from django.urls import path, include
from . import views

app_name = 'cards'

urlpatterns = [
    path('enroll/', views.enroll_view, name='enroll_card_info'),
    path('api/v1/card-enroll', views.CardEnrollView.as_view(), name='card_enroll'), 
]