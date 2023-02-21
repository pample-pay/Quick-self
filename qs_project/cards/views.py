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

            if form_card_num_valid(ccf):

                ################### 카드 토큰 39, 5자리 ###################
                card_token39, card_token05 = modules.get_token(card_num)
                ########################################################

            else:
                context = {}
                
                context['card_num1'] = ccf['card_num1']
                context['card_num2'] = ccf['card_num2']
                context['card_num3'] = ccf['card_num3']
                context['card_num4'] = ccf['card_num4']

                context['error'] = "카드 번호를 확인해주세요."

                return TemplateResponse(request, "cards/insert_enroll.html", context)


            try:
                card_info = Card_Info.objects.get(card_token = (card_token39+card_token05[:5]).decode())
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
            
            context = {}

            context['card_num1'] = ccf['card_num1']
            context['card_num2'] = ccf['card_num2']
            context['card_num3'] = ccf['card_num3']
            context['card_num4'] = ccf['card_num4']

            if form_card_num_valid(ccf):

                ################### 카드 토큰 39, 5자리 ###################
                card_token39, card_token05 = modules.get_token(card_num)
                ########################################################

                try :
                    Card_Info.objects.get(card_token = (card_token39+card_token05[:5]).decode())
                except:
                    context['error'] = "등록된 카드가 존재하지 않습니다."

                    return TemplateResponse(request, "cards/insert_enroll.html", context)

                updated_values = {
                    'card_uniq' : ccf['card_num1'],
                    'card_nickname' : ccf['card_num1'],
                }

            else:
                context['error'] = "카드 번호를 확인해주세요."

                return TemplateResponse(request, "cards/insert_enroll.html", context)


        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            Card_Info.objects.update_or_create(
                card_token = (card_token39+card_token05[:5]).decode(),
                defaults = updated_values
            )

            User_Card.objects.update_or_create(
                user_id=request.user,
                card_token=Card_Info.objects.get(card_token=(card_token39+card_token05[:5]).decode())
            )

            return redirect('/enroll')


class CardEnrollView(APIView):

    def post(self, request):

        try:
            ccf = request.data
            card_num = ccf['card_num1']+ccf['card_num2']+ccf['card_num3']+ccf['card_num4']

            context = {
                'form2_card_num1' : ccf['card_num1'],
                'form2_card_num2' : ccf['card_num2'],
                'form2_card_num3' : ccf['card_num3'],
                'form2_card_num4' : ccf['card_num4'],
                
                'form2_oiling_type' : ccf['oiling_type'],
                'form2_oiling_price' : ccf['oiling_price'],

                'form2_point_num1' : ccf['point_num1'],
                'form2_point_num2' : ccf['point_num2'],
                'form2_point_num3' : ccf['point_num3'],
                'form2_point_num4' : ccf['point_num4'],

                'form2_oiling_receipt' : ccf['oiling_receipt'],
            }

            if form_card_num_valid(ccf):

                ################### 카드 토큰 39, 5자리 ###################
                card_token39, card_token05 = modules.get_token(card_num)
                ########################################################
                
                #for your card name
                cn = card_nickname(ccf['card_where'], ccf['card_num1'])

                if point_valid(ccf):
                    point_num = ccf['point_num1']+ccf['point_num2']+ccf['point_num3']+ccf['point_num4']
                else:
                    point_num = ''

                updated_values = {
                    'card_uniq' : ccf['card_num1'],
                    'card_nickname' : cn,
                    'oiling_type' : ccf['oiling_type'],
                    'oiling_price' : ccf['oiling_price'],
                    'point_number' : point_num,
                    'oiling_receipt' : ccf['oiling_receipt'],
                }
            
            else:
                context['error'] = "카드 번호를 확인해주세요."

                return TemplateResponse(request, "cards/insert_enroll.html", context)

        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            Card_Info.objects.update_or_create(
                card_token = (card_token39+card_token05[:5]).decode(),
                defaults = updated_values
                )

            User_Card.objects.update_or_create(
                user_id = request.user,
                card_token = Card_Info.objects.get(card_token = (card_token39+card_token05[:5]).decode()),
            )

            print(card_token05[5:])

            return redirect('/enroll')


class CardDelete(APIView):

    def post(self, request, pk):
        try:
            card_post = User_Card.objects.get(pk=pk)
            card_post.delete()   
        
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return redirect('/enroll')

class CardEdit(APIView):

    def post(self, request, pk):

        try:
            ccf = request.data
            card_token = User_Card.objects.get(pk=pk).card_token
            card_post = Card_Info.objects.get(card_token=card_token)


        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
            
        
        else:
            card_post.card_nickname = ccf['card_nickname']
            card_post.oiling_type = ccf['oiling_type']
            card_post.oiling_price = ccf['oiling_price']
            card_post.oiling_receipt = ccf['oiling_receipt']

            card_post.save()

            return redirect('/enroll')
