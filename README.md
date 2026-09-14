#  Compañía Naviera SEA STAR

Proyecto desarrollado para resolver el caso práctico de la **Compañía Naviera SEA STAR**, una empresa dedicada a la realización de cruceros.

El sistema permite administrar la información relacionada con los navíos, sus cubiertas, camarotes, tripulantes, itinerarios, puertos, viajes y pasajeros.

##  Descripción del proyecto

La compañía SEA STAR cuenta actualmente con tres navíos y tiene previsto incorporar nuevas embarcaciones a su flota.

El sistema busca organizar y relacionar toda la información necesaria para la gestión de los cruceros, permitiendo registrar:

- Navíos y sus características.
- Cubiertas de cada navío.
- Camarotes y su ubicación.
- Tripulación y puestos de trabajo.
- Relaciones entre tripulantes y sus jefes.
- Itinerarios y puertos.
- Escalas dentro de los itinerarios.
- Viajes realizados por los navíos.
- Pasajeros y sus reservas.
- Camarotes ocupados por los pasajeros.

##  Navíos

De cada navío se registran los siguientes datos:

- Código de navío.
- Nombre.
- Altura.
- Eslora.
- Manga.
- Desplazamiento.
- Autonomía de viaje.
- Cantidad de camarotes.
- Cantidad máxima de pasajeros.
- Cantidad de motores.
- Cantidad de tripulantes.
- Clasificación o nivel de lujo.

Cada navío está formado por varias **cubiertas**, las cuales poseen un número único dentro de cada barco y una descripción.

##  Cubiertas y camarotes

Cada cubierta pertenece a un navío y cuenta con un encargado.

Algunas cubiertas poseen camarotes destinados a los pasajeros.

De cada camarote se registra:

- Número de camarote.
- Tipo de camarote.
- Ubicación dentro de la cubierta:
  - Babor.
  - Crujía.
  - Estribor.

El número de camarote puede repetirse en diferentes cubiertas del mismo navío.

##  Tripulación

Cada navío cuenta con una tripulación que puede variar según el viaje.

De cada tripulante se registra:

- Legajo.
- Nombre.
- Puesto.
- Navío que tripula.
- Jefe.

Entre los puestos pueden encontrarse:

- Capitán.
- Primer Oficial.
- Segundo Oficial.
- Tercer Oficial.
- Maquinista.
- Camarero.
- Entre otros.

Un tripulante no puede formar parte de la tripulación de dos navíos al mismo tiempo.

##  Itinerarios y puertos

Los itinerarios están formados por diferentes puertos que son visitados durante el recorrido.

Cada puerto posee un número de **escala** dentro del itinerario.

Un mismo puerto puede formar parte de varios itinerarios y también puede ser visitado más de una vez dentro del mismo itinerario.

Los itinerarios tienen una categoría:

- Especial.
- Super Lujo.
- Lujoso.
- Común.

## Viajes

El sistema permite registrar los viajes realizados por los distintos navíos.

De cada viaje se registra:

- Navío que realiza el viaje.
- Itinerario realizado.
- Fecha del viaje.
- Duración.

La duración se registra para cada viaje debido a que un mismo itinerario puede tener diferentes duraciones dependiendo del viaje y del navío que lo realice.

##  Pasajeros

El sistema también permite registrar los pasajeros que hayan viajado o realizado reservas.

De cada pasajero se registra:

- Tipo de documento.
- Número de documento.
- Nombre.
- País de procedencia.
- Ciudad de procedencia.
- Crucero realizado.
- Camarote en el que se alojó.

##  Tecnologías utilizadas

- Python 3.12.3
- Django 5.2
- MySQL
- HTML
- CSS
- GitHub

  ##  Instalacion
Para ejecutar el proyecto localmente:
1. Clonar el repositorio
git clone git@github.com:Villada-PG3/trabajo-practico-integrador-compania_naviera_sea-star.git
2. Entrar en la carpeta
cd trabajo-practico-integrador-compania_naviera_sea-star
3. Crear el entorno virtual
python3 -m venv venv
4. Activar el entorno virtual

En Linux/WSL:

source venv/bin/activate


5. Instalar las dependencias
pip install -r requirements.txt
6. Realizar las migraciones
python manage.py makemigrations

python manage.py migrate
7. Ejecutar el servidor
python manage.py runserver

Luego se puede acceder al proyecto desde:

http://127.0.0.1:8000/

##  Estructura del proyecto

La estructura principal del proyecto se organiza de la siguiente manera:

```text
compania_naviera_sea_star/
│
├── manage.py
├── requirements.txt
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── naviera/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── ...
│
├── templates/
│   ├── base.html
│   └── naviera/
│       └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
├── media/
│   └── img/
│
└── docs/
    └── diagramas/
