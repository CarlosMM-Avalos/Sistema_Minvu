from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Municipios, Convenios

class MunicipioForm(forms.ModelForm):
    class Meta:
        model = Municipios
        fields = ["nombre","rut","cuenta",]


class ConvenioForm(forms.ModelForm):
    class Meta:
        model = Convenios
        fields = ["id","nombre","descripcion","total","documento","municipio",]






class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']  # Agrega los campos que quieras
        