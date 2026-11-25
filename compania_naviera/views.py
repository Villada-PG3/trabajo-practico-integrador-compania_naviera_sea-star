
from sqlite3 import IntegrityError

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView

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


# =====================================
# VISTAS BASADAS EN CLASES
# =====================================

# LISTAR NAVIOS

class NavioListView(ListView):

    model = Navio
    template_name = 'navios.html'
    context_object_name = 'navios'

    def get_queryset(self):

        return Navio.objects.all().order_by('nombre')


# DETALLE DE UN NAVIO

class NavioDetailView(DetailView):

    model = Navio
    template_name = 'navio_detail.html'
    context_object_name = 'navio'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Detalles del navío'

        return context


# LISTAR ITINERARIOS

class ItinerarioListView(ListView):

    model = Itinerario
    template_name = 'itinerarios.html'
    context_object_name = 'itinerarios'

    def get_queryset(self):

        return Itinerario.objects.all().order_by('nombre')


# LISTAR CRUCEROS

class CruceroListView(ListView):

    model = Viaje
    template_name = 'cruceros.html'
    context_object_name = 'viajes'

    def get_queryset(self):

        return Viaje.objects.select_related(
            'navio',
            'itinerario'
        ).order_by('fecha')


# =====================================
# INICIO
# =====================================

def home(request):

    return render(request, 'home.html')


# =====================================
# REGISTRO DE PASAJEROS
# =====================================

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


# =====================================
# INICIAR SESION
# =====================================

def iniciar_sesion(request):

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

    return render(request, 'login.html')


# =====================================
# CERRAR SESION
# =====================================

@login_required
def cerrar_sesion(request):

    logout(request)

    return redirect('login')


# =====================================
# MI CUENTA
# =====================================

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
        'cuenta.html',
        {
            'perfil': perfil,
            'tickets': tickets,
            'reservas': reservas,
            'notificaciones': notificaciones
        }
    )


# =====================================
# SOLICITAR RESERVA
# =====================================

@login_required
def solicitar_reserva(request):

    perfil = get_object_or_404(
        Perfil,
        usuario=request.user
    )

    viajes = Viaje.objects.select_related(
        'navio',
        'itinerario'
    ).order_by('fecha')

    viaje_id = request.GET.get('viaje') or request.POST.get('viaje_id')

    viaje = None
    camarotes = []
    camarote_seleccionado = None

    if viaje_id:

        viaje = get_object_or_404(
            Viaje.objects.select_related('navio', 'itinerario'),
            id=viaje_id
        )

        camarotes = list(
            Camarote.objects.filter(
                cubierta__navio=viaje.navio
            ).select_related(
                'cubierta',
                'cubierta__navio'
            ).order_by(
                'cubierta__numero',
                'ubicacion',
                'numero'
            )
        )

        ocupados = set(
            Reserva.objects.filter(
                viaje=viaje,
                estado__in=['PENDIENTE', 'CONFIRMADA']
            ).values_list(
                'camarote_id',
                flat=True
            )
        )

        for camarote in camarotes:
            camarote.ocupado = camarote.id in ocupados

        if request.method == 'POST':

            camarote_id = request.POST.get('camarote_id')

            camarote_seleccionado = next(
                (
                    c for c in camarotes
                    if str(c.id) == str(camarote_id)
                ),
                None
            )

            if camarote_seleccionado is None:

                messages.error(
                    request,
                    'Seleccioná un camarote válido.'
                )

            elif camarote_seleccionado.ocupado:

                messages.error(
                    request,
                    'Ese camarote ya no está disponible.'
                )

            else:
                try:

                    Reserva.objects.create(
                        pasajero=perfil.pasajero,
                        viaje=viaje,
                        camarote=camarote_seleccionado,
                        estado='PENDIENTE'
                    )

                    messages.success(
                        request,
                        'Tu solicitud fue enviada al administrador.'
                    )

                    return redirect('mi_cuenta')

                except IntegrityError:

                    messages.error(
                        request,
                        'Otro pasajero acaba de reservar ese camarote.'
                    )

                    camarote_seleccionado.ocupado = True

    return render(
        request,
        'camarotes.html',
        {
            'viajes': viajes,
            'viaje': viaje,
            'camarotes': camarotes,
            'camarote_seleccionado': camarote_seleccionado
        }
    )



# =====================================
# LEER NOTIFICACION
# =====================================

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