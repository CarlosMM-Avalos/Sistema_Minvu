
from django.urls import path
from Sistema1 import views 

urlpatterns = [
    path('login/', views.Login_Template, name = "login"),


    path('',views.Ui2, name = "Ui2"),
    path('ui1/',views.Inicio, name = "Ui1"),
    path('Mun_List/',views.Listar_Municipios, name = "Mun_List"),
    path('addConv/',views.Agregar_Convenios, name = "addConv"),
    path('ver_convenio/<str:nombre_archivo>/', views.ver_convenio, name='ver_convenio'),
    #Municipios
    path('ui4/',views.Ui4, name = "ui4"),
    #path('uiL/',views.Listar_Municipios, name = "listar"),
    path('actualizar_Mun/<int:id>/', views.Actualizar_Municipio, name='actualizar_Mun'),
    path('deleteMun/<int:id>/', views.Eliminar_Municipio, name="delete_mun"),
    path('detailsMun/<int:id>/', views.detalles_Municipio, name="md"),

    path('base/',views.base, name = "base"),


    path('logout/',views.exit, name = "exitt"),   
]
