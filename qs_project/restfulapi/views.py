from cards.models import Card_Info

from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class ReceiveCardsView(APIView):
    '''
    # get POST json API
    {
        "card_token": "123456789000",
        "oiling_type": "0",
        "oiling_price":"1",
        "point_token":"",
        "oiling_receipt":"0"
    }
    '''

    def post(self, request):

        try:
            cpf = request.data

            card_token = cpf['card_token']
            oiling_type = cpf['oiling_type']
            oiling_price = cpf['oiling_price']
            point_token = cpf['point_token']
            oiling_receipt = cpf['oiling_receipt']

            updated_values = {
                'oiling_type' : oiling_type,
                'oiling_price' : oiling_price,
                'point_token' : point_token,
                'oiling_receipt' : oiling_receipt,
            }

        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            Card_Info.objects.update_or_create(
                card_token=card_token,
                defaults=updated_values
                )

            return Response({'message': 'OK'})


class SendCardInfo(APIView):
    '''
    # get POST json API
    {
        "card_token": "123456789000",
    }
    # return POST json API
    {
        "card_token": "123456789000",
        "oiling_type": "0",
        "oiling_price":"1",
        "point_token":"",
        "oiling_receipt":"0"
    }
    '''

    def post(self, request):

        try:
            ct = request.data

            card_token = ct['card_token']
            card_infos = Card_Info.objects.filter(card_token=card_token)

            print(card_infos)


        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:


            return Response({'message': 'OK'})