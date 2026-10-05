from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('registro/', views.registro_pasajero, name='registro_pasajero'),
    path('crear-tripulante/', views.crear_tripulante, name='crear_tripulante'),
]