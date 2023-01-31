from django.urls import path, include
from . import views

app_name = 'restfulapip'

urlpatterns = [
    path('api/v1/receive-cards', views.ReceiveCardsView.as_view(), name='receive_cards'), 
    path('api/v1/send-card-info', views.SendCardInfo.as_view(), name='send_card_info'), 
]