from django.contrib import admin
from .models import (
    Navio, Cubierta, Camarote, Tripulante, Puerto, Itinerario,
    Escala, Viaje, Pasajero, Perfil,
)


@admin.register(Navio)
class NavioAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "clasificacion", "max_pasajeros")
    search_fields = ("codigo", "nombre")


@admin.register(Cubierta)
class CubiertaAdmin(admin.ModelAdmin):
    list_display = ("navio", "numero", "encargado")
    list_filter = ("navio",)


@admin.register(Camarote)
class CamaroteAdmin(admin.ModelAdmin):
    list_display = ("numero", "cubierta", "tipo", "ubicacion")
    list_filter = ("ubicacion", "cubierta__navio")


@admin.register(Tripulante)
class TripulanteAdmin(admin.ModelAdmin):
    list_display = ("legajo", "nombre", "puesto", "navio", "jefe")
    search_fields = ("legajo", "nombre")


@admin.register(Puerto)
class PuertoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ciudad", "pais")


@admin.register(Itinerario)
class ItinerarioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria")
    list_filter = ("categoria",)


@admin.register(Escala)
class EscalaAdmin(admin.ModelAdmin):
    list_display = ("itinerario", "numero_escala", "puerto")


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ("navio", "itinerario", "fecha", "duracion", "get_categoria")
    list_filter = ("itinerario__categoria", "navio")

    @admin.display(description="Categoría", ordering="itinerario__categoria")
    def get_categoria(self, obj):
        return obj.itinerario.categoria


@admin.register(Pasajero)
class PasajeroAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo_documento", "numero_documento", "pais_procedencia")
    search_fields = ("nombre", "numero_documento")


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "pasajero")