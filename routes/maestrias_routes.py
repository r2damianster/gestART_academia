import io
import zipfile
from datetime import datetime
from flask import Blueprint, request, send_file
from logic.PATS.Pat03 import generar_documento_pat03
from logic.PATS.Pat04 import generar_documento_pat04
from logic.PATS.Pat05 import generar_documento_pat05
from logic.PATS.Pat06 import generar_documento_pat06

maestrias_bp = Blueprint('maestrias', __name__)

info_maestrias = {
    "1": {"nombre": "Maestría en Educación con Mención en Lingüística y Literatura...", "responsable": "Mg. Vargas Parraga Vanessa"},
    "2": {"nombre": "Maestría en Educación con Mención en Innovaciones Pedagógicas...", "responsable": "Mg. Delgado Mero Diana"},
    "3": {"nombre": "Maestría en Pedagogía de los Idiomas Nacionales...", "responsable": "Mg. Bazurto Alcivar Gabriel"}
}

temas_map = {
    "1": ["Socialización PAT", "Selección de revista", "Delimitación", "Problema", "Protocolo", "Búsqueda", "Categorización", "Marco teórico", "Discusión"],
    "2": ["Socialización PAT", "Problema", "Justificación", "Marco referencial", "Variables", "Diseño", "Población", "Validación", "Análisis"],
    "3": ["Socialización PAT", "Hipótesis", "Antecedentes", "Intervención", "Grupos", "Pilotaje", "Implementación", "Pre/Post-test", "Análisis"]
}

@maestrias_bp.route('/generar_pat_zip', methods=['POST'])
def generar_pat_zip():
    try:
        m_op = request.form.get('maestria_opcion')
        metod_op = request.form.get('metodologia_opcion')
        
        datos = {
            "MAESTRIA": info_maestrias[m_op]["nombre"],
            "responsable": info_maestrias[m_op]["responsable"],
            "temas": temas_map[metod_op],
            "nombre": request.form.get('nombre_maestrante'),
            "articulo": request.form.get('titulo_articulo'),
            "oficio": request.form.get('num_oficio'),
            "fecha_final": datetime.strptime(request.form.get('fecha_sesion'), '%Y-%m-%d'),
            "fecha_designacion": datetime.strptime(request.form.get('fecha_designacion'), '%Y-%m-%d').strftime('%d/%m/%Y'),
            "hora": request.form.get('hora_inicio')
        }

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            pats = [
                (generar_documento_pat03(datos), "PAT_003_Cronograma.docx"),
                (generar_documento_pat04(datos), "PAT_004_Oficio.docx"),
                (generar_documento_pat05(datos), "PAT_005_Asistencia.docx"),
                (generar_documento_pat06(datos), "PAT_006_Informe.docx"),
            ]
            for buff, name in pats:
                if buff: zip_file.writestr(name, buff.getvalue())

        zip_buffer.seek(0)
        return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name="PATS_Maestria.zip")
    except Exception as e:
        return f"Error: {str(e)}", 500