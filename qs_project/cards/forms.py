from .models import Card_Info

from django import forms


class CardEnrollForm(forms.ModelForm):

    class Meta:
        model = Card_Info
        fields = ['card_token', 'oiling_type', 'oiling_price', 'point_token', 'oiling_receipt',]
