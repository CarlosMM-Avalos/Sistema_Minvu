
from django.urls import path
from Sistema1 import views 

urlpatterns = [

    #Log
    path('base/',views.base, name = "base"),
    path('logout/',views.exit, name = "exitt"),   
    path('login/', views.Login_Template, name = "login"),
    path('register/', views.Register_Template, name = "register"),
    path('home/',views.Home, name = "Home"),    
    path('perfil/',views.perfil, name = "perfil"),    
    path('perfil/update_username/', views.update_username, name='update_username'),
    path('perfil/change_password/', views.change_password, name='change_password'),
    
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
    path('rendiciones/<int:id>/',views.rendiciones_view, name = "rendiciones"),
    path('agregar_rendicion',views.Agregar_Rendiciones, name='agregar_rendicion'),
    #dashboard
    path('dashboard/',views.dashboard_view, name = "dashboard"),
    path('dashboard2/',views.dashboard_view2, name = "dashboard2"),
    path('dashboard3/',views.dashboard_view3, name = "dashboard3"),
    path('dashboard4/',views.dashboard_view4, name = "dashboard4"),
    #programas
    path('',views.programas_view, name = "programas"),
    path('detallesProgramas/<int:id>/',views.programas_detalles, name = "dprogramas"),
    #reintehros
    path('lreintegros/',views.Listar_Reintegros, name = "Listar_Reintegros"),
    path('areintegros/',views.Agregar_Reintegros, name = "Agregar_Reintegros"),
    path('acreintegros/<int:id>/',views.Actualizar_Reintegros, name = "Actualizar_Reintegros"),
    path('breintegros/<int:id>/',views.borrar_Reintegros, name = "breintegro"),
    path('detailsReint/<int:id>/', views.detalles_Reintegro, name="rd"),
    #prueba
    path('prueba/', views.prueba, name="prueba"),
    path('notificaciones/marcar-leida/<int:id>/', views.marcar_notificacion_como_leida, name='marcar_leida'),
    path('notificaciones/', views.lista_notificaciones, name='lista_notificaciones'),


]
