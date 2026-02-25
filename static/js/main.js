/**
 * main.js - Lógica Global de ARTeacher
 */

// 1. Control de navegación dinámico entre secciones
// Esta función oculta automáticamente cualquier div con la clase 'content-section'
function mostrarSeccion(seccionId) {
    // Seleccionamos todas las secciones por su clase (evita errores de listas manuales)
    const secciones = document.querySelectorAll('.content-section');
    
    secciones.forEach(el => {
        el.classList.add('hidden');
    });

    // Mostramos la sección solicitada
    const seccionAMostrar = document.getElementById(seccionId);
    if (seccionAMostrar) {
        seccionAMostrar.classList.remove('hidden');
    } else {
        console.warn(`La sección con ID "${seccionId}" no existe en el DOM.`);
    }
}

// 2. Control de submenús laterales (Dropdowns)
function toggleSubmenu() {
    const submenu = document.getElementById('submenu-socializacion');
    if (submenu) submenu.classList.toggle('hidden');
}

function toggleSubmenuMaestria() {
    const submenu = document.getElementById('submenu-maestria');
    if (submenu) submenu.classList.toggle('hidden');
}

// 3. Conversión de fecha a formato largo (ej: 25 de febrero de 2026)
function convertirFechaLarga(input, hiddenId) {
    if (!input.value) return;
    
    const partes = input.value.split('-');
    // Creamos la fecha (mes es 0-indexado)
    const fecha = new Date(partes[0], partes[1] - 1, partes[2]);
    
    const opciones = { day: 'numeric', month: 'long', year: 'numeric' };
    const fechaTexto = fecha.toLocaleDateString('es-ES', opciones);
    
    const targetInput = document.getElementById(hiddenId);
    if (targetInput) {
        targetInput.value = fechaTexto;
    }
}

// 4. Inicialización y Listeners al cargar el DOM
document.addEventListener('DOMContentLoaded', function() {
    // Lógica para selección de múltiples cursos (Informe de Notas)
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

    // Inicializar cualquier otro componente dinámico aquí
});

// 5. Visualización previa de archivos Excel seleccionados
function actualizarListaArchivos() {
    const input = document.getElementById('excel_files');
    const display = document.getElementById('lista-archivos-seleccionados');
    const selectCursos = document.getElementById('cursos-multiple');
    
    const numCursos = selectCursos ? Array.from(selectCursos.selectedOptions).length : 0;

    if (input && input.files.length > 0) {
        let html = `<strong>Archivos a procesar: ${input.files.length}</strong>`;
        
        // Alerta visual si faltan archivos según los cursos elegidos
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