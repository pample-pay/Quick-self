from .models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm

def hp_validator(value):
    if len(str(value)) != 10:
        raise forms.ValidationError('핸드폰 번호 입력 형식을 맞춰주세요.')


class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['user_id'].label = '아이디'
        self.fields['user_id'].widget.attrs.update({     
            'class': 'form-control',
            'autofocus': False
        })
        self.fields['password1'].label = '비밀번호'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
        })

    class Meta:
        model = User
        fields = ['user_id', 'password1', 'password2', 'hp',]

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.level = '2'
        user.save()

        return user