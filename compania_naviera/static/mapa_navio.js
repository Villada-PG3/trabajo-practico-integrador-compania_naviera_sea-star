// Plano interactivo del navío (template mapa_navio.html)
// Al hacer clic en un camarote o una instalación se muestra su foto y sus datos.

document.addEventListener('DOMContentLoaded', function () {

    const panel = document.getElementById('panel-info');

    if (!panel) {
        return;
    }

    const ayuda = document.getElementById('ayuda-seleccion');
    const detalle = document.getElementById('detalle');
    const titulo = document.getElementById('detalle-titulo');
    const descripcion = document.getElementById('detalle-descripcion');
    const contenedorImagen = document.getElementById('contenedor-imagen');
    const imagen = document.getElementById('detalle-imagen');
    const boton = document.getElementById('boton-reservar');

    document.querySelectorAll('.elemento-mapa').forEach(function (elemento) {

        elemento.addEventListener('click', function () {

            // Marcar como seleccionado solo el elemento clickeado
            document.querySelectorAll('.elemento-mapa').forEach(function (otro) {
                otro.classList.remove('seleccionado');
            });
            elemento.classList.add('seleccionado');

            // Completar el panel con los datos guardados en data-*
            titulo.textContent = elemento.dataset.titulo;
            descripcion.textContent = elemento.dataset.descripcion;

            if (elemento.dataset.imagen) {
                imagen.src = elemento.dataset.imagen;
                imagen.alt = elemento.dataset.titulo;
                contenedorImagen.hidden = false;
            } else {
                contenedorImagen.hidden = true;
            }

            ayuda.hidden = true;
            detalle.hidden = false;

            // En la página de reserva: solo se puede reservar un camarote libre
            if (boton) {
                const radio = elemento.querySelector('input[type="radio"]');
                boton.disabled = !(radio && !radio.disabled);
            }

        });

    });

});
