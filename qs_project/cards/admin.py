from django.contrib import admin
from .models import Card_Info, User_Card
from django.contrib.auth.models import Group

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'card_token', 
        'oiling_type',
        'oiling_price',
        'oiling_receipt',
        )
    search_fields = ('card_token',)

admin.site.register(Card_Info, UserAdmin)


class UserCardAdmin(admin.ModelAdmin):
    list_display = (
        'user_id', 
        'card_token',
        )
    search_fields = ('user_id',)

admin.site.register(User_Card, UserCardAdmin)