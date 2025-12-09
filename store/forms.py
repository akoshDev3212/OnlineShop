from django import forms
from .models import Order, Review, RATE_CHOICES

class OrderForm(forms.Form):
    adress = forms.CharField(label='Write your adress',)
    phone = forms.CharField(label='Write your phone number',)

    class Meta:
        model = Order
        fields = ['phone', 'adress']


class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'textarea'}), label='Fikringizni yozing')
    rate = forms.ChoiceField(choices=RATE_CHOICES,required=True, label='baholash 1 dan 5 gacha')


    class Meta:
        model = Review
        fields = ['text','rate']