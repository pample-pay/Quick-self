import modules

from .models import Card_Info, User_Card
from .restricts import *
from users.decorators import *

from django.shortcuts import render, redirect
from django.template.response import TemplateResponse

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView


@login_message_required
def enroll_view(request):
    if request.user.is_authenticated:
        card_sets = User_Card.objects.filter(user_id = request.user)
        context = {
            'card_sets': card_sets
            }
        return render(request, 'cards/enroll.html',context)
    
    else:
        return render(request, 'cards/enroll.html')


@login_message_required
def insert_card_view(request):
    return render(request, 'cards/insert_enroll.html')


### For API views ###
class CardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card_Info
        fields = [
            'oiling_type',
            'oiling_price',
            'point_number',
            'oiling_receipt',
        ]


class CardCheckView(APIView):

    def post(self, request):

        try:
            ccf = request.data
            card_num = ccf['card_num1']+ccf['card_num2']+ccf['card_num3']+ccf['card_num4']


            if len(card_num) != 16:
                context = {}
                
                context['card_num1'] = ccf['card_num1']
                context['card_num2'] = ccf['card_num2']
                context['card_num3'] = ccf['card_num3']
                context['card_num4'] = ccf['card_num4']

                context['error'] = "카드 번호를 확인해주세요."
                
                return TemplateResponse(request, "cards/insert_enroll.html", context)

            #####################
            card_token39, card_token05 = modules.get_token(card_num)
            #####################

            print(card_token39)
            print(card_token05)


            try:
                card_info = Card_Info.objects.get(card_token1 = card_token39).get(card_token2 = card_token05)
                serializer_class = CardInfoSerializer(card_info)
                context = serializer_class.data
                
                context['oiling_type'] = Card_Info(oiling_type=context['oiling_type']).get_oiling_type_display()
                context['oiling_price'] = Card_Info(oiling_price=context['oiling_price']).get_oiling_price_display()
                context['oiling_receipt'] = Card_Info(oiling_receipt=context['oiling_receipt']).get_oiling_receipt_display()

                context['point_number'] = '없음'
                
                if card_info.point_number:

                    context['point_number'] = (
                        card_info.point_number[:4] + '-'
                        + card_info.point_number[4:8] + '-'
                        + card_info.point_number[8:12] + '-'
                        + card_info.point_number[12:16]
                    )


            except:
                context = {}
                context['error'] = "등록된 카드가 존재하지 않습니다."

            context['card_num1'] = ccf['card_num1']
            context['card_num2'] = ccf['card_num2']
            context['card_num3'] = ccf['card_num3']
            context['card_num4'] = ccf['card_num4']


        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return TemplateResponse(request, "cards/insert_enroll.html", context)


class CardCheckEnrollView(APIView):

    def post(self, request):

        try:
            ccf = request.data
            card_num = ccf['card_num1']+ccf['card_num2']+ccf['card_num3']+ccf['card_num4']


            if len(card_num) != 16:
                context = {}
                
                context['card_num1'] = ccf['card_num1']
                context['card_num2'] = ccf['card_num2']
                context['card_num3'] = ccf['card_num3']
                context['card_num4'] = ccf['card_num4']

                context['error'] = "카드 번호를 확인해주세요."
                
                return TemplateResponse(request, "cards/insert_enroll.html", context)

            #####################
            card_token39, card_token05 = modules.get_token(card_num)
            #####################


            try:
                Card_Info.objects.get(card_token1 = card_token39).get(card_token2 = card_token05)

            except:
                context = {}
                
                context['card_num1'] = ccf['card_num1']
                context['card_num2'] = ccf['card_num2']
                context['card_num3'] = ccf['card_num3']
                context['card_num4'] = ccf['card_num4']
                
                context['error'] = "등록된 카드가 존재하지 않습니다."

                return TemplateResponse(request, "cards/insert_enroll.html", context)

        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

        else:

            User_Card.objects.update_or_create(
                user_id=request.user,
                card_token=Card_Info.objects.get(card_token1=card_token39).get(card_token2=card_token05)
            )

            return redirect('/enroll')


class CardEnrollView(APIView):

    def post(self, request):

        try:
            # user cards list
            card_sets = User_Card.objects.filter(user_id = request.user)
            cef = request.data

            if form_card_num_valid(cef['card_num1'], cef['card_num2'], cef['card_num3'], cef['card_num4']):
                card_num = cef['card_num1']+cef['card_num2']+cef['card_num3']+cef['card_num4']
            
            #####################
            card_token = card_num
            #####################
            card_init = ''
            point_num = ''
            
            #for your card name
            if cef['card_where'] == '0':
                card_init = '국민'
            elif cef['card_where'] == '1':
                card_init = '신한'
            elif cef['card_where'] == '2':
                card_init = '우리'
            elif cef['card_where'] == '3':
                card_init = '카카오'

            card_nickname = card_init + cef['card_num4']

            if (cef['point_num1']!='' and
                cef['point_num2']!='' and
                cef['point_num3']!='' and
                cef['point_num4']!=''):
                point_num = cef['point_num1']+cef['point_num2']+cef['point_num3']+cef['point_num4']
            
            else:
                
                card_sets = User_Card.objects.filter(user_id = request.user)
                context = {
                    'form2_card_num1':cef['card_num1'],
                    'form2_card_num2':cef['card_num2'],
                    'form2_card_num3':cef['card_num3'],
                    'form2_card_num4':cef['card_num4'],
                    
                    'form2_oiling_type' : cef['oiling_type'],
                    'form2_oiling_type':cef['oiling_type'],

                    'form2_point_num1':cef['point_num1'],
                    'form2_point_num2':cef['point_num2'],
                    'form2_point_num3':cef['point_num3'],
                    'form2_point_num4':cef['point_num4'],

                    'form2_oiling_receipt' : cef['oiling_receipt'],
                    
                    'card_sets': card_sets,
                    'error': '포인트 카드 번호를 확인해 주세요.'
                }
                return TemplateResponse(request, "cards/enroll.html", context)


            updated_values = {
                'card_nickname' : card_nickname,
                'oiling_type' : cef['oiling_type'],
                'oiling_price' : cef['oiling_price'],
                'point_number' : point_num,
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


class CardDelete(APIView):

    def post(self, request, pk):
        card_post = User_Card.objects.get(pk=pk)
        card_post.delete()   
        
        return redirect('/enroll')