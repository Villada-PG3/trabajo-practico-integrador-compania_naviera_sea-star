
from django.contrib import admin
from .models import (
    Navio, Cubierta, Camarote, Tripulante, Puerto,
    Itinerario, Escala, Viaje, Pasajero, Perfil,
    Reserva, Ticket, Notificacion
)


# CONFIGURACIÓN GENERAL

admin.site.site_header = "SEA STAR | Administración"
admin.site.site_title = "SEA STAR"
admin.site.index_title = "Centro de gestión de la compañía"


# NAVÍOS

@admin.register(Navio)
class NavioAdmin(admin.ModelAdmin):
    list_display = (
        "codigo", "nombre", "clasificacion", "max_pasajeros"
    )
    search_fields = ("codigo", "nombre")
    list_filter = ("clasificacion",)
    ordering = ("nombre",)
    list_per_page = 15


# CUBIERTAS

@admin.register(Cubierta)
class CubiertaAdmin(admin.ModelAdmin):
    list_display = ("navio", "numero", "encargado")
    list_filter = ("navio",)
    search_fields = ("encargado", "navio__nombre")
    list_per_page = 15


# CAMAROTES

@admin.register(Camarote)
class CamaroteAdmin(admin.ModelAdmin):
    list_display = ("numero", "cubierta", "tipo", "ubicacion")
    list_filter = ("ubicacion", "tipo", "cubierta__navio")
    search_fields = ("numero", "cubierta__navio__nombre")
    list_per_page = 20


# TRIPULANTES

@admin.register(Tripulante)
class TripulanteAdmin(admin.ModelAdmin):
    list_display = ("legajo", "nombre", "puesto", "navio", "jefe")
    list_filter = ("puesto", "navio")
    search_fields = ("legajo", "nombre", "puesto")
    list_per_page = 20


# PUERTOS

@admin.register(Puerto)
class PuertoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ciudad", "pais")
    list_filter = ("pais",)
    search_fields = ("nombre", "ciudad", "pais")
    ordering = ("pais", "ciudad")
    list_per_page = 20


# ITINERARIOS

@admin.register(Itinerario)
class ItinerarioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria")
    list_filter = ("categoria",)
    search_fields = ("nombre",)
    list_per_page = 15


# ESCALAS

@admin.register(Escala)
class EscalaAdmin(admin.ModelAdmin):
    list_display = ("itinerario", "numero_escala", "puerto")
    list_filter = ("itinerario",)
    search_fields = ("itinerario__nombre", "puerto__nombre")
    list_per_page = 20


# VIAJES

@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = (
        "navio", "itinerario", "fecha",
        "duracion", "get_categoria"
    )
    list_filter = ("itinerario__categoria", "navio")
    search_fields = ("navio__nombre", "itinerario__nombre")
    date_hierarchy = "fecha"
    ordering = ("fecha",)
    list_per_page = 20

    @admin.display(
        description="Categoría",
        ordering="itinerario__categoria"
    )
    def get_categoria(self, obj):
        return obj.itinerario.categoria


# PASAJEROS

@admin.register(Pasajero)
class PasajeroAdmin(admin.ModelAdmin):
    list_display = (
        "nombre", "tipo_documento",
        "numero_documento", "pais_procedencia"
    )
    list_filter = ("pais_procedencia",)
    search_fields = ("nombre", "numero_documento")
    list_per_page = 20


# PERFILES

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "pasajero")
    search_fields = ("usuario__username", "pasajero__nombre")
    list_per_page = 20


# RESERVAS

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        "pasajero", "viaje", "camarote",
        "estado", "fecha_solicitud"
    )
    list_filter = ("estado", "viaje__fecha")
    search_fields = (
        "pasajero__nombre",
        "pasajero__numero_documento",
        "viaje__navio__nombre"
    )
    date_hierarchy = "fecha_solicitud"
    readonly_fields = ("fecha_solicitud",)
    ordering = ("-fecha_solicitud",)
    list_per_page = 20


# TICKETS

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("codigo", "reserva", "fecha_emision")
    search_fields = (
        "codigo",
        "reserva__pasajero__nombre"
    )
    readonly_fields = ("codigo", "fecha_emision")
    date_hierarchy = "fecha_emision"
    list_per_page = 20


# NOTIFICACIONES

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ("pasajero", "mensaje", "fecha", "leida")
    list_filter = ("leida", "fecha")
    search_fields = ("pasajero__nombre", "mensaje")
    readonly_fields = ("fecha",)
    date_hierarchy = "fecha"
    list_per_page = 20
