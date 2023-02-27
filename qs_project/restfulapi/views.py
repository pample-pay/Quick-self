import modules

from .permissions import *
from cards.models import Card_Info

from django.http import HttpResponse 

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class ReceiveCardsView(APIView):

    '''
    # get POST json API
    {
        "card" : "1234123412341234",
        "oiling_type" : "0",
        "oiling_price" : "0",
        "point_number" : "1234123412341234",
        "oiling_receipt" :"0"
    }
    '''

    permission_classes = [IPBasedPermission]

    def post(self, request):

        try:
            # received json data
            rvd_jd = request.data

            card_num = rvd_jd['card']

            ################### 카드 토큰 39, 5자리 ###################
            card_token39, card_token05 = modules.get_token(card_num)
            ########################################################

            updated_values = {
                    'card_uniq' : card_token05[5:9],
                    'card_nickname' : card_token05[5:9],
                    'oiling_type' : rvd_jd['oiling_type'],
                    'oiling_price' : rvd_jd['oiling_price'],
                    'point_number' : rvd_jd['point_number'],
                    'oiling_receipt' : rvd_jd['oiling_receipt'],
            }


        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            Card_Info.objects.update_or_create(
                card_token = (card_token39+card_token05[:5]).decode(),
                defaults = updated_values
            )
            return HttpResponse({'message': 'Success'})
        


class SendCardInfo(APIView):

    '''
    # get POST json API
    {
        "card": "1234123412341234"
    }
    # return POST json API
    {
        "card_token": "00000000000000000000000000000000000000000000",
        "oiling_type": "0",
        "oiling_price":"0",
        "point_token":"1234123412341234",
        "oiling_receipt":"0"
    }
    '''

    permission_classes = [IPBasedPermission]

    def post(self, request):

        try:
            # received json data
            rvd_jd = request.data

            card_num = rvd_jd['card']

            ################### 카드 토큰 39, 5자리 ###################
            card_token39, card_token05 = modules.get_token(card_num)
            ########################################################

            try:
                card_infos = Card_Info.objects.get(card_token = (card_token39+card_token05[:5]).decode())
            
            except:
                return HttpResponse({'message': 'Failed'})


        except KeyError:
            return Response({'message': "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
        
        else:

            return HttpResponse({
                'message' : 'Success',
                'card_token' : (card_token39+card_token05[:5]).decode(),
                'oiling_type' : card_infos.oiling_type,
                'oiling_price' : card_infos.oiling_price,
                'point_number' : card_infos.point_number,
                'oiling_receipt' : card_infos.oiling_receipt
                })