from django import forms
from .models import Navio, Tripulante


# Formulario para autoregistro de Pasajeros
class RegistroPasajeroForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    email = forms.EmailField(label="Correo electrónico")

    TIPO_DOC_CHOICES = [
        ('DNI', 'DNI'),
        ('PASAPORTE', 'Pasaporte'),
        ('CEDULA', 'Cédula'),
    ]
    tipo_documento = forms.ChoiceField(
        choices=TIPO_DOC_CHOICES, label="Tipo de Documento"
    )
    numero_documento = forms.CharField(
        label="Número de Documento", max_length=50
    )
    nombre = forms.CharField(label="Nombre Completo", max_length=100)
    pais_procedencia = forms.CharField(
        label="País de Procedencia", max_length=100
    )
    ciudad_procedencia = forms.CharField(
        label="Ciudad de Procedencia", max_length=100
    )


# Formulario para que el Admin cree Tripulantes
class RegistroTripulanteForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    email = forms.EmailField(label="Correo electrónico", required=False)

    legajo = forms.CharField(label="Legajo", max_length=20)
    nombre = forms.CharField(label="Nombre Completo", max_length=100)
    puesto = forms.CharField(label="Puesto", max_length=100)

    codigo_navio = forms.ModelChoiceField(
        queryset=Navio.objects.all(), label="Navío Asignado", required=False
    )
    legajo_jefe = forms.ModelChoiceField(
        queryset=Tripulante.objects.all(), label="Jefe Directo", required=False
    )