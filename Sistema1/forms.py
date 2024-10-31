from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Municipio

class MunicipioForm(forms.ModelForm):
    class Meta:
        model = Municipio
        fields = ["nombre","rut","cuenta"]
        