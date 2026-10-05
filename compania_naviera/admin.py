from django.contrib import admin
from django.urls import path
from compania_naviera import views
from django.contrib import admin
from .models import (
    Navio,
    Cubierta,
    Camarote,
    Tripulante,
    Puerto,
    Itinerario,
    Escala,
    Viaje,
    Pasajero,
    Reserva,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
]

admin.site.register(Navio)
admin.site.register(Cubierta)
admin.site.register(Camarote)
admin.site.register(Tripulante)
admin.site.register(Puerto)
admin.site.register(Itinerario)
admin.site.register(Escala)
admin.site.register(Viaje)
admin.site.register(Pasajero)
admin.site.register(Reserva)