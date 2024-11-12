
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import logout 
from django.contrib.auth.decorators import login_required
from .forms import MunicipioForm
from .models import Municipios,Convenios
from django.http import FileResponse, Http404
import os
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

   if request.method == "POST":
      if request.POST.get('nombre') and request.POST.get('rut') and request.POST.get('cuenta'):
         muni = Municipios()
         muni.nombre = request.POST.get('nombre')
         muni.rut = request.POST.get('rut')
         muni.cuenta = request.POST.get('cuenta')
         muni.save()
         return redirect('listar')
   return render(request, 'Ui/ui4.html',)


def Agregar_Convenios(request):
   if request.method == "POST":
      if request.POST.get('nombre') and request.POST.get('descripcion') and request.POST.get('total') and request.POST.get('documento') and request.POST.get('municipio'):
         conven = Convenios()
         conven.nombre = request.POST.get('nombre')
         conven.descripcion = request.POST.get('descripcion')
         conven.total = request.POST.get('total')
         conven.documento = request.POST.get('documento')
         conven.municipio = request.POST.get('municipio')
         conven.save()
         return redirect('listar')
   return render(request, 'Ui/convenios.html',)



def Listar_Municipios(request):
   municipalidad = Municipios.objects.all()
   datos = {'municipios_d': municipalidad}
   return render(request,'Ui/ui3.html',datos)


def detalles_Municipio(request,id):
   municipio = get_object_or_404(Municipios, id=id)
   convenios = municipio.convenios.all()  
   datos = {"municipio":municipio, "convenios":convenios}
   return render(request,'Ui/detalle_Municipio.html',datos)

def ver_convenio(request, nombre_archivo):
    ruta_convenios = os.path.join("ruta/completa/a/convenios", nombre_archivo)
    if os.path.exists(ruta_convenios):
        return FileResponse(open(ruta_convenios, 'rb'), content_type='application/pdf')
    else:
        raise Http404("Archivo no encontrado")



   
   # Form_Municipal = MunicipioForm()
   # if request.method == "POST":
   #    Form_Municipal = MunicipioForm(request.POST)
   #    if Form_Municipal.is_valid():
   #       Form_Municipal.save()
   #       return Ui3(request)
   # data = {"form":Form_Municipal}

   



@login_required
def base(request):
   return render(request,"Ui/base.html")


def exit(request):
   logout(request)
   return redirect('Ui2')