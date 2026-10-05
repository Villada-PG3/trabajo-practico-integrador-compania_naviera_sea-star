from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import (
    Camarote,
    Cubierta,
    Escala,
    Itinerario,
    Navio,
    Pasajero,
    Perfil,
    Puerto,
    Reserva,
    Tripulante,
    Viaje,
)


# Configuración del Perfil dentro del Usuario de Django
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'


class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)


# Re-registrar Usuario con su Inline
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Registro único de Perfil
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'pasajero', 'tripulante')
    list_filter = ('rol',)


# Registro del resto de entidades del ER
@admin.register(Navio)
class NavioAdmin(admin.ModelAdmin):
    list_display = (
        'codigo_navio',
        'nombre',
        'cantidad_maxima_pasajeros',
        'clasificacion',
        'activo',
    )
    list_filter = ('clasificacion', 'activo')
    search_fields = ('codigo_navio', 'nombre')


@admin.register(Cubierta)
class CubiertaAdmin(admin.ModelAdmin):
    list_display = ('navio', 'numero_cubierta', 'encargado')
    list_filter = ('navio',)
    search_fields = ('numero_cubierta', 'encargado', 'navio__nombre')


@admin.register(Camarote)
class CamaroteAdmin(admin.ModelAdmin):
    list_display = ('cubierta', 'numero_camarote', 'tipo', 'ubicacion')
    list_filter = ('ubicacion', 'tipo', 'cubierta__navio')
    search_fields = ('numero_camarote', 'cubierta__navio__nombre')


@admin.register(Tripulante)
class TripulanteAdmin(admin.ModelAdmin):
    list_display = ('legajo', 'nombre', 'puesto', 'navio', 'jefe', 'activo')
    list_filter = ('puesto', 'activo', 'navio')
    search_fields = ('legajo', 'nombre', 'puesto')


@admin.register(Itinerario)
class ItinerarioAdmin(admin.ModelAdmin):
    list_display = ('codigo_itinerario', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('codigo_itinerario',)


@admin.register(Puerto)
class PuertoAdmin(admin.ModelAdmin):
    list_display = ('codigo_puerto', 'nombre')
    search_fields = ('codigo_puerto', 'nombre')


@admin.register(Escala)
class EscalaAdmin(admin.ModelAdmin):
    list_display = ('itinerario', 'numero_escala', 'puerto')
    list_filter = ('itinerario', 'puerto')
    search_fields = ('itinerario__codigo_itinerario', 'puerto__nombre')


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = (
        'codigo_viaje',
        'navio',
        'itinerario',
        'fecha_viaje',
        'duracion',
    )
    list_filter = ('fecha_viaje', 'navio', 'itinerario')
    search_fields = ('codigo_viaje', 'navio__nombre')


@admin.register(Pasajero)
class PasajeroAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'tipo_documento',
        'numero_documento',
        'pais_procedencia',
        'ciudad_procedencia',
    )
    list_filter = ('pais_procedencia', 'tipo_documento')
    search_fields = ('nombre', 'numero_documento')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'codigo_reserva',
        'pasajero',
        'viaje',
        'camarote',
        'fecha_creacion',
        'activo',
    )
    list_filter = ('activo', 'fecha_creacion', 'viaje')
    search_fields = (
        'codigo_reserva',
        'pasajero__nombre',
        'pasajero__numero_documento',
    )