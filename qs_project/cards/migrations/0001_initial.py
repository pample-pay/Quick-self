# Generated by Django 4.1.7 on 2023-03-17 05:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_token', models.CharField(max_length=256, verbose_name='카드토큰')),
                ('card_uniq', models.CharField(default='None', max_length=10, verbose_name='카드구분')),
                ('card_nickname', models.CharField(default='None', max_length=10, verbose_name='카드닉네임')),
                ('oiling_type', models.CharField(choices=[('2', '고급휘발유'), ('1', '휘발유'), ('0', '경유')], max_length=10, verbose_name='유종')),
                ('oiling_price', models.CharField(choices=[('10', '가득'), ('9', '10만원'), ('8', '9만원'), ('7', '8만원'), ('6', '7만원'), ('5', '6만원'), ('4', '5만원'), ('3', '4만원'), ('2', '3만원'), ('1', '2만원'), ('0', '1만원')], max_length=10, verbose_name='금액')),
                ('point_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='포인트카드번호')),
                ('oiling_receipt', models.CharField(choices=[('1', 'NO'), ('0', 'YES')], default=0, max_length=10, verbose_name='영수증발행여부')),
            ],
            options={
                'verbose_name': '카드정보',
                'verbose_name_plural': '카드정보',
                'db_table': 'CARDINFO_TB',
            },
        ),
        migrations.CreateModel(
            name='Card_Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_token', models.CharField(max_length=256, verbose_name='카드토큰')),
                ('card_uniq', models.CharField(default='None', max_length=10, verbose_name='카드구분')),
                ('oiling_type', models.CharField(choices=[('2', '고급휘발유'), ('1', '휘발유'), ('0', '경유')], max_length=10, verbose_name='유종')),
                ('oiling_price', models.CharField(choices=[('10', '가득'), ('9', '10만원'), ('8', '9만원'), ('7', '8만원'), ('6', '7만원'), ('5', '6만원'), ('4', '5만원'), ('3', '4만원'), ('2', '3만원'), ('1', '2만원'), ('0', '1만원')], max_length=10, verbose_name='금액')),
                ('point_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='포인트카드번호')),
                ('oiling_receipt', models.CharField(choices=[('1', 'NO'), ('0', 'YES')], default=0, max_length=10, verbose_name='영수증발행여부')),
                ('gs_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='주유소코드')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '결제내역',
                'verbose_name_plural': '결제내역',
                'db_table': 'CARDRECEIPT_TB',
            },
        ),
        migrations.CreateModel(
            name='User_Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.card_info')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='아이디')),
            ],
            options={
                'verbose_name': '유저카드',
                'verbose_name_plural': '유저카드',
                'db_table': 'USERCARD_TB',
            },
        ),
    ]
