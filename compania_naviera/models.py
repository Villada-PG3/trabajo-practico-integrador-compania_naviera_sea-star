from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
import uuid

class Navio(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    altura = models.DecimalField(max_digits=10, decimal_places=2)
    eslora = models.DecimalField(max_digits=10, decimal_places=2)
    manga = models.DecimalField(max_digits=10, decimal_places=2)
    desplazamiento = models.DecimalField(max_digits=12, decimal_places=2)
    autonomia = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad_camarotes = models.IntegerField()
    max_pasajeros = models.IntegerField()
    cantidad_motores = models.IntegerField()
    cantidad_tripulantes = models.IntegerField()
    clasificacion = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Cubierta(models.Model):
    navio = models.ForeignKey(Navio, on_delete=models.CASCADE)
    numero = models.CharField(max_length=10)
    encargado = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        unique_together = ('navio', 'numero')

    def __str__(self):
        return f"{self.navio.nombre} - Cubierta {self.numero}"


class Camarote(models.Model):
    UBICACIONES = [
        ('Babor', 'Babor'),
        ('Crujía', 'Crujía'),
        ('Estribor', 'Estribor'),
    ]

    cubierta = models.ForeignKey(Cubierta, on_delete=models.CASCADE)
    numero = models.CharField(max_length=10)
    tipo = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=20, choices=UBICACIONES)

    def __str__(self):
        return f"Camarote {self.numero} - {self.cubierta}"


class Tripulante(models.Model):
    legajo = models.CharField(max_length=20, unique=True)
    navio = models.ForeignKey(Navio, on_delete=models.CASCADE)
    puesto = models.CharField(max_length=100)
    jefe = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.puesto}"


class Puerto(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"


class Itinerario(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Escala(models.Model):
    itinerario = models.ForeignKey(Itinerario, on_delete=models.CASCADE)
    puerto = models.ForeignKey(Puerto, on_delete=models.CASCADE)
    numero_escala = models.IntegerField()

    class Meta:
        unique_together = ('itinerario', 'numero_escala')

    def __str__(self):
        return f"{self.itinerario} - Escala {self.numero_escala}"

class Viaje(models.Model):

    CATEGORIAS = [
        ('Especial', 'Especial'),
        ('Super Lujo', 'Super Lujo'),
        ('Lujoso', 'Lujoso'),
        ('Común', 'Común'),
    ]

    navio = models.ForeignKey(Navio, on_delete=models.CASCADE)
    itinerario = models.ForeignKey(Itinerario, on_delete=models.CASCADE)
    fecha = models.DateField()
    duracion = models.IntegerField()

    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIAS
    )

    def __str__(self):
        return f"{self.navio} - {self.fecha}"
class Pasajero(models.Model):
    tipo_documento = models.CharField(max_length=20)
    numero_documento = models.CharField(max_length=30)
    nombre = models.CharField(max_length=100)
    pais_procedencia = models.CharField(max_length=100)
    ciudad_procedencia = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    pasajero = models.OneToOneField(
        Pasajero,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.usuario.username



class Reserva(models.Model):

    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
    ]

    pasajero = models.ForeignKey(
        Pasajero,
        on_delete=models.CASCADE
    )

    viaje = models.ForeignKey(
        Viaje,
        on_delete=models.CASCADE
    )

    camarote = models.ForeignKey(
        Camarote,
        on_delete=models.CASCADE
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='PENDIENTE'
    )

    fecha_solicitud = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['viaje', 'camarote'],
                condition=Q(estado__in=['PENDIENTE', 'CONFIRMADA']),
                name='camarote_unico_por_viaje'
            )
        ]

    def __str__(self):
        return f"{self.pasajero} - {self.viaje}"


class Ticket(models.Model):

    reserva = models.OneToOneField(
        Reserva,
        on_delete=models.CASCADE
    )

    codigo = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    fecha_emision = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Ticket {self.codigo}"


class Notificacion(models.Model):

    pasajero = models.ForeignKey(
        Pasajero,
        on_delete=models.CASCADE
    )

    mensaje = models.TextField()

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    leida = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"Notificación para {self.pasajero}"
