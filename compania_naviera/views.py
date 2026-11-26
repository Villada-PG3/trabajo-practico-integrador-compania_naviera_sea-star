
from django.db import IntegrityError
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
    Cubierta,
)

from .forms import (
    RegistroPasajeroForm,
    ReservaForm
)


# =====================================
# PLANO DEL NAVIO
# =====================================

def armar_plano(navio, ocupados=None):
    """
    Arma la información para dibujar el plano del navío:
    una lista de cubiertas, cada una con sus camarotes separados
    por ubicación (Babor, Crujía, Estribor) y sus instalaciones.
    'ocupados' es un conjunto con los id de camarotes ya reservados.
    """

    if ocupados is None:
        ocupados = set()

    cubiertas = Cubierta.objects.filter(
        navio=navio
    ).prefetch_related(
        'camarote_set',
        'instalaciones'
    ).order_by('numero')

    plano = []

    for cubierta in cubiertas:

        camarotes = sorted(
            cubierta.camarote_set.all(),
            key=lambda c: c.numero
        )

        for camarote in camarotes:
            camarote.ocupado = camarote.id in ocupados

        zonas = []

        for ubicacion, nombre in Camarote.UBICACIONES:
            zonas.append({
                'nombre': nombre,
                'camarotes': [
                    c for c in camarotes if c.ubicacion == ubicacion
                ],
            })

        plano.append({
            'cubierta': cubierta,
            'zonas': zonas,
            'instalaciones': cubierta.instalaciones.all(),
        })

    return plano


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

        context['plano'] = armar_plano(self.object)

        context['instalaciones'] = self.object.instalaciones.all()

        # Un camarote de ejemplo por cada tipo, para mostrar sus fotos
        tipos = {}

        for camarote in Camarote.objects.filter(
            cubierta__navio=self.object
        ).order_by('numero'):

            if camarote.tipo not in tipos or (
                camarote.imagen and not tipos[camarote.tipo].imagen
            ):
                tipos[camarote.tipo] = camarote

        context['tipos_camarote'] = tipos.values()

        return context


# LISTAR ITINERARIOS

class ItinerarioListView(ListView):

    model = Itinerario
    template_name = 'itinerarios.html'
    context_object_name = 'itinerarios'

    def get_queryset(self):

        return Itinerario.objects.prefetch_related(
            'escala_set__puerto'
        ).order_by('nombre')


# DETALLE DE UN ITINERARIO (MAPA DE LA RUTA)

class ItinerarioDetailView(DetailView):

    model = Itinerario
    template_name = 'itinerario_detail.html'
    context_object_name = 'itinerario'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        escalas = self.object.escala_set.select_related('puerto')

        # Datos de cada parada que usa el mapa (JavaScript)
        paradas = []

        for escala in escalas:

            puerto = escala.puerto

            if puerto.latitud is None or puerto.longitud is None:
                continue

            paradas.append({
                'escala': escala.numero_escala,
                'nombre': puerto.nombre,
                'ciudad': puerto.ciudad,
                'pais': puerto.pais,
                'lat': float(puerto.latitud),
                'lng': float(puerto.longitud),
                'imagen': puerto.imagen.url if puerto.imagen else '',
            })

        context['escalas'] = escalas
        context['paradas'] = paradas
        context['viajes'] = self.object.viaje_set.select_related(
            'navio'
        ).order_by('fecha')

        return context


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

    navios = Navio.objects.all().order_by('nombre')

    return render(
        request,
        'home.html',
        {'navios': navios}
    )


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
    plano = []
    camarote_seleccionado = None

    if viaje_id:

        viaje = get_object_or_404(
            Viaje.objects.select_related('navio', 'itinerario'),
            id=viaje_id
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

        plano = armar_plano(viaje.navio, ocupados)

        # Lista plana de todos los camarotes del navío
        camarotes = [
            c
            for cubierta in plano
            for zona in cubierta['zonas']
            for c in zona['camarotes']
        ]

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
        'reserva.html',
        {
            'viajes': viajes,
            'viaje': viaje,
            'plano': plano,
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