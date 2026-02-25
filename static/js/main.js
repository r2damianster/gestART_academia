/**
 * main.js - Lógica de ARTeacher
 */

// 1. Control de navegación inteligente
// Oculta automáticamente cualquier elemento con la clase 'content-section' 
// y muestra solo el ID solicitado.
function mostrarSeccion(idSeccionAMostrar) {
    // Buscamos todos los contenedores de formularios
    const todasLasSecciones = document.querySelectorAll('.content-section');
    
    // Ocultamos todos de golpe
    todasLasSecciones.forEach(seccion => {
        seccion.classList.add('hidden');
    });

    // Mostramos el que corresponde
    const seccionActiva = document.getElementById(idSeccionAMostrar);
    if (seccionActiva) {
        seccionActiva.classList.remove('hidden');
    } else {
        console.error("Error: No existe la sección con ID:", idSeccionAMostrar);
    }
}

// 2. Control de submenús laterales
function toggleSubmenu() {
    const submenu = document.getElementById('submenu-socializacion');
    if (submenu) submenu.classList.toggle('hidden');
}

function toggleSubmenuMaestria() {
    const submenu = document.getElementById('submenu-maestria');
    if (submenu) submenu.classList.toggle('hidden');
}

// 3. Conversión de fecha a formato largo (ej: 24 de febrero de 2026)
function convertirFechaLarga(input, hiddenId) {
    if (!input.value) return;
    const partes = input.value.split('-');
    // Nota: El mes en Date() es index 0 (enero = 0)
    const fecha = new Date(partes[0], partes[1] - 1, partes[2]);
    const opciones = { day: 'numeric', month: 'long', year: 'numeric' };
    
    const hiddenInput = document.getElementById(hiddenId);
    if (hiddenInput) {
        hiddenInput.value = fecha.toLocaleDateString('es-ES', opciones);
    }
}

// 4. Lógica para selección de múltiples cursos y archivos
document.addEventListener('DOMContentLoaded', function() {
    const selectCursos = document.getElementById('cursos-multiple');
    if (selectCursos) {
        selectCursos.addEventListener('change', function() {
            const aviso = document.getElementById('aviso-cursos');
            const seleccionados = Array.from(this.selectedOptions).length;
            if (aviso) {
                aviso.style.display = (seleccionados > 1) ? 'block' : 'none';
            }
            actualizarListaArchivos();
        });
    }
});

// 5. Visualización previa de archivos seleccionados
function actualizarListaArchivos() {
    const input = document.getElementById('excel_files');
    const display = document.getElementById('lista-archivos-seleccionados');
    const selectCursos = document.getElementById('cursos-multiple');
    const numCursos = selectCursos ? Array.from(selectCursos.selectedOptions).length : 0;

    if (input && input.files.length > 0) {
        let html = `<strong>Archivos a procesar: ${input.files.length}</strong>`;
        
        // Alerta si faltan archivos para la cantidad de cursos elegidos
        if (numCursos > 0 && input.files.length < numCursos) {
            html += ` <br><span style="color:#f0ad4e; font-size: 0.85em;">⚠️ Nota: Has elegido ${numCursos} cursos, pero solo subiste ${input.files.length} archivo(s).</span>`;
        }
        
        html += "<ul style='margin-top: 10px; list-style: none; padding-left: 0;'>";
        for (let i = 0; i < input.files.length; i++) {
            html += "<li>✅ " + input.files[i].name + "</li>";
        }
        html += "</ul>";
        
        if (display) display.innerHTML = html;
    } else if (display) {
        display.innerHTML = "<em>Ningún archivo seleccionado.</em>";
    }
}