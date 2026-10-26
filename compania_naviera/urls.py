from django.urls import path
from compania_naviera import views

urlpatterns = [
    path("", views.home, name="home"),

    path("navios/", views.navios, name="navios"),

    path("itinerarios/", views.itinerarios, name="itinerarios"),

    path("cruceros/", views.cruceros, name="cruceros"),
]
