from django.urls import path, include
from . import views

app_name = 'cards'

urlpatterns = [
    path('enroll/', views.enroll_view, name='enroll_card_info'),    

    path('api/v1/card-enroll', views.CardEnrollView.as_view(), name='card_enroll'), 

    path('api/v1/card-check', views.CardCheckView.as_view(), name='card_check'), 
    path('api/v1/card-check-enroll', views.CardCheckEnrollView.as_view(), name='card_check_enroll'), 

    path('api/v1/card-delete/<int:pk>', views.CardDelete.as_view(), name='card_delete'), 

    path('enroll/insert', views.insert_card_view, name='insert_card_info'),       
]