
from django.contrib import admin, messages

from .models import Reserva, Ticket, Notificacion

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'pasajero',
        'viaje',
        'camarote',
        'estado',
        'fecha_solicitud'
    )

    list_filter = ('estado', 'viaje')
    search_fields = (
        'pasajero__nombre',
        'pasajero__numero_documento'
    )

    actions = [
        'aprobar_reservas',
        'rechazar_reservas'
    ]

    @admin.action(description="Aprobar reservas y emitir tickets")
    def aprobar_reservas(self, request, queryset):

        for reserva in queryset:

            if reserva.estado == 'CANCELADA':
                continue

            reserva.estado = 'CONFIRMADA'
            reserva.save()

            ticket, creado = Ticket.objects.get_or_create(
                reserva=reserva
            )

            if creado:
                Notificacion.objects.create(
                    pasajero=reserva.pasajero,
                    mensaje=(
                        f'Tu reserva para el viaje {reserva.viaje} '
                        f'fue confirmada. Tu código de ticket es '
                        f'{ticket.codigo}.'
                    )
                )

        self.message_user(
            request,
            'Reservas aprobadas y tickets emitidos.',
            messages.SUCCESS
        )

    @admin.action(description="Rechazar reservas")
    def rechazar_reservas(self, request, queryset):

        for reserva in queryset:

            if reserva.estado == 'PENDIENTE':

                reserva.estado = 'CANCELADA'
                reserva.save()

                Notificacion.objects.create(
                    pasajero=reserva.pasajero,
                    mensaje=(
                        f'Tu solicitud para el viaje '
                        f'{reserva.viaje} fue rechazada.'
                    )
                )

        self.message_user(
            request,
            'Reservas rechazadas.',
            messages.WARNING
        )

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    list_display = (
        'codigo',
        'reserva',
        'fecha_emision'
    )

    search_fields = (
        'codigo',
        'reserva__pasajero__nombre'
    )

    readonly_fields = (
        'codigo',
        'fecha_emision'
    )


# ==========================================
# ADMINISTRAR NOTIFICACIONES
# ==========================================

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):

    list_display = (
        'pasajero',
        'mensaje',
        'fecha',
        'leida'
    )

    list_filter = ('leida', 'fecha')
    search_fields = ('pasajero__nombre', 'mensaje')
