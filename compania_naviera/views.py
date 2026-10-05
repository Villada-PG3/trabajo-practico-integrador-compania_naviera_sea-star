from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import RegistroPasajeroForm, RegistroTripulanteForm
from .models import Pasajero, Perfil, Tripulante


def home(request):
    return render(request, "home.html")


def panel_admin(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.perfil.rol != 'ADMIN':
        return redirect('home')

    return render(request, 'panel_admin.html')


# 1. Registro público de Pasajeros
def registro_pasajero(request):
    if request.method == 'POST':
        form = RegistroPasajeroForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )

            pasajero = Pasajero.objects.create(
                tipo_documento=form.cleaned_data['tipo_documento'],
                numero_documento=form.cleaned_data['numero_documento'],
                nombre=form.cleaned_data['nombre'],
                pais_procedencia=form.cleaned_data['pais_procedencia'],
                ciudad_procedencia=form.cleaned_data['ciudad_procedencia'],
            )

            Perfil.objects.create(user=user, rol='PASAJERO', pasajero=pasajero)

            return redirect('login')
    else:
        form = RegistroPasajeroForm()

    return render(request, 'registro_pasajero.html', {'form': form})


# 2. Creación de Tripulantes (Exclusivo para el Admin)
@login_required
def crear_tripulante(request):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('home')

    if request.method == 'POST':
        form = RegistroTripulanteForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )

            # Corregido: navio y jefe coinciden con los nombres del modelo Tripulante
            tripulante = Tripulante.objects.create(
                legajo=form.cleaned_data['legajo'],
                nombre=form.cleaned_data['nombre'],
                puesto=form.cleaned_data['puesto'],
                navio=form.cleaned_data['codigo_navio'],
                jefe=form.cleaned_data['legajo_jefe'],
            )

            Perfil.objects.create(
                user=user, rol='TRIPULANTE', tripulante=tripulante
            )

            return redirect('home')
    else:
        form = RegistroTripulanteForm()

    return render(request, 'crear_tripulante.html', {'form': form})