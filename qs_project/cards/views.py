from django.shortcuts import render
from .models import Card_Info
from .forms import CardEnrollForm

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


def enroll_view(request):
    form = CardEnrollForm
    return render(request, 'cards/enroll.html', {'form':form})


### For API views ###
class CardEnrollView(APIView):

    def post(self, request):

        try:
            cef = request.data
            card_num = cef['card_num1']+cef['card_num2']+cef['card_num3']+cef['card_num4']
            card_token = card_num

            point_num = ''

            if (cef['point_num1']!='' and
                cef['point_num2']!='' and
                cef['point_num3']!='' and
                cef['point_num4']!=''):
                point_num = cef['point_num1']+cef['point_num2']+cef['point_num3']+cef['point_num4']

            updated_values = {
                'oiling_type' : cef['oiling_type'],
                'oiling_price' : cef['oiling_price'],
                'point_token' : point_num,
                'oiling_receipt' : cef['oiling_receipt'],
            }

        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            Card_Info.objects.update_or_create(
                card_token=card_token,
                defaults=updated_values
                )
            return Response({'message': 'OK'})
