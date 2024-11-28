
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import logout 
from django.contrib.auth.decorators import login_required
from .forms import MunicipioForm
from .models import Municipios,Convenios, HistorialConvenios
from django.http import FileResponse, Http404
import os
# Create your views here.


@login_required
def Login_Template(request):   
   return render(request,'registration/login.html')

@login_required
def Inicio(request):
  return render(request,'Ui/ui1.html')

#Inicio----------------------------------

@login_required
def Home(request):
   return render(request, 'Ui/home.html')   

#Municipio----------------------------------

@login_required
def Agregar_Mun(request):

   if request.method == "POST":
      if request.POST.get('nombre') and request.POST.get('rut') and request.POST.get('cuenta'):
         muni = Municipios()
         muni.nombre = request.POST.get('nombre')
         muni.rut = request.POST.get('rut')
         muni.cuenta = request.POST.get('cuenta')
         muni.save()
         return redirect('Mun_List')
   return render(request, 'Ui/Agregar_Mun.html',)

@login_required
def Lista_Mun(request):
   return render(request, 'Ui/Lista_Mun.html')

def Listar_Municipios(request):
   municipalidad = Municipios.objects.all()
   datos = {'municipios_d': municipalidad}
   return render(request,'Ui/Lista_Mun.html',datos)

def detalles_Municipio(request,id):
   municipio = get_object_or_404(Municipios, id=id)
   convenios = municipio.convenios.all()  
   datos = {"municipio":municipio, "convenios":convenios}
   return render(request,'Ui/detalle_Municipio.html',datos)    

def Actualizar_Municipio(request,id):
    municipio = get_object_or_404(Municipios, id=id)
    if request.method == "POST":
       municipio.nombre = request.POST.get('nombre')
       municipio.rut = request.POST.get('rut')
       municipio.cuenta = request.POST.get('cuenta')
       municipio.save()
       return redirect('Mun_List')  
    data = {'municipio': municipio}
    return render(request, 'UI\Actulizar_Mun.html',data)    
    
def Eliminar_Municipio(request, id):
    municipio = get_object_or_404(Municipios, id=id)
    municipio.delete()
    return redirect('Mun_List')  

#Convenios----------------------------------


def ver_convenio(request, nombre_archivo):
    ruta_convenios = os.path.join("ruta/completa/a/convenios", nombre_archivo)
    if os.path.exists(ruta_convenios):
        return FileResponse(open(ruta_convenios, 'rb'), content_type='application/pdf')
    else:
        raise Http404("Archivo no encontrado")
    
def Agregar_Convenios(request):
   mun_data = Municipios.objects.all()
   if request.method == "POST":
      if request.POST.get('nombre') and request.POST.get('descripcion') and request.POST.get('total') and request.FILES.get('documento') and request.POST.get('municipio'):
         conven = Convenios()
         conven.nombre = request.POST.get('nombre')
         conven.descripcion = request.POST.get('descripcion')
         conven.total = request.POST.get('total')
         conven.documento = request.FILES.get('documento')
         municipio_id = request.POST.get('municipio')
         conven.municipio = Municipios.objects.get(id=int(municipio_id))
         conven.save()
         print("Archivo guardado en:", conven.documento.path)  
         return redirect('Mun_List')
   return render(request, 'Ui/convenios.html', {'municipio': mun_data})
   
def Actualizar_Convenio(request, id):
    convenio = get_object_or_404(Convenios, id=id)

    if request.method == "POST":
        # Crear un registro en el historial antes de actualizar el convenio
        HistorialConvenios.objects.create(
            convenio_madre=convenio,
            nombre=convenio.nombre,
            descripcion=convenio.descripcion,
            total=convenio.total,
            documento=convenio.documento if convenio.documento else None
        )

        # Actualizar los campos del convenio actual
        convenio.nombre = request.POST.get('nombre')
        convenio.descripcion = request.POST.get('descripcion')
        convenio.total = request.POST.get('total')

        if request.FILES.get('documento'):
            convenio.documento = request.FILES.get('documento')

        convenio.save()
        return redirect('Mun_List')

    # Incluye el historial relacionado
    historial = convenio.historial.all()
    data = {'convenio': convenio, 'historial': historial}
    return render(request, 'UI/Actulizar_Conv.html', data)



def Ver_Historial_Convenio(request, id):
    # Obtener el convenio específico
    convenio = get_object_or_404(Convenios, id=id)
    
    # Obtener todos los registros del historial relacionados con este convenio
    historial = convenio.historial.all()
    
    # Crear un diccionario con el convenio y su historial
    data = {
        'convenio': convenio,
        'historial': historial
    }
    
    # Pasar los datos a la plantilla para renderizarlos
    return render(request, 'UI/ui1.html', data)



#funciones.............................

@login_required
def base(request):
   return render(request,"Ui/base.html")


def exit(request):
   logout(request)
   return redirect('Home')





'''  
def actualizar_Municipio(request, id):
    empleado = Municipios.objects.get(id = id)
    form = MunicipioForm(instance=empleado)
    if request.method == 'POST':                           
        form = MunicipioForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
        return Ui3(request)
    data = {'form' : form}
    return render(request, 'kozanApp/Actualizar_Mun.html', data)
'''


'''
   Form_Municipal = MunicipioForm()
   if request.method == "POST":
      Form_Municipal = MunicipioForm(request.POST)
      if Form_Municipal.is_valid():
         Form_Municipal.save()
         return Ui3(request)
   data = {"form":Form_Municipal}
'''

'''def Actualizar_Convenio(request,id):
    convenio = get_object_or_404(Convenios, id=id)
    if request.method == "POST":
       convenio.nombre = request.POST.get('nombre')
       convenio.descripcion = request.POST.get('descripcion')
       convenio.total = request.POST.get('total')
       convenio.documento = request.FILES.get('documento')
       convenio.municipio = request.POST.get('municipio')
       
       convenio.save()
       return redirect('Mun_List')  # Redirige a la lista de municipios
    data = {'convenio': convenio}
    return render(request, 'UI\Actulizar_Conv.html',data)   '''