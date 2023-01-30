from .models import Card_Info, User_Card
from .forms import CardEnrollForm

from django.shortcuts import render, redirect
from django.template.response import TemplateResponse

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView


def enroll_view(request):

    card_sets = User_Card.objects.filter(user_id = request.user)
    context = {
        'card_sets': card_sets
    }

    return render(request, 'cards/enroll.html',context)


### For API views ###
class CardEnrollView(APIView):

    def post(self, request):

        try:
            cef = request.data
            card_num = cef['card_num1']+cef['card_num2']+cef['card_num3']+cef['card_num4']
            
            #####################
            card_token = card_num
            #####################
                
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

            User_Card.objects.update_or_create(
                user_id=request.user,
                card_token=Card_Info.objects.get(card_token=card_token),
            )
            
            card_sets = User_Card.objects.filter(user_id = request.user)
            context = {
                'card_sets': card_sets
            }

            return TemplateResponse(request, "cards/enroll.html", context)



class CardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card_Info
        fields = [
            'oiling_type',
            'oiling_price',
            'point_token',
            'oiling_receipt',
        ]


class CardCheckView(APIView):

    def post(self, request):

        try:
            ccf = request.data
            card_num = ccf['card_num1']+ccf['card_num2']+ccf['card_num3']+ccf['card_num4']

            #####################
            card_token = card_num
            #####################

            card_info = ''

            card_info = Card_Info.objects.get(card_token = card_token)
            serializer_class = CardInfoSerializer(card_info)

            context = serializer_class.data
        
            context['card_num1'] = ccf['card_num1']
            context['card_num2'] = ccf['card_num2']
            context['card_num3'] = ccf['card_num3']
            context['card_num4'] = ccf['card_num4']

            context['oiling_type'] = Card_Info(oiling_type=context['oiling_type']).get_oiling_type_display()
            context['oiling_price'] = Card_Info(oiling_price=context['oiling_price']).get_oiling_price_display()
            context['oiling_receipt'] = Card_Info(oiling_receipt=context['oiling_receipt']).get_oiling_receipt_display()

            context['point_token'] = '없음'
            if card_info.point_token:
                context['point_token'] = card_info.point_token

        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            card_sets = User_Card.objects.filter(user_id = request.user)
            context['card_sets']= card_sets

            return TemplateResponse(request, "cards/enroll.html", context)



class CardCheckEnrollView(APIView):

    def post(self, request):

        try:
            ccf = request.data
            card_num = ccf['card_num1']+ccf['card_num2']+ccf['card_num3']+ccf['card_num4']

            ####
            card_token = card_num
            ####


        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            User_Card.objects.update_or_create(
                user_id=request.user,
                card_token=Card_Info.objects.get(card_token=card_token),
            )

            card_sets = User_Card.objects.filter(user_id = request.user)
            context = {
                'card_sets': card_sets
            }

            return TemplateResponse(request, "cards/enroll.html", context)

class CardDelete(APIView):

    def post(self, request, pk):
        card_post = User_Card.objects.get(pk=pk)
        card_post.delete()   
        
        return redirect('/enroll')