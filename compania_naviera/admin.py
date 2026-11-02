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


# Configuración para editar el Perfil directamente dentro del Usuario de Django
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil de Rol'


class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)


# Re-registrar Usuario con su Inline de Perfil
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Registro del modelo Perfil
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'pasajero', 'tripulante')
    list_filter = ('rol',)


# Registro del resto de modelos del negocio
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