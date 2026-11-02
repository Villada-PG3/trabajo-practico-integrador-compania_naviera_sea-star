from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import (
    Pasajero,
    Perfil,
    Reserva,
    Ticket,
    Notificacion,
    Viaje,
    Navio,
    Itinerario,
    Camarote,

)

from .forms import (
    RegistroPasajeroForm,
    ReservaForm
)
def home(request):
    return render(request, 'home.html')

def navios(request):
    navios = Navio.objects.all()

    return render(request, "navios.html", {
        "navios": navios
    })


def itinerarios(request):
    itinerarios = Itinerario.objects.all()

    return render(request, "itinerarios.html", {
        "itinerarios": itinerarios
    })


def cruceros(request):
    viajes = Viaje.objects.all()

    return render(request, "cruceros.html", {
        "viajes": viajes
    })

def registro(request):

    if request.method == 'POST':

        form = RegistroPasajeroForm(request.POST)

        if form.is_valid():

            usuario = form.save(commit=False)
            usuario.email = form.cleaned_data['email']
            usuario.save()

            pasajero = Pasajero.objects.create(
                tipo_documento=form.cleaned_data['tipo_documento'],
                numero_documento=form.cleaned_data['numero_documento'],
                nombre=form.cleaned_data['nombre'],
                pais_procedencia=form.cleaned_data['pais_procedencia'],
                ciudad_procedencia=form.cleaned_data['ciudad_procedencia']
            )

            Perfil.objects.create(
                usuario=usuario,
                pasajero=pasajero
            )

            login(request, usuario)

            messages.success(
                request,
                'Tu cuenta fue creada correctamente.'
            )

            return redirect('mi_cuenta')

    else:
        form = RegistroPasajeroForm()

    return render(
        request,
        'registro.html',
        {'form': form}
    )


def iniciar_sesion(request):

    from django.contrib.auth import authenticate

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:

            if hasattr(usuario, 'perfil'):
                login(request, usuario)
                return redirect('mi_cuenta')

            messages.error(
                request,
                'Esta cuenta no tiene un perfil de pasajero.'
            )

        else:
            messages.error(
                request,
                'Usuario o contraseña incorrectos.'
            )

    return render(
        request,
        'login.html'
    )


@login_required
def cerrar_sesion(request):

    logout(request)

    return redirect('login')



@login_required
def mi_cuenta(request):

    perfil = get_object_or_404(
        Perfil,
        usuario=request.user
    )

    tickets = Ticket.objects.filter(
        reserva__pasajero=perfil.pasajero
    ).select_related(
        'reserva__viaje__navio',
        'reserva__viaje__itinerario',
        'reserva__camarote'
    )

    reservas = Reserva.objects.filter(
        pasajero=perfil.pasajero
    ).select_related(
        'viaje',
        'camarote'
    )

    notificaciones = Notificacion.objects.filter(
        pasajero=perfil.pasajero
    ).order_by('-fecha')

    return render(
        request,
        'mi_cuenta.html',
        {
            'perfil': perfil,
            'tickets': tickets,
            'reservas': reservas,
            'notificaciones': notificaciones
        }
    )

    
@login_required
def solicitar_reserva(request):

    perfil = get_object_or_404(
        Perfil,
        usuario=request.user
    )

    if request.method == 'POST':

        form = ReservaForm(request.POST)

        if form.is_valid():

            viaje = form.cleaned_data['viaje']
            camarote = form.cleaned_data['camarote']

            reserva = Reserva(
                pasajero=perfil.pasajero,
                viaje=viaje,
                camarote=camarote
            )

            try:
                reserva.save()

                messages.success(
                    request,
                    'Tu solicitud fue enviada al administrador.'
                )

                return redirect('mi_cuenta')

            except Exception:
                messages.error(
                    request,
                    'Ese camarote ya no está disponible para este viaje.'
                )

    else:
        form = ReservaForm()

    return render(
        request,
        'reservar.html',
        {'form': form}
    )
@login_required
def leer_notificacion(request, id):

    perfil = get_object_or_404(
        Perfil,
        usuario=request.user
    )

    notificacion = get_object_or_404(
        Notificacion,
        id=id,
        pasajero=perfil.pasajero
    )

    notificacion.leida = True
    notificacion.save()

    return redirect('mi_cuenta') 