from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('TRIPULANTE', 'Tripulante'),
        ('PASAJERO', 'Pasajero'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='perfil'
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='PASAJERO')

    tripulante = models.OneToOneField(
        'Tripulante',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='perfil_usuario',
    )
    pasajero = models.OneToOneField(
        'Pasajero',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='perfil_usuario',
    )

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f'{self.user.username} - {self.get_rol_display()}'

class Navio(models.Model):
    codigo_navio = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    altura = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    eslora = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    manga = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    desplazamiento = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    autonomia_viaje = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    cantidad_camarotes = models.IntegerField(default=0)
    cantidad_maxima_pasajeros = models.IntegerField(default=0)
    cantidad_motores = models.IntegerField(default=0)
    cantidad_tripulantes = models.IntegerField(default=0)
    clasificacion = models.CharField(max_length=50, default='Estandar')

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Navío"
        verbose_name_plural = "Navíos"
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo_navio} - {self.nombre} - Capacidad: {self.cantidad_maxima_pasajeros}'


class Cubierta(models.Model):
    navio = models.ForeignKey(
        Navio,
        on_delete=models.CASCADE,
        related_name='cubiertas'
    )
    numero_cubierta = models.CharField(max_length=10)
    encargado = models.CharField(max_length=100)
    descripcion = models.TextField(
        null=True, 
        blank=True # Opcional
    )

    class Meta:
        verbose_name = "Cubierta"
        verbose_name_plural = "Cubiertas"
        ordering = ['navio', 'numero_cubierta']
        unique_together = ('navio', 'numero_cubierta')

    def __str__(self):
        return f'Cubierta {self.numero_cubierta} - {self.navio.nombre}'


class Camarote(models.Model):
    UBICACION_CHOICES = [
        ('BABOR', 'Babor'),
        ('CRUJIA', 'Crujía'),
        ('ESTRIBOR', 'Estribor'),
    ]
    cubierta = models.ForeignKey(
        Cubierta,
        on_delete=models.CASCADE,
        related_name='camarotes'
    )
    numero_camarote = models.IntegerField(default=0)
    tipo = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=20, choices=UBICACION_CHOICES, default='BABOR')

    class Meta:
        verbose_name = "Camarote"
        verbose_name_plural = "Camarotes"
        ordering = ['cubierta', 'numero_camarote']

    def __str__(self):
        return f'Camarote {self.numero_camarote} - {self.tipo} ({self.get_ubicacion_display()})'


class Tripulante(models.Model):
    navio = models.ForeignKey(
        Navio,
        on_delete=models.SET_NULL,
        related_name='tripulantes',
        null=True,
        blank=True # Puede no estar asignado a un navío temporalmente
    )
    jefe = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='subordinados',
        null=True,
        blank=True # Si no tiene jefe es la máxima autoridad
    )
    legajo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)

    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tripulante"
        verbose_name_plural = "Tripulantes"
        ordering = ['nombre']

    def __str__(self):
        return f'{self.legajo} - {self.nombre} - Puesto: {self.puesto}'


class Itinerario(models.Model):
    CATEGORIA_CHOICES = [
        ('ESPECIAL', 'Especial'),
        ('SUPER_LUJO', 'Super Lujo'),
        ('LUJOSO', 'Lujoso'),
        ('COMUN', 'Común'),
    ]
    codigo_itinerario = models.CharField(max_length=50, unique=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='COMUN')

    class Meta:
        verbose_name = "Itinerario"
        verbose_name_plural = "Itinerarios"
        ordering = ['codigo_itinerario']

    def __str__(self):
        return f'Itinerario {self.codigo_itinerario} - {self.get_categoria_display()}'


class Puerto(models.Model):
    codigo_puerto = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Puerto"
        verbose_name_plural = "Puertos"
        ordering = ['nombre']

    def __str__(self):
        return f'{self.codigo_puerto} - {self.nombre}'


class Escala(models.Model):
    itinerario = models.ForeignKey(
        Itinerario,
        on_delete=models.CASCADE,
        related_name='escalas'
    )
    puerto = models.ForeignKey(
        Puerto,
        on_delete=models.CASCADE,
        related_name='escalas'
    )
    numero_escala = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Escala"
        verbose_name_plural = "Escalas"
        ordering = ['itinerario', 'numero_escala']
        unique_together = ('itinerario', 'numero_escala')

    def __str__(self):
        return f'Escala {self.numero_escala} - {self.puerto.nombre}'


class Viaje(models.Model):
    navio = models.ForeignKey(
        Navio,
        on_delete=models.CASCADE,
        related_name='viajes'
    )
    itinerario = models.ForeignKey(
        Itinerario,
        on_delete=models.CASCADE,
        related_name='viajes'
    )
    codigo_viaje = models.CharField(max_length=50, unique=True)
    fecha_viaje = models.DateField()
    duracion = models.IntegerField(default=0) # Duración en días

    class Meta:
        verbose_name = "Viaje"
        verbose_name_plural = "Viajes"
        ordering = ['-fecha_viaje']

    def __str__(self):
        return f'Viaje {self.codigo_viaje} - {self.navio.nombre} - Fecha: {self.fecha_viaje}'


class Pasajero(models.Model):
    tipo_documento = models.CharField(max_length=20)
    numero_documento = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    pais_procedencia = models.CharField(max_length=100)
    ciudad_procedencia = models.CharField(max_length=100)
    
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pasajero"
        verbose_name_plural = "Pasajeros"
        ordering = ['nombre']
        unique_together = ('tipo_documento', 'numero_documento')

    def __str__(self):
        return f'{self.nombre} - {self.tipo_documento}: {self.numero_documento}'


class Reserva(models.Model):
    pasajero = models.ForeignKey(
        Pasajero,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    viaje = models.ForeignKey(
        Viaje,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    camarote = models.ForeignKey(
        Camarote,
        on_delete=models.CASCADE,
        related_name='reservas',
        null=True,
        blank=True # Puede que se asigne el camarote al momento de embarcar
    )
    codigo_reserva = models.CharField(max_length=50, unique=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'Reserva {self.codigo_reserva} - Pasajero: {self.pasajero.nombre} - Viaje: {self.viaje.codigo_viaje}'