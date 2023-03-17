from django.contrib import admin
from .models import Card_Info, User_Card, Card_Receipt

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'card_token', 
        'card_nickname',
        'oiling_type',
        'oiling_price',
        'point_number',
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

class UserCardReceiptAdmin(admin.ModelAdmin):
    list_display = (
        'card_token', 
        'card_uniq',
        'oiling_type',
        'oiling_price',
        'point_number',
        'oiling_receipt',
        'gs_code',
        'created_on',
        )
    search_fields = ('user_id',)

admin.site.register(Card_Receipt, UserCardReceiptAdmin)