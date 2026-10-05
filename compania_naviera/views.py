from django.shortcuts import render
from django.shortcuts import render
from .models import Navio, Itinerario, Viaje

def home(request):
    return render(request, "home.html")

def home(request):
    return render(request, "home.html")


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
