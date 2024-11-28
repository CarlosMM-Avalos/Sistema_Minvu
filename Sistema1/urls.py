
from django.urls import path
from Sistema1 import views 

urlpatterns = [
    path('login/', views.Login_Template, name = "login"),


    path('',views.Home, name = "Home"),
    path('ui1/<int:id>/', views.Ver_Historial_Convenio, name='H_convenio'),
    path('Mun_List/',views.Listar_Municipios, name = "Mun_List"),
    #convenios
    path('addConv/',views.Agregar_Convenios, name = "addConv"),
    path('ver_convenio/<str:nombre_archivo>/', views.ver_convenio, name='ver_convenio'),
    path('actualizar_Conv/<int:id>/', views.Actualizar_Convenio, name='actualizar_Conv'),  
    path('convenio/<int:id>/historial/', views.Ver_Historial_Convenio, name='ver_historial_convenio'),  
    #Municipios
    path('Agregar_Mun/',views.Agregar_Mun, name = "Agregar_Mun"),
    #path('uiL/',views.Listar_Municipios, name = "listar"),
    path('actualizar_Mun/<int:id>/', views.Actualizar_Municipio, name='actualizar_Mun'),
    path('deleteMun/<int:id>/', views.Eliminar_Municipio, name="delete_mun"),
    path('detailsMun/<int:id>/', views.detalles_Municipio, name="md"),

    path('base/',views.base, name = "base"),


    path('logout/',views.exit, name = "exitt"),   
]
