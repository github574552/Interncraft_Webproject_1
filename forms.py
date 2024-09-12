# forms.py
from django import forms
from .models import Image
class QuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)

from django import forms

class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'placeholder': '123 Main St, City, Country',
        'class': 'form-control'
    }))
    card = forms.CharField(max_length=16, widget=forms.TextInput(attrs={
        'placeholder': 'Card Number',
        'class': 'form-control'
    }))


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['name', 'image', 'price']
        

