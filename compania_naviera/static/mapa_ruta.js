// Mapa de la ruta de un itinerario (template itinerario_detail.html)
// Usa la librería Leaflet: pone un marcador en cada parada y une las paradas con una línea.

document.addEventListener('DOMContentLoaded', function () {

    const contenedor = document.getElementById('mapa-ruta');

    if (!contenedor) {
        return;
    }

    // Lista de paradas que mandó la vista con json_script
    const paradas = JSON.parse(document.getElementById('paradas-data').textContent);

    // Crear el mapa y cargar el fondo de OpenStreetMap
    const mapa = L.map('mapa-ruta');

    // referrerPolicy: OpenStreetMap exige saber desde qué sitio se piden los mapas.
    // Django por defecto no lo envía, y sin esto OpenStreetMap bloquea las imágenes.
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; OpenStreetMap',
        referrerPolicy: 'strict-origin-when-cross-origin'
    }).addTo(mapa);

    const puntos = [];

    // Si el barco pasa dos veces por el mismo puerto (por ejemplo, sale y vuelve
    // a Buenos Aires) se usa un solo marcador con las dos escalas, así no se tapan.
    const puertos = {};

    paradas.forEach(function (parada) {

        puntos.push([parada.lat, parada.lng]);

        const clave = parada.lat + ',' + parada.lng;

        if (puertos[clave]) {
            puertos[clave].escalas.push(parada.escala);
        } else {
            puertos[clave] = { parada: parada, escalas: [parada.escala] };
        }

    });

    Object.values(puertos).forEach(function (puerto) {

        const parada = puerto.parada;
        const escalas = puerto.escalas.join(' y ');

        // Contenido del cartel que aparece al hacer clic en el marcador
        const popup = document.createElement('div');
        popup.className = 'popup-parada';

        if (parada.imagen) {
            const img = document.createElement('img');
            img.src = parada.imagen;
            img.alt = parada.ciudad;
            popup.appendChild(img);
        }

        const titulo = document.createElement('strong');
        titulo.textContent = (puerto.escalas.length > 1 ? 'Escalas ' : 'Escala ') + escalas + ': ' + parada.ciudad;
        popup.appendChild(titulo);

        const detalle = document.createElement('p');
        detalle.textContent = parada.nombre + ' · ' + parada.pais;
        popup.appendChild(detalle);

        L.marker([parada.lat, parada.lng])
            .addTo(mapa)
            .bindPopup(popup)
            .bindTooltip(escalas, { permanent: true, direction: 'top' });

    });

    // Línea que une las paradas en orden: la ruta del barco
    L.polyline(puntos, {
        color: '#173B55',
        weight: 3,
        dashArray: '8 8'
    }).addTo(mapa);

    // Acomodar el zoom para que se vean todas las paradas
    if (puntos.length === 1) {
        mapa.setView(puntos[0], 8);
    } else {
        mapa.fitBounds(puntos, { padding: [50, 50] });
    }

});
