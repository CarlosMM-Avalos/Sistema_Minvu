
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import MunicipioForm
from .models import Municipios,Convenios, HistorialConvenios, Rendiciones, Programas, Notificaciones,Reintegros
from django.http import FileResponse, Http404
import os
from django.db.models import Q
from .forms import CustomUserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .models import Rendiciones, Convenios
from datetime import datetime
from decimal import Decimal
from django.core.paginator import Paginator
# Create your views here.

from django.http import JsonResponse
from django.template.loader import render_to_string
import json
from django.db.models import Sum

from django.shortcuts import render
from django.db.models import Sum

from django.shortcuts import render
from django.db.models import Sum
from .models import Convenios, Rendiciones

from django.shortcuts import render
from django.db.models import Sum
from .models import Convenios, Rendiciones
from django.shortcuts import render
from django.db.models import Sum
from .models import Convenios, Rendiciones

from django.shortcuts import render
from django.db.models import Sum, F
from .models import Convenios, Rendiciones
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

def Register_Template(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está en uso.")
            return redirect('register')

        # Crear el usuario
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)  # Autentica al usuario después de registrarse
        messages.success(request, "Cuenta creada exitosamente.")
        return redirect('programas')  # Redirige a la página principal o donde desees

    return render(request, 'registration/register.html')





@login_required
def Login_Template(request):   
   return render(request,'registration/login.html')

@login_required
def Inicio(request):
  return render(request,'UI/ui1.html')

#perfil
def perfil(request):
   return render(request,'UI/perfil.html')


@login_required
def update_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')

        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username=new_username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso. Elige otro.')
        else:
            # Actualizar el nombre de usuario del usuario actual
            request.user.username = new_username
            request.user.save()
            messages.success(request, 'Nombre de usuario actualizado con éxito.')

    return render(request, 'UI/perfil.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            messages.error(request, 'La contraseña actual es incorrecta.')
        elif new_password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Mantener sesión activa después del cambio de contraseña
            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('perfil')  # Cambia a la URL que corresponda

        # Redirigir a la misma página si hay errores
        return redirect('change_password')

    # Manejo de solicitudes GET
    return render(request, 'change_password.html')




#Inicio----------------------------------

@login_required
def Home(request):
   return render(request, 'UI/home.html')   

#Municipio--------------------------------------------------------------------------------------------------------------------------------------------------------------
@login_required
def Agregar_Mun(request):
    # Obtener todos los programas disponibles
    programa_data = Programas.objects.all()

    bancos = Municipios.BANCOS_CHOICES 
    tcuenta = Municipios.TCUENTA_CHOICES
    # Obtener el programa actual desde la URL (GET o POST)
    programa_id_actual = request.GET.get('programa_id') or request.POST.get('programa')

    if request.method == "POST":
        # Validar que todos los campos necesarios estén presentes
        if request.POST.get('nombre') and request.POST.get('rut') and request.POST.get('cuenta') and request.POST.get('banco') and request.POST.get('tcuenta') and request.POST.get('programa'):
            try:
                # Crear un nuevo municipio
                muni = Municipios()
                muni.nombre = request.POST.get('nombre')
                muni.rut = request.POST.get('rut')
                muni.cuenta = request.POST.get('cuenta')
                muni.banco = request.POST.get('banco')
                muni.tcuenta = request.POST.get('tcuenta')
                programa_id = request.POST.get('programa')
                muni.programas = Programas.objects.get(id=int(programa_id))
                muni.save()

                # Redirigir al programa actual
                return redirect(f"/detallesProgramas/{programa_id}/")
            except Programas.DoesNotExist:
                return render(request, 'UI/Agregar_Mun.html', {
                    'programa': programa_data,
                    'error': 'El programa seleccionado no existe.'
                })

    # Si no se proporciona un programa_id, manejar el caso con un valor predeterminado
    if not programa_id_actual and programa_data.exists():
        programa_id_actual = programa_data.first().id

    return render(request, 'UI/Agregar_Mun.html', 
    {
        'programa': programa_data,
        'programa_id': programa_id_actual,  # Enviar el programa actual al template
        'bancos': bancos,
        'tcuenta': tcuenta,
    })







@login_required
def Lista_Mun(request):
   return render(request, 'UI/Lista_Mun.html')

def Listar_Municipios(request):

   busqueda = request.GET.get('buscar')
   municipalidad = Municipios.objects.all()

   if busqueda: 
      municipalidad = Municipios.objects.filter(
         Q(nombre__icontains = busqueda) |
         Q(rut__icontains = busqueda) |
         Q(cuenta__icontains = busqueda)
      ).distinct()

   datos = {'municipios_d': municipalidad}
   return render(request,'UI/Lista_Mun.html',datos)




def detalles_Municipio(request, id):
    municipio = get_object_or_404(Municipios, id=id)    
    convenios = municipio.convenios.all()
    
    # Obtener la búsqueda del usuario
    busqueda = request.GET.get('buscar')
    if busqueda: 
        # Aplicar filtro por nombre en los convenios del municipio
        convenios = convenios.filter(
            Q(nombre__icontains=busqueda)
        ).distinct()

    paginator = Paginator(convenios, 8)  
    page_number = request.GET.get('page')
    convenios = paginator.get_page(page_number)

    # Pasar los datos al template
    datos = {"municipio": municipio, "convenios": convenios,}
    return render(request, 'UI/detalle_Municipio.html', datos)


def Actualizar_Municipio(request, id):

    bancos = Municipios.BANCOS_CHOICES 
    tcuenta = Municipios.TCUENTA_CHOICES
    municipio = get_object_or_404(Municipios, id=id)
    if request.method == "POST":
        municipio.nombre = request.POST.get('nombre')
        municipio.rut = request.POST.get('rut')
        municipio.cuenta = request.POST.get('cuenta')
        municipio.banco = request.POST.get('banco')
        municipio.tcuenta = request.POST.get('tcuenta')
        municipio.save()
        
        # Redirigir a la URL pasada en el campo 'next'
        next_url = request.POST.get('next', 'programas')  # Por defecto, redirige a 'programas'
        return redirect(next_url)
    
    data = {'municipio': municipio, "bancos":bancos,"tcuenta":tcuenta}
    return render(request, 'UI/Actulizar_Mun.html', data)
    
def Eliminar_Municipio(request, id):
    municipio = get_object_or_404(Municipios, id=id)
    municipio.delete()
    return redirect(request.META.get('HTTP_REFERER', 'programas')) 




#Convenios--------------------------------------------------------------------------------------------------------------------------------------------------------------


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
         conven.res = request.POST.get('res')
         conven.fecha = request.POST.get('fecha')
         conven.lcl = request.POST.get('lcl')
         conven.total = request.POST.get('total')
         conven.documento = request.FILES.get('documento')
         municipio_id = request.POST.get('municipio')
         conven.municipio = Municipios.objects.get(id=int(municipio_id))
         conven.save()
         print("Archivo guardado en:", conven.documento.path)  
         return redirect('md', id=municipio_id)
   return render(request, 'UI/convenios.html', {'municipio': mun_data})
   


def Actualizar_Convenio(request, id):
    convenio = get_object_or_404(Convenios, id=id)
    municipios = Municipios.objects.all()

    if request.method == "POST":
        # Crear un registro en el historial antes de actualizar el convenio
        HistorialConvenios.objects.create(
            convenio_madre=convenio,
            nombre=convenio.nombre,
            descripcion=convenio.descripcion,
            res=convenio.res,
            fecha=convenio.fecha,
            lcl=convenio.lcl,
            total=convenio.total,
            documento=convenio.documento if convenio.documento else None
        )

        # Actualizar los campos del convenio actual
        convenio.nombre = request.POST.get('nombre')
        convenio.descripcion = request.POST.get('descripcion')
        convenio.res = request.POST.get('res')

        # Procesar la fecha para asegurarse de que está en el formato correcto
        fecha_str = request.POST.get('fecha')  # Obtiene el valor enviado en el formulario
        if fecha_str:
            convenio.fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

        convenio.lcl = request.POST.get('lcl')
        convenio.total = request.POST.get('total')
        

        # Procesar archivo si se subió uno nuevo
        if request.FILES.get('documento'):
            convenio.documento = request.FILES.get('documento')

        # Guardar los cambios
        convenio.save()

        # Redirigir a la vista de detalles del municipio
        municipio_id = convenio.municipio.id  # Obtener el ID del municipio relacionado
        return redirect('md', id=municipio_id)  # 'md' es el nombre de la URL para detalles del municipio

    # Incluye el historial relacionado para mostrarlo en la plantilla
    historial = convenio.historial.all()
    data = {'convenio': convenio, 'historial': historial,'municipios': municipios,}
    return render(request, 'UI/Actulizar_Conv.html', data)


def Eliminar_Convenios(request, id):
    convenio = get_object_or_404(Convenios, id=id)
    convenio.delete()
    #return redirect('HTTP_REFERER', 'default_view')  
    return redirect(request.META.get('HTTP_REFERER', 'default_view'))



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






#Rendiciones-------------------------------------------------------------------------------------------------------------------------------------------------------------


def rendiciones_view(request, id):
    # Obtener el convenio específico
    convenio = get_object_or_404(Convenios, id=id)

    # Obtener el mes seleccionado desde los parámetros de la URL o formulario
    mes_filtro = request.GET.get('mes_rendicion')

    # Filtrar las rendiciones según el convenio y mes seleccionado
    if mes_filtro:
        rendiciones = Rendiciones.objects.filter(
            convenio=convenio, 
            mes_rendicion=mes_filtro
        )
    else:
        # Mostrar todas las rendiciones del convenio si no hay filtro de mes
        rendiciones = Rendiciones.objects.filter(convenio=convenio)

    # Pasar los datos al template
    data = {
        'convenio': convenio,
        'rendiciones': rendiciones,
        'mes_filtro': mes_filtro,
    }
    return render(request, 'UI/Rendiciones.html', data)

def Agregar_Rendiciones(request):
    # Obtener todos los convenios disponibles para mostrar en el formulario
    convenios = Convenios.objects.all()

    if request.method == "POST":
        if (request.POST.get('descripcion') and
            request.POST.get('mes_rendicion') and 
            request.POST.get('numero_oficio') and 
            request.POST.get('estado') and 
            request.POST.get('fecha_de_oficio') and 
            request.POST.get('n_nemo_interno') and 
            request.POST.get('n_sigfe') and 
            request.POST.get('fecha_sigfe') and 
            request.POST.get('gasto_operacional') and 
            request.POST.get('gasto_personal') and 
            request.POST.get('gasto_inversion')):

            # Crear una nueva instancia de Rendiciones
            rendicion = Rendiciones()

            # Asignar valores a los campos del modelo
            rendicion.descripcion = request.POST.get('descripcion')
            rendicion.mes_rendicion = request.POST.get('mes_rendicion')
            rendicion.numero_oficio = request.POST.get('numero_oficio')
            rendicion.estado = request.POST.get('estado')
            rendicion.fecha_de_oficio = request.POST.get('fecha_de_oficio')
            rendicion.n_nemo_interno = request.POST.get('n_nemo_interno')
            rendicion.n_sigfe = request.POST.get('n_sigfe')
            rendicion.fecha_sigfe = request.POST.get('fecha_sigfe')
            rendicion.fecha_actual = datetime.now().date()  # Usamos la fecha actual
            rendicion.gasto_operacional = Decimal(request.POST.get('gasto_operacional'))
            rendicion.gasto_personal = Decimal(request.POST.get('gasto_personal'))
            rendicion.gasto_inversion = Decimal(request.POST.get('gasto_inversion'))
            
            # Obtener el convenio seleccionado
            convenio_id = request.POST.get('convenio')
            if convenio_id:
                rendicion.convenio = Convenios.objects.get(id=convenio_id)

            # Guardar la instancia de Rendiciones en la base de datos
            rendicion.save()

            # Redirigir a la lista de rendiciones
            return redirect('programas')

    return render(request, 'UI/Agregar_Rendiciones.html', {'convenios': convenios})


#DASHBOARD------------------------------------------------------------------------------------------------------------------------------



def dashboard_view(request):
    # Captura los filtros desde el request
    mes = request.GET.get('mes_rendicion', None)
    convenio_id = request.GET.get('convenio', None)

    # Filtrar las rendiciones según el mes y convenio seleccionados (si se proporcionan)
    rendiciones_query = Rendiciones.objects.all()
    if mes:
        rendiciones_query = rendiciones_query.filter(mes_rendicion=mes)
    if convenio_id:
        rendiciones_query = rendiciones_query.filter(convenio_id=convenio_id)

    # Datos agregados para las rendiciones
    rendiciones_aggregates = (
        rendiciones_query
        .values('convenio__nombre')  # Agrupar por convenio
        .annotate(
            total_gasto_operacional=Sum('gasto_operacional'),
            total_gasto_personal=Sum('gasto_personal'),
            total_gasto_inversion=Sum('gasto_inversion'),
            total_gastos=Sum('gasto_operacional') + Sum('gasto_personal') + Sum('gasto_inversion'),
            total_convenio=F('convenio__total')  # Agrega el total desde Convenios
        )
    )

    # Preparar los datos para el gráfico
    labels = [item['convenio__nombre'] for item in rendiciones_aggregates]
    data_total = [item['total_gastos'] for item in rendiciones_aggregates]
    data_operacional = [item['total_gasto_operacional'] for item in rendiciones_aggregates]
    data_personal = [item['total_gasto_personal'] for item in rendiciones_aggregates]
    data_inversion = [item['total_gasto_inversion'] for item in rendiciones_aggregates]
    data_total_convenio = [item['total_convenio'] for item in rendiciones_aggregates]

    # Obtener la lista de convenios para el dropdown
    convenios = Convenios.objects.all()

    # Pasar los datos al template
    context = {
        'labels': labels,
        'data_total': data_total,
        'data_operacional': data_operacional,
        'data_personal': data_personal,
        'data_inversion': data_inversion,
        'data_total_convenio': data_total_convenio,
        'mes_seleccionado': mes,  # Para recordar el filtro seleccionado
        'convenio_seleccionado': convenio_id,  # Para recordar el convenio seleccionado
        'convenios': convenios,  # Lista de convenios
    }
    return render(request, 'UI/dashboard.html', context)


def dashboard_view2(request):
    # Captura los filtros desde el request
    mes = request.GET.get('mes_rendicion', None)
    convenio_id = request.GET.get('convenio', None)

    # Filtrar las rendiciones según el mes y convenio seleccionados (si se proporcionan)
    rendiciones_query = Rendiciones.objects.all()
    if mes:
        rendiciones_query = rendiciones_query.filter(mes_rendicion=mes)
    if convenio_id:
        rendiciones_query = rendiciones_query.filter(convenio_id=convenio_id)

    # Datos agregados para las rendiciones
    rendiciones_aggregates = (
        rendiciones_query
        .values('convenio__nombre')  # Agrupar por convenio
        .annotate(
            total_gasto_operacional=Sum('gasto_operacional'),
            total_gasto_personal=Sum('gasto_personal'),
            total_gasto_inversion=Sum('gasto_inversion'),
            total_gastos=Sum('gasto_operacional') + Sum('gasto_personal') + Sum('gasto_inversion'),
            total_convenio=F('convenio__total')  # Agrega el total desde Convenios
        )
    )

    # Preparar los datos para el gráfico
    labels = [item['convenio__nombre'] for item in rendiciones_aggregates]
    data_total = [item['total_gastos'] for item in rendiciones_aggregates]
    data_operacional = [item['total_gasto_operacional'] for item in rendiciones_aggregates]
    data_personal = [item['total_gasto_personal'] for item in rendiciones_aggregates]
    data_inversion = [item['total_gasto_inversion'] for item in rendiciones_aggregates]
    data_total_convenio = [item['total_convenio'] for item in rendiciones_aggregates]

    # Obtener la lista de convenios para el dropdown
    convenios = Convenios.objects.all()

    # Pasar los datos al template
    context = {
        'labels': labels,
        'data_total': data_total,
        'data_operacional': data_operacional,
        'data_personal': data_personal,
        'data_inversion': data_inversion,
        'data_total_convenio': data_total_convenio,
        'mes_seleccionado': mes,  # Para recordar el filtro seleccionado
        'convenio_seleccionado': convenio_id,  # Para recordar el convenio seleccionado
        'convenios': convenios,  # Lista de convenios
    }
    return render(request, 'UI/dashboard2.html', context)

def dashboard_view3(request):
    # Captura los filtros desde el request
    mes = request.GET.get('mes_rendicion', None)
    convenio_id = request.GET.get('convenio', None)

    # Filtrar las rendiciones según el mes y convenio seleccionados (si se proporcionan)
    rendiciones_query = Rendiciones.objects.all()
    if mes:
        rendiciones_query = rendiciones_query.filter(mes_rendicion=mes)
    if convenio_id:
        rendiciones_query = rendiciones_query.filter(convenio_id=convenio_id)

    # Datos agregados para las rendiciones
    rendiciones_aggregates = (
        rendiciones_query
        .values('convenio__nombre')  # Agrupar por convenio
        .annotate(
            total_gasto_operacional=Sum('gasto_operacional'),
            total_gasto_personal=Sum('gasto_personal'),
            total_gasto_inversion=Sum('gasto_inversion'),
            total_gastos=Sum('gasto_operacional') + Sum('gasto_personal') + Sum('gasto_inversion'),
            total_convenio=F('convenio__total')  # Agrega el total desde Convenios
        )
    )

    # Preparar los datos para el gráfico
    labels = [item['convenio__nombre'] for item in rendiciones_aggregates]
    data_total = [item['total_gastos'] for item in rendiciones_aggregates]
    data_operacional = [item['total_gasto_operacional'] for item in rendiciones_aggregates]
    data_personal = [item['total_gasto_personal'] for item in rendiciones_aggregates]
    data_inversion = [item['total_gasto_inversion'] for item in rendiciones_aggregates]
    data_total_convenio = [item['total_convenio'] for item in rendiciones_aggregates]

    # Obtener la lista de convenios para el dropdown
    convenios = Convenios.objects.all()

    # Pasar los datos al template
    context = {
        'labels': labels,
        'data_total': data_total,
        'data_operacional': data_operacional,
        'data_personal': data_personal,
        'data_inversion': data_inversion,
        'data_total_convenio': data_total_convenio,
        'mes_seleccionado': mes,  # Para recordar el filtro seleccionado
        'convenio_seleccionado': convenio_id,  # Para recordar el convenio seleccionado
        'convenios': convenios,  # Lista de convenios
    }
    return render(request, 'UI/dashboard3.html', context)


def dashboard_view4(request):
    # Captura los filtros desde el request
    mes = request.GET.get('mes_rendicion', None)
    convenio_id = request.GET.get('convenio', None)

    # Filtrar las rendiciones según el mes y convenio seleccionados (si se proporcionan)
    rendiciones_query = Rendiciones.objects.all()
    if mes:
        rendiciones_query = rendiciones_query.filter(mes_rendicion=mes)
    if convenio_id:
        rendiciones_query = rendiciones_query.filter(convenio_id=convenio_id)

    # Datos agregados para las rendiciones
    rendiciones_aggregates = (
        rendiciones_query
        .values('convenio__nombre')  # Agrupar por convenio
        .annotate(
            total_gasto_operacional=Sum('gasto_operacional'),
            total_gasto_personal=Sum('gasto_personal'),
            total_gasto_inversion=Sum('gasto_inversion'),
            total_gastos=Sum('gasto_operacional') + Sum('gasto_personal') + Sum('gasto_inversion'),
            total_convenio=F('convenio__total')  # Agrega el total desde Convenios
        )
    )

    # Preparar los datos para el gráfico
    labels = [item['convenio__nombre'] for item in rendiciones_aggregates]
    data_total = [item['total_gastos'] for item in rendiciones_aggregates]
    data_operacional = [item['total_gasto_operacional'] for item in rendiciones_aggregates]
    data_personal = [item['total_gasto_personal'] for item in rendiciones_aggregates]
    data_inversion = [item['total_gasto_inversion'] for item in rendiciones_aggregates]
    data_total_convenio = [item['total_convenio'] for item in rendiciones_aggregates]

    # Obtener la lista de convenios para el dropdown
    convenios = Convenios.objects.all()

    # Pasar los datos al template
    context = {
        'labels': labels,
        'data_total': data_total,
        'data_operacional': data_operacional,
        'data_personal': data_personal,
        'data_inversion': data_inversion,
        'data_total_convenio': data_total_convenio,
        'mes_seleccionado': mes,  # Para recordar el filtro seleccionado
        'convenio_seleccionado': convenio_id,  # Para recordar el convenio seleccionado
        'convenios': convenios,  # Lista de convenios
    }
    return render(request, 'UI/dashboard4.html', context)



#programas-------------------------------------------------------------------------------------------------------------------------

@login_required
def programas_view(request):
    programas = Programas.objects.all()  # Recuperar todos los programas
    # Crear una lista de colores para asignar a las tarjetas
    colores = ['blue', 'green', 'yellow']
    
    # Pasar los programas y los colores al template
    return render(request, 'UI/programas.html', {'programas': programas, 'colores': colores})




def programas_detalles(request, id):
    programa = get_object_or_404(Programas, id=id)
    municipios_asociados = programa.municipios.all()  # Los municipios asociados al programa específico

    # Búsqueda en municipios asociados
    busqueda = request.GET.get('buscar')
    if busqueda:
        municipios_asociados = municipios_asociados.filter(
            Q(nombre__icontains=busqueda) |
            Q(rut__icontains=busqueda) |
            Q(cuenta__icontains=busqueda)
        ).distinct()

    paginator = Paginator(municipios_asociados, 8)  # Paginar municipios asociados
    page_number = request.GET.get('page')
    municipios = paginator.get_page(page_number)

    # Preparar datos para el template
    datos = {"municipios": municipios, "programas": [programa]}
    return render(request, "UI/detalles_programas.html", datos)


def Listar_Municipios(request):

   busqueda = request.GET.get('buscar')
   municipalidad = Municipios.objects.all()

   if busqueda: 
      municipalidad = Municipios.objects.filter(
         Q(nombre__icontains = busqueda) |
         Q(rut__icontains = busqueda) |
         Q(cuenta__icontains = busqueda)
      ).distinct()

   datos = {'municipios_d': municipalidad}
   return render(request,'UI/Lista_Mun.html',datos)




#extra.............................----------------------------------------------------------------------------------------------------


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Notificaciones

def marcar_notificacion_como_leida(request, id):
    if request.method == "POST":
        notificacion = get_object_or_404(Notificaciones, id=id)
        notificacion.leido = True
        notificacion.save()
        return JsonResponse({"success": True, "id": id})
    return JsonResponse({"success": False})

def lista_notificaciones(request):
    notificaciones = Notificaciones.objects.all().order_by('-fecha_creacion')
    no_leidas = Notificaciones.objects.filter(leido=False).count()
    return render(request, 'notificaciones.html', {
        'notifi': notificaciones,
        'no_leidas': no_leidas
    })


@login_required
def base(request):
   notif = Notificaciones.objects.all()
   

   return render(request,"UI/base.html",{'notifi':notif,})


def exit(request):
   logout(request)
   return redirect('login')

#reintegros-------------------------------------------------------------------------------------------------------------------------------

from django.db.models import Sum

def Listar_Reintegros(request):
    # Filtros dinámicos
    convenios = request.GET.get('convenio', None)
    municipio = request.GET.get('municipio', None)
    fecha_inicio = request.GET.get('fecha_inicio', None)
    fecha_fin = request.GET.get('fecha_fin', None)
    
    filters = Q()
    if convenios:
        filters &= Q(convenio_id=convenios)
    if municipio:
        filters &= Q(convenio__municipio__nombre__icontains=municipio)
    if fecha_inicio and fecha_fin:
        filters &= Q(fecha_limite_devolucion__range=[fecha_inicio, fecha_fin])
    if request.GET.get('buscar'):
        filters &= Q(codigo_referencia__icontains=request.GET.get('buscar'))

    reintegros = Reintegros.objects.filter(filters)

    # Calcular totales
    total_entregado = reintegros.aggregate(total=Sum('monto_entregado'))['total'] or 0
    total_reintegrar = reintegros.aggregate(total=Sum('monto_reintegrar'))['total'] or 0

    # Contexto
    convenios_lista = Convenios.objects.all()
    municipios_lista = Municipios.objects.all()

    datos = {
        'reintegros': reintegros,
        'convenios': convenios_lista,
        'municipios': municipios_lista,
        'total_entregado': total_entregado,
        'total_reintegrar': total_reintegrar,
    }
    return render(request, 'UI/Lista_reintegros.html', datos)



# def Listar_Reintegros(request):
#     # Obtener parámetros de búsqueda
#     convenios = request.GET.get('convenio', None)
#     municipio = request.GET.get('municipio', None)
#     fecha_inicio = request.GET.get('fecha_inicio', None)
#     fecha_fin = request.GET.get('fecha_fin', None)

#     # Filtros dinámicos
#     filters = Q()
    
#     # Filtrar por convenio (asegúrate de que 'convenio' sea una relación válida)
#     if convenios:
#         filters &= Q(convenio__id=convenios)  # Cambié a 'id', usa el campo correcto aquí
    
#     # Filtrar por municipio (asegúrate de que 'municipio' sea una relación válida)
#     if municipio:
#         filters &= Q(convenio__municipio__nombre__icontains=municipio)
    
#     # Filtrar por rango de fechas
#     if fecha_inicio and fecha_fin:
#         filters &= Q(fecha_limite_devolucion__range=[fecha_inicio, fecha_fin])

#     # Filtro por código de referencia
#     busqueda = request.GET.get('buscar')
#     if busqueda:
#         filters &= Q(codigo_referencia__icontains=busqueda)
    
#     # Aplicar filtros al modelo
#     reintegros = Reintegros.objects.filter(filters)

#     # Obtener listas para los select
#     convenios_lista = Convenios.objects.all()
#     municipios_lista = Municipios.objects.all()  # Suponiendo que Municipio es otro modelo relacionado

#       # Agregar datos para el gráfico
#     montos_por_convenio = (
#         reintegros
#         .values('convenio__nombre')
#         .annotate(
#             total_prestado=Sum('monto_entregado'),
#             total_reintegrar=Sum('monto_reintegrar'),
#             porcentaje_reintegrar=(F('monto_reintegrar') * 100) / F('monto_entregado')
#         )
#     )

#     # Contexto para la plantilla
#     datos = {
#         'reintegros': reintegros,
#         'convenios': convenios_lista,
#         'municipios': municipios_lista,
#         'grafico_datos': list(montos_por_convenio),
#     }
#     return render(request,  'UI/Lista_reintegros.html', datos)


# def Listar_Reintegros(request):
#     convenios = request.GET.get('convenio', None)
#     municipio = request.GET.get('municipio', None)
#     fecha_inicio = request.GET.get('fecha_inicio', None)
#     fecha_fin = request.GET.get('fecha_fin', None)

#     filters = Q()
    
#     # Filtrar por convenio
#     if convenios:
#         filters &= Q(convenio__codigo__icontains=convenios)
    
#     # Filtrar por municipio
#     if municipio:
#         filters &= Q(convenio__municipio__nombre__icontains=municipio)
    
#     # Filtrar por rango de fechas
#     if fecha_inicio and fecha_fin:
#         filters &= Q(fecha_limite_devolucion__range=[fecha_inicio, fecha_fin])

#     # Filtro por la búsqueda del código de referencia
#     busqueda = request.GET.get('buscar')
#     if busqueda:
#         filters &= Q(codigo_referencia__icontains=busqueda)
    
#     reintegros = Reintegros.objects.filter(filters)

#     # Obtener convenios y municipios para los select
#     convenios_lista = Convenios.objects.all()
#     municipios_lista = Municipios.objects.all()  # Asumiendo que Municipio es otro modelo

#     datos = {
#         'reintegros': reintegros,
#         'convenios': convenios_lista,
#         'municipios': municipios_lista
#     }
    
#     return render(request, 'UI/Lista_reintegros.html', datos)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# def Agregar_Reintegros(request):
#     convenio_data = Convenios.objects.all()
#     estados = Reintegros.ESTADO_CHOICES

#     if request.method == "POST":
#         try:
#             # Validar los campos obligatorios
#             convenio_id = request.POST.get('convenio')
#             convenio = get_object_or_404(Convenios, id=int(convenio_id))

#             reintegro = Reintegros(
#                 fecha_solicitud=request.POST.get('fecha_solicitud'),
#                 fecha_aprobacion=request.POST.get('fecha_aprobacion'),
#                 codigo_referencia=request.POST.get('codigo_referencia'),
#                 numero_oficio=request.POST.get('numero_oficio'),
#                 fecha_oficio=request.POST.get('fecha_oficio'),
#                 numero_sigfe=request.POST.get('numero_sigfe'),
#                 fecha_sigfe=request.POST.get('fecha_sigfe'),
#                 monto_entregado=request.POST.get('monto_entregado'),
#                 monto_reintegrar=request.POST.get('monto_reintegrar'),
#                 fecha_creacion=request.POST.get('fecha_creacion'),
#                 fecha_limite_devolucion=request.POST.get('fecha_limite_devolucion'),
#                 estado_reintegro=request.POST.get('estado_reintegro'),
#                 documento=request.FILES.get('documento'),
#                 convenio=convenio
#             )

#             # Validación adicional si es necesario
#             if int(reintegro.monto_reintegrar) > int(reintegro.monto_entregado):
#                 messages.error(request, "El monto a reintegrar no puede ser mayor que el monto entregado.")
#                 return render(request, 'UI/Agregar_reintegros.html', {'convenio': convenio_data, "estados": estados})

#             # Guardar el reintegro
#             reintegro.save()
#             messages.success(request, "Reintegro registrado exitosamente.")
#             return redirect('Listar_Reintegros')

#         except Exception as e:
#             messages.error(request, f"Error al registrar el reintegro: {str(e)}")
#             return render(request, 'UI/Agregar_reintegros.html', {'convenio': convenio_data, "estados": estados})

#     return render(request, 'UI/Agregar_reintegros.html', {'convenio': convenio_data, "estados": estados})

# views.py
from django.shortcuts import render, redirect
from .models import Reintegros

def Agregar_Reintegros(request):
    if request.method == 'POST':
        convenio_id = request.POST.get('convenio')
        fecha_solicitud = request.POST.get('fecha_solicitud')
        fecha_aprobacion = request.POST.get('fecha_aprobacion')
        codigo_referencia = request.POST.get('codigo_referencia')
        numero_oficio = request.POST.get('numero_oficio')
        fecha_oficio = request.POST.get('fecha_oficio')
        numero_sigfe = request.POST.get('numero_sigfe')
        fecha_sigfe = request.POST.get('fecha_sigfe')
        monto_entregado = request.POST.get('monto_entregado')
        monto_reintegrar = request.POST.get('monto_reintegrar')
        descripcion = request.POST.get('descripcion')
        fecha_limite_devolucion = request.POST.get('fecha_limite_devolucion')
        estado_reintegro = request.POST.get('estado_reintegro')
        documento = request.FILES.get('documento')

        # Validar la existencia del convenio
        convenio = None
        if convenio_id:
            convenio = get_object_or_404(Convenios, id=convenio_id)

        # Crear el nuevo registro en la base de datos
        Reintegros.objects.create(
            convenio=convenio,
            fecha_solicitud=fecha_solicitud,
            fecha_aprobacion=fecha_aprobacion,
            codigo_referencia=codigo_referencia,
            numero_oficio=numero_oficio,
            fecha_oficio=fecha_oficio,
            numero_sigfe=numero_sigfe,
            fecha_sigfe=fecha_sigfe,
            monto_entregado=monto_entregado,
            monto_reintegrar=monto_reintegrar,
            descripcion=descripcion,
            fecha_limite_devolucion=fecha_limite_devolucion,
            estado_reintegro=estado_reintegro,
            documento=documento
        )

        return redirect('Listar_Reintegros')  # Redirigir a la vista de lista.

    # Pasar convenios existentes al formulario para seleccionar.
    convenios = Convenios.objects.all()
    return render(request, 'UI/Agregar_reintegros.html', {'convenios': convenios})  

            
 

from django.shortcuts import get_object_or_404, redirect, render
from .models import Reintegros, Convenios
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from .models import Reintegros, Convenios
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from .models import Reintegros, Convenios
from datetime import datetime

def Actualizar_Reintegros(request, id):
    convenios = Convenios.objects.all()  # Trae todos los convenios disponibles
    reintegro = get_object_or_404(Reintegros, id=id)  # Obtiene el reintegro con el id correspondiente
    
    if request.method == 'POST':
        try:
            # Actualiza los campos con los valores del formulario
            reintegro.convenio = Convenios.objects.get(id=request.POST.get('convenio'))
            reintegro.fecha_solicitud = datetime.strptime(request.POST.get('fecha_solicitud'), '%Y-%m-%d').date()
            reintegro.fecha_aprobacion = datetime.strptime(request.POST.get('fecha_aprobacion'), '%Y-%m-%d').date()
            reintegro.codigo_referencia = request.POST.get('codigo_referencia')
            reintegro.numero_oficio = request.POST.get('numero_oficio')
            reintegro.fecha_oficio = datetime.strptime(request.POST.get('fecha_oficio'), '%Y-%m-%d').date()
            reintegro.numero_sigfe = request.POST.get('numero_sigfe')
            reintegro.fecha_sigfe = datetime.strptime(request.POST.get('fecha_sigfe'), '%Y-%m-%d').date()
            reintegro.monto_entregado = request.POST.get('monto_entregado')
            reintegro.monto_reintegrar = request.POST.get('monto_reintegrar')
            reintegro.descripcion = request.POST.get('descripcion')
            reintegro.fecha_limite_devolucion = datetime.strptime(request.POST.get('fecha_limite_devolucion'), '%Y-%m-%d').date()
            reintegro.estado_reintegro = request.POST.get('estado_reintegro')

            # Si se sube un nuevo documento
            if request.FILES.get('documento'):
                reintegro.documento = request.FILES.get('documento')
            
            # Guarda los cambios en el reintegro
            reintegro.save()

            # Redirige a la vista de listar reintegros
            return redirect('Listar_Reintegros')  # Redirige a la URL que lista todos los reintegros

        except Exception as e:
            # Si hay algún error, imprime el error para depurar y muestra el formulario con el mensaje de error
            print(f"Error al actualizar el reintegro: {e}")
            return render(request, 'UI/Actualizar_reintegros.html', {'reintegro': reintegro, 'convenios': convenios, 'error': str(e)})

    # En el caso de que la solicitud sea GET, renderiza el formulario con los datos actuales
    data = {'reintegro': reintegro, 'convenios': convenios}
    
    # Si ya tiene un documento, agregarlo al contexto para mostrarlo en el formulario
    if reintegro.documento:
        data['documento_url'] = reintegro.documento.url  # Asumiendo que 'documento' es un FileField y está almacenado

    return render(request, 'UI/Actualizar_reintegros.html', data)


    #     # Validar convenio
    #     convenio = None
    #     if convenio_id:
    #         convenio = get_object_or_404(Convenios, id=convenio_id)

    #     # Actualizar los datos del reintegro
    #     reintegro.convenio = convenio
    #     reintegro.fecha_solicitud = fecha_solicitud
    #     reintegro.fecha_aprobacion = fecha_aprobacion
    #     reintegro.codigo_referencia = codigo_referencia
    #     reintegro.numero_oficio = numero_oficio
    #     reintegro.fecha_oficio = fecha_oficio
    #     reintegro.numero_sigfe = numero_sigfe
    #     reintegro.fecha_sigfe = fecha_sigfe
    #     reintegro.monto_entregado = monto_entregado
    #     reintegro.monto_reintegrar = monto_reintegrar
    #     reintegro.descripcion = descripcion
    #     reintegro.fecha_limite_devolucion = fecha_limite_devolucion
    #     reintegro.estado_reintegro = estado_reintegro

    #     if documento:  # Solo actualizar si se adjunta un nuevo documento
    #         reintegro.documento = documento
        
    #     reintegro.save()

    #     return redirect('Listar_Reintegros')  # Redirigir a la lista de reintegros

    # # Cargar la lista de convenios para el formulario
    # convenios = Convenios.objects.all()
    # return render(request, 'UI/Actualizar_reintegros.html', {
    #     'reintegro': reintegro,
    #     'convenios': convenios
    # })
    

def borrar_Reintegros(request,id):

    reintegro = get_object_or_404(Reintegros, id=id)
    reintegro.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))
    #return redirect(request.META.get('HTTP_REFERER', 'default_view'))
    #return render(request,'UI/.html')

def detalles_Reintegro(request,id):
    pass

def prueba(request):
     return render(request,'UI/prueba.html',)




#Paginacion 


# def programas_detalles(request, id):
    
#     programa = get_object_or_404(Programas, id=id)
#     municipio = programa.municipios.all()   
    
#     paginator = Paginator(municipio, 8)  
#     page_number = request.GET.get('page')
#     municipios = paginator.get_page(page_number)

    
#     datos = {"municipios": municipios, "programas": [programa]}
#     return render(request, "UI/detalles_programas.html", datos)


