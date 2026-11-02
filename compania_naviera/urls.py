from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('navios/', views.navios, name='navios'),
    path('itinerarios/', views.itinerarios, name='itinerarios'),
    path('cruceros/', views.cruceros, name='cruceros'),

    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('reservar/', views.solicitar_reserva, name='reservar'),
    path('notificacion/<int:id>/', views.leer_notificacion, name='leer_notificacion'),
]