
from django.urls import path
from Sistema1 import views 

urlpatterns = [
    path('login/', views.Login_Template, name = "login"),


    path('',views.Ui2, name = "Ui2"),
    path('ui1/',views.Inicio, name = "Ui1"),
    path('ui3/',views.Listar_Municipios, name = "ui3"),
    path('addConv/',views.Agregar_Convenios, name = "addConv"),
    path('detailsMun/<int:id>/', views.detalles_Municipio, name="md"),
    path('ver_convenio/<str:nombre_archivo>/', views.ver_convenio, name='ver_convenio'),
    path('ui4/',views.Ui4, name = "ui4"),
    path('uiL/',views.Listar_Municipios, name = "listar"),

    path('base/',views.base, name = "base"),


    path('logout/',views.exit, name = "exitt"),   
]
