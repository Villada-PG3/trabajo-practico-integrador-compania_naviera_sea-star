from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    # NAVIOS
    path(
        'navios/',
        views.NavioListView.as_view(),
        name='navios'
    ),

    path(
        'navios/<int:pk>/',
        views.NavioDetailView.as_view(),
        name='navio_detail'
    ),

    # ITINERARIOS
    path(
        'itinerarios/',
        views.ItinerarioListView.as_view(),
        name='itinerarios'
    ),

    # CRUCEROS
    path(
        'cruceros/',
        views.CruceroListView.as_view(),
        name='cruceros'
    ),

    # USUARIOS
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),

    # CUENTA
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),

    # RESERVAS
    path('reservar/', views.solicitar_reserva, name='reservar'),

    # NOTIFICACIONES
    path(
        'notificacion/<int:id>/',
        views.leer_notificacion,
        name='leer_notificacion'
    ),

]