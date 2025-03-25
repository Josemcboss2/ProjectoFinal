from django import forms
from .models import ContactMessage

class ContactForm(forms.Form):
    name = forms.CharField(label='Nombre completo', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingresa tu nombre'
    }))
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingresa tu email'
    }))
    message = forms.CharField(label='Mensaje', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 5,
        'placeholder': '¿En qué podemos ayudarte?'
    }))