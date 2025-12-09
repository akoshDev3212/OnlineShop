from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserRegisterForm( UserCreationForm):
    email = forms.EmailField(label='Е-маил')
    first_name = forms.CharField(label='Имя', max_length=100)
    last_name = forms.CharField(label='Фамилия', max_length=100)
    username = forms.CharField(label='Юзер', max_length=100)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', ]


class UserloginForm( AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'email',]