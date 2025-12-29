from django import forms
from django.forms import ModelForm
from .models import Moto

class MotoForm(ModelForm):
    class Meta:
        model = Moto
        fields = ['marca', 'modelo', 'year', 'color', 'placa', 'observaciones']


        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Año'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Placa'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Observaciones'}),
        }