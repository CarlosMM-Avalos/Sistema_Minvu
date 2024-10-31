
from django.shortcuts import render, redirect
from django.contrib.auth import logout 
from django.contrib.auth.decorators import login_required
from .forms import MunicipioForm
# Create your views here.


@login_required
def Login_Template(request):   
   return render(request,'registration/login.html')

@login_required
def Inicio(request):
  return render(request,'Ui/ui1.html')


#Interfaz inicial
@login_required
def Ui2(request):
   return render(request, 'Ui/ui2.html')
   
#Interfaz Municipio
@login_required
def Ui3(request):
   return render(request, 'Ui/ui3.html')


#Interfaz Crea Municipio
@login_required
def Ui4(request):
   Form_Municipal = MunicipioForm()
   if request.method == "POST":
      Form_Municipal = MunicipioForm(request.POST)
      if Form_Municipal.is_valid():
         Form_Municipal.save()
         return Ui3(request)
   data = {"form":Form_Municipal}

   return render(request, 'Ui/ui4.html',data)


@login_required
def base(request):
   return render(request,"Ui/base.html")


def exit(request):
   logout(request)
   return redirect('Ui2')