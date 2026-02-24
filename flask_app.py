import os
import io
import zipfile
from datetime import datetime
from flask import Flask, render_template, request, send_file
from logic.convocatorias import ConvocatoriaLogic
from logic.menor import ReportGeneratorLogic  # Añade esta línea al inicio

# Importación de tus generadores de PAT
from logic.PATS.Pat03 import generar_documento_pat03
from logic.PATS.Pat04 import generar_documento_pat04
from logic.PATS.Pat05 import generar_documento_pat05
from logic.PATS.Pat06 import generar_documento_pat06

app = Flask(__name__)

# --- CONFIGURACIÓN Y DATOS MAESTRÍAS ---

info_maestrias = {
    "1": {
        "nombre": "Maestría en Educación con Mención en Lingüística y Literatura, Cohorte IV – Matriz Manta.",
        "responsable": "Mg.\nVargas Parraga Vanessa Monserrate"
    },
    "2": {
        "nombre": "Maestría en Educación con Mención en Innovaciones Pedagógicas, Cohorte IV – sede Matriz.",
        "responsable": "Mg.\nDelgado Mero Diana Maria"
    },
    "3": {
        "nombre": "Maestría en Pedagogía de los Idiomas Nacionales y Extranjeros Mención Inglés Matriz Manta, Cohorte III.",
        "responsable": "Mg.\nBazurto Alcivar Gabriel José"
    }
}

temas_map = {
    "1": [ # REVISIÓN SISTEMÁTICA
        "Socialización de los PAT (003- 006)", "Selección de revista a publicar",
        "Delimitación del tema del trabajo de titulación", "Formulación del problema",
        "Diseño del protocolo de revisión", "Búsqueda sistemática de literatura",
        "Análisis y categorización temática", "Redacción del marco teórico",
        "Elaboración de discusión académica"
    ],
    "2": [ # NO EXPERIMENTAL
        "Socialización de los procesos de titulación (PAT)", "Planteamiento del problema",
        "Justificación, objetivos y viabilidad", "Construcción del marco referencial",
        "Definición y operativización de variables", "Diseño metodológico",
        "Identificación de población y muestra", "Diseño y validación de instrumentos",
        "Planificación del análisis de resultados"
    ],
    "3": [ # CUASI-EXPERIMENTAL
        "Socialización de normativas y formatos PAT", "Planteamiento de hipótesis",
        "Revisión de antecedentes y bases teóricas", "Diseño del plan de intervención",
        "Selección de grupos (Experimental/Control)", "Diseño y pilotaje de instrumentos",
        "Implementación de la intervención", "Aplicación de Pre-test y Post-test",
        "Análisis comparativo de datos"
    ]
}

# --- RUTAS ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convocatoria_estudiante', methods=['POST'])
def convocatoria_estudiante():
    try:
        cursos_seleccionados = request.form.getlist('cursos')
        cursos_str = ", ".join(cursos_seleccionados)
        sigla_fija = "PINE"

        datos = {
            'num_convocatoria': request.form.get('num_convocatoria'),
            'periodo': request.form.get('periodo'),
            'siglas_convocante': sigla_fija,
            'ciudad': request.form.get('ciudad'),
            'fecha_larga': request.form.get('fecha_larga'),
            'asunto': request.form.get('asunto'),
            'curso': cursos_str,
            'descripcion_convocatoria': request.form.get('descripcion_convocatoria'),
            'fecha_reunion': request.form.get('fecha_reunion'),
            'hora_reunion': request.form.get('hora_reunion'),
            'lugar_reunion': request.form.get('lugar_reunion'),
            'convocante_titulo': request.form.get('convocante_titulo'),
            'convocante_nombre': request.form.get('convocante_nombre'),
            'convocante_cargo': request.form.get('convocante_cargo'),
            'iniciales_elaborador': request.form.get('iniciales_elaborador')
        }

        archivos = request.files.getlist('excel_files')
        logic = ConvocatoriaLogic()
        buffer = logic.generar_docx("estudiante", datos, excel_files=archivos)

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"Convocatoria_Estudiantes_{datos['num_convocatoria']}.docx",
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/convocatoria_docente', methods=['POST'])
def convocatoria_docente():
    try:
        sigla_fija = "PINE"
        num = request.form.get('num_convocatoria')
        
        datos = {
            'num_convocatoria': num,
            'periodo': request.form.get('periodo'),
            'siglas_convocante': sigla_fija,
            'ciudad': request.form.get('ciudad'),
            'fecha_larga': request.form.get('fecha_larga'),
            'asunto': request.form.get('asunto'),
            'descripcion_convocatoria': request.form.get('descripcion_convocatoria'),
            'fecha_reunion': request.form.get('fecha_reunion'),
            'hora_reunion': request.form.get('hora_reunion'),
            'lugar_reunion': request.form.get('lugar_reunion'),
            'convocante_titulo': request.form.get('convocante_titulo'),
            'convocante_nombre': request.form.get('convocante_nombre'),
            'convocante_cargo': request.form.get('convocante_cargo'),
            'iniciales_elaborador': request.form.get('iniciales_elaborador')
        }

        logic = ConvocatoriaLogic()
        buffer = logic.generar_docx("docente", datos)

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"Convocatoria_Docentes_{num}.docx",
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/generar_pat_zip', methods=['POST'])
def generar_pat_zip():
    try:
        m_op = request.form.get('maestria_opcion')
        metod_op = request.form.get('metodologia_opcion')
        
        # Procesamiento de fechas
        fecha_s = request.form.get('fecha_sesion')
        fecha_d = request.form.get('fecha_designacion')
        
        # Formateamos para que la lógica lo entienda
        fecha_final_obj = datetime.strptime(fecha_s, '%Y-%m-%d')
        fecha_desig_str = datetime.strptime(fecha_d, '%Y-%m-%d').strftime('%d/%m/%Y')

        datos = {
            "MAESTRIA": info_maestrias[m_op]["nombre"],
            "responsable": info_maestrias[m_op]["responsable"],
            "temas": temas_map[metod_op],
            "nombre": request.form.get('nombre_maestrante'),
            "articulo": request.form.get('titulo_articulo'),
            "oficio": request.form.get('num_oficio'),
            "fecha_final": fecha_final_obj,
            "fecha_designacion": fecha_desig_str,
            "hora": request.form.get('hora_inicio')
        }

        # Crear el ZIP en memoria
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Lista de funciones y sus nombres de archivo
            pats = [
                (generar_documento_pat03(datos), "PAT_003_Cronograma.docx"),
                (generar_documento_pat04(datos), "PAT_004_Oficio.docx"),
                (generar_documento_pat05(datos), "PAT_005_Asistencia.docx"),
                (generar_documento_pat06(datos), "PAT_006_Informe.docx"),
            ]
            
            for buffer, name in pats:
                if buffer:
                    zip_file.writestr(name, buffer.getvalue())

        zip_buffer.seek(0)
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f"PAT_{datos['nombre'].replace(' ', '_')}.zip"
        )
    except Exception as e:
        return f"Error en Maestría: {str(e)}", 500

@app.route('/generate_report', methods=['POST'])
def generate_report():
    try:
        parcial_id = request.form.get('parcial_seleccionado')
        excel_file = request.files.get('excel_file')
        
        if not excel_file:
            return "No se subió ningún archivo", 400

        # Mapeo completo de todos los campos del formulario
        datos = {
            "fecha": request.form.get('fecha'),
            "titulo_academico_destinatario": request.form.get('titulo_academico_destinatario'),
            "nombres_apellidos_destinatario": request.form.get('nombres_apellidos_destinatario'),
            "facultad_extension_destinatario": request.form.get('facultad_extension_destinatario'),
            "titulo_academico_emisor": request.form.get('titulo_academico_emisor'),
            "nombres_apellidos_emisor": request.form.get('nombres_apellidos_emisor'),
            "titulo_academico_cc": request.form.get('titulo_academico_cc'), # NUEVO
            "nombres_apellidos_cc": request.form.get('nombres_apellidos_cc'), # NUEVO
            "asignatura": "ASIGNATURA" 
        }

        logic = ReportGeneratorLogic()
        
        if excel_file.filename:
            datos["asignatura"] = logic._extract_subject_from_filename(excel_file.filename)

        estudiantes, info_parcial = logic.process_excel_data(excel_file, parcial_id)
        buffer = logic.generate_report(datos, estudiantes, info_parcial)

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"Informe_Notas_Menores_{parcial_id}.docx",
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        return f"Error en Informe: {str(e)}", 500

@app.route('/generar_acta', methods=['POST'])
def generar_acta():
    # Aquí irá la lógica similar a las demás para llenar el Word
    return "Funcionalidad de Acta en construcción", 200


# --- INICIO DEL SERVIDOR ---
if __name__ == '__main__':
    # El servidor debe arrancar DESPUÉS de definir todas las rutas
    app.run(debug=True, port=5000)