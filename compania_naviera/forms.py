
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import (
    Pasajero,
    Viaje,
    Camarote,
    Reserva,
    Navio,
    Tripulante
)


class RegistroPasajeroForm(UserCreationForm):

    email = forms.EmailField(
        label="Correo electrónico"
    )

    tipo_documento = forms.ChoiceField(
        choices=[
            ('DNI', 'DNI'),
            ('PASAPORTE', 'Pasaporte'),
            ('CEDULA', 'Cédula'),
        ],
        label="Tipo de documento"
    )

    numero_documento = forms.CharField(
        label="Número de documento",
        max_length=30
    )

    nombre = forms.CharField(
        label="Nombre completo",
        max_length=100
    )

    pais_procedencia = forms.CharField(
        label="País de procedencia",
        max_length=100
    )

    ciudad_procedencia = forms.CharField(
        label="Ciudad de procedencia",
        max_length=100
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

class ReservaForm(forms.Form):

    viaje = forms.ModelChoiceField(
        queryset=Viaje.objects.select_related(
            'navio', 'itinerario'
        ).all().order_by('fecha'),
        label="Seleccionar viaje"
    )

    camarote = forms.ModelChoiceField(
        queryset=Camarote.objects.all().order_by('numero'),
        label="Seleccionar camarote"
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        viaje_id = self.data.get('viaje') or self.initial.get('viaje')

        if viaje_id:
            try:
                viaje = Viaje.objects.get(pk=viaje_id)

                ocupados = Reserva.objects.filter(
                    viaje=viaje,
                    estado__in=['PENDIENTE', 'CONFIRMADA']
                ).values_list('camarote_id', flat=True)

                self.fields['camarote'].queryset = (
                    Camarote.objects.filter(
                        cubierta__navio=viaje.navio
                    ).exclude(
                        pk__in=ocupados
                    ).order_by('numero')
                )

            except (Viaje.DoesNotExist, ValueError, TypeError):
                self.fields['camarote'].queryset = Camarote.objects.none()

    def clean(self):

        cleaned_data = super().clean()

        viaje = cleaned_data.get('viaje')
        camarote = cleaned_data.get('camarote')

        if viaje and camarote:

            if camarote.cubierta.navio_id != viaje.navio_id:

                self.add_error(
                    'camarote',
                    'El camarote no pertenece al navío de este viaje.'
                )

            elif Reserva.objects.filter(
                viaje=viaje,
                camarote=camarote,
                estado__in=['PENDIENTE', 'CONFIRMADA']
            ).exists():

                self.add_error(
                    'camarote',
                    'Ese camarote ya no está disponible.'
                )

        return cleaned_data


class RegistroTripulanteForm(forms.Form):

    username = forms.CharField(max_length=150)

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    email = forms.EmailField(required=False)

    legajo = forms.CharField(max_length=20)

    nombre = forms.CharField(max_length=100)

    puesto = forms.CharField(max_length=100)

    codigo_navio = forms.ModelChoiceField(
        queryset=Navio.objects.all(),
        required=False
    )

    legajo_jefe = forms.ModelChoiceField(
        queryset=Tripulante.objects.all(),
        required=False
    )
