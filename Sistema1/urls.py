
from django.urls import path
from Sistema1 import views 

urlpatterns = [

    #Log
    path('base/',views.base, name = "base"),
    path('logout/',views.exit, name = "exitt"),   
    path('login/', views.Login_Template, name = "login"),
    path('register/', views.Register_Template, name = "register"),
    path('',views.Home, name = "Home"),    
    path('perfil/',views.vista_perfil, name = "perfil"),    
    
    #convenios
    path('addConv/',views.Agregar_Convenios, name = "addConv"),
    path('ver_convenio/<str:nombre_archivo>/', views.ver_convenio, name='ver_convenio'),
    path('actualizar_Conv/<int:id>/', views.Actualizar_Convenio, name='actualizar_Conv'),
    path('eliminar_Conv/<int:id>/', views.Eliminar_Convenios, name='eliminar_Conv'),
    path('convenio/<int:id>/historial/', views.Ver_Historial_Convenio, name='ver_historial_convenio'),  
    path('ui1/<int:id>/', views.Ver_Historial_Convenio, name='H_convenio'),

    #Municipios
    path('Mun_List/',views.Listar_Municipios, name = "Mun_List"),
    path('Agregar_Mun/',views.Agregar_Mun, name = "Agregar_Mun"),
    path('actualizar_Mun/<int:id>/', views.Actualizar_Municipio, name='actualizar_Mun'),
    path('deleteMun/<int:id>/', views.Eliminar_Municipio, name="delete_mun"),
    path('detailsMun/<int:id>/', views.detalles_Municipio, name="md"),
    #Rendiciones
    path('rendiciones/',views.Lista_Rendiciones, name = "rendiciones"),
    path('agregar_rendicion',views.Agregar_Rendiciones, name='agregar_rendicion'),



]
