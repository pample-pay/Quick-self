from django.contrib import admin
from .models import Card_Info
from django.contrib.auth.models import Group

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'card_token', 
        'oiling_type',
        'oiling_price',
        'oiling_receipt',
        )
    search_fields = ('user_id',)

admin.site.register(Card_Info, UserAdmin)