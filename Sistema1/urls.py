
from django.urls import path
from Sistema1 import views 

urlpatterns = [
    path('login/', views.Login_Template, name = "login"),


    path('',views.Ui2, name = "Ui2"),
    path('ui1/',views.Inicio, name = "Ui1"),
    path('ui3/',views.Ui3, name = "ui3"),
    path('ui4/',views.Ui4, name = "ui4"),

    path('base/',views.base, name = "base"),


    path('logout/',views.exit, name = "exitt"),   
]
