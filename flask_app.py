import os
from flask import Flask, render_template, request, send_file
from logic.convocatorias import ConvocatoriaLogic

app = Flask(__name__)

# Configuración de carpetas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
            # --- CORRECCIÓN AQUÍ ---
            'curso': cursos_str,   # Añadimos 'curso' para que reemplace {{CURSO}}
            'cursos': cursos_str,  # Mantenemos 'cursos' por si acaso
            # -----------------------
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
        # Aquí 'excel_files' es el nombre del argumento en logic/convocatorias.py
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
        # 1. Definimos la sigla fija de la carrera
        sigla_fija = "PINE"
        
        # 2. Recogemos los datos del formulario
        num = request.form.get('num_convocatoria')
        periodo = request.form.get('periodo')
        ciudad = request.form.get('ciudad')
        fecha_l = request.form.get('fecha_larga')
        asunto = request.form.get('asunto')
        desc = request.form.get('descripcion_convocatoria')
        f_reu = request.form.get('fecha_reunion')
        h_reu = request.form.get('hora_reunion')
        l_reu = request.form.get('lugar_reunion')
        tit = request.form.get('convocante_titulo')
        nom = request.form.get('convocante_nombre')
        car = request.form.get('convocante_cargo')
        ini = request.form.get('iniciales_elaborador')

        # 3. Diccionario unificado (la lógica se encarga de las llaves {{}})
        # Nota: Ya no necesitamos pasar 'siglas_convocante' desde el form, usamos sigla_fija
        datos = {
            'num_convocatoria': num, 'NUM_CONVOCATORIA': num,
            'periodo': periodo, 'PERIODO': periodo,
            'siglas_convocante': sigla_fija, 'SIGLAS_CONVOCANTE': sigla_fija,
            'ciudad': ciudad, 'CIUDAD': ciudad,
            'fecha_larga': fecha_l, 'FECHA_LARGA': fecha_l,
            'asunto': asunto, 'ASUNTO': asunto,
            'descripcion_convocatoria': desc, 'DESCRIPCION_CONVOCATORIA': desc,
            'fecha_reunion': f_reu, 'FECHA_REUNION': f_reu,
            'hora_reunion': h_reu, 'HORA_REUNION': h_reu,
            'lugar_reunion': l_reu, 'LUGAR_REUNION': l_reu,
            'convocante_titulo': tit, 'CONVOCANTE_TITULO': tit,
            'convocante_nombre': nom, 'CONVOCANTE_NOMBRE': nom,
            'convocante_cargo': car, 'CONVOCANTE_CARGO': car,
            'iniciales_elaborador': ini, 'INICIALES_ELABORADOR': ini
        }

        # 4. Llamada a la lógica
        logic = ConvocatoriaLogic()
        buffer = logic.generar_docx("docente", datos)

        # 5. Retorno del archivo corregido
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"Convocatoria_Docentes_{num}.docx",
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        return f"Error en el servidor: {str(e)}", 500

@app.route('/generate_report', methods=['POST'])
def generate_report():
    # Aquí iría la lógica que ya tienes para el informe de notas promedios menores
    # Por ahora, un placeholder para que no rompa el server
    return "Funcionalidad de Informe en desarrollo o integrada aquí.", 200

if __name__ == '__main__':
    print("Iniciando servidor Flask en http://127.0.0.1:5000")
    app.run(debug=True)