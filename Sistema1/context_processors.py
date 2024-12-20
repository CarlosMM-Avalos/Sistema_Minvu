from .models import Notificaciones

def notificaciones(request):
    # Puedes añadir más lógica aquí si es necesario
    return {
        'notifi': Notificaciones.objects.all()
    }