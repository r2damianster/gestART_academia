import os
import sys
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

# Asegurar que el sistema reconozca la carpeta logic para las importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from PATS.Pat03 import generar_documento_pat03
    from PATS.Pat04 import generar_documento_pat04
    from PATS.Pat05 import generar_documento_pat05
    from PATS.Pat06 import generar_documento_pat06
except ImportError as e:
    print(f"❌ Error al importar módulos: {e}")
    sys.exit()

def obtener_datos_interactivos():
    datos_ventana = {}
    root = tk.Tk()
    root.title("Fechas y Horas - PAT")
    root.geometry("350x350")
    root.attributes("-topmost", True)

    tk.Label(root, text="Fecha Sesión 9:", font=('Arial', 10, 'bold')).pack(pady=5)
    cal_sesion = DateEntry(root, width=12, date_pattern='dd/mm/yyyy')
    cal_sesion.pack(pady=5)

    tk.Label(root, text="Fecha Designación Tutor:", font=('Arial', 10, 'bold')).pack(pady=5)
    cal_desig = DateEntry(root, width=12, date_pattern='dd/mm/yyyy')
    cal_desig.pack(pady=5)

    tk.Label(root, text="Hora de Inicio:", font=('Arial', 10, 'bold')).pack(pady=5)
    frame_h = tk.Frame(root)
    frame_h.pack(pady=5)
    h = ttk.Combobox(frame_h, values=[f"{i:02d}" for i in range(7, 21)], width=4, state="readonly")
    h.set("16")
    h.pack(side=tk.LEFT)
    m = ttk.Combobox(frame_h, values=["00", "15", "30", "45"], width=4, state="readonly")
    m.set("00")
    m.pack(side=tk.LEFT)

    def guardar():
        datos_ventana['f9'] = cal_sesion.get_date()
        datos_ventana['f_desig'] = cal_desig.get_date().strftime("%d/%m/%Y")
        datos_ventana['hora'] = f"{h.get()}:{m.get()}"
        root.destroy()

    tk.Button(root, text="Aceptar", command=guardar, bg="green", fg="white").pack(pady=20)
    root.mainloop()
    return datos_ventana

def main():
    print("--- SISTEMA DE AUTOMATIZACIÓN PAT ---")
    
    print("\nSeleccione el Programa:")
    print("1 - Lingüística y Literatura")
    print("2 - Innovaciones Pedagógicas")
    print("3 - Pedagogía de Idiomas (Inglés)")
    m_op = input("Opción: ")

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

    if m_op in info_maestrias:
        maestria = info_maestrias[m_op]["nombre"]
        responsable = info_maestrias[m_op]["responsable"]
    else:
        maestria = input("Nombre maestría manual: ")
        responsable = input("Responsable manual: ")

    print("\n1-Revisión | 2-No Exp | 3-Cuasi")
    op = input("Opción: ")
    
    # Definición de temas largos y profesionales
    temas_map = {
        "1": [ # REVISIÓN SISTEMÁTICA
            "Socialización de los PAT (003- 006)",
            "Selección de revista a publicar",
            "Delimitación del tema del trabajo de titulación",
            "Formulación del problema de investigación y preguntas",
            "Diseño del protocolo de revisión",
            "Búsqueda sistemática y organización de literatura científica",
            "Análisis y categorización temática de los estudios",
            "Redacción del marco teórico y estado del arte",
            "Elaboración de discusión académica y conclusiones derivadas de la revisión"
        ],
        "2": [ # NO EXPERIMENTAL
            "Socialización de los procesos de titulación (PAT)",
            "Delimitación y planteamiento del problema de investigación",
            "Justificación, objetivos y viabilidad del estudio",
            "Revisión de literatura y construcción del marco referencial",
            "Definición y operativización de variables de estudio",
            "Diseño metodológico y selección del enfoque de investigación",
            "Identificación de población, muestra y técnicas de muestreo",
            "Diseño y validación de instrumentos de recolección de datos",
            "Planificación del análisis estadístico o cualitativo de resultados"
        ],
        "3": [ # CUASI-EXPERIMENTAL
            "Socialización de normativas y formatos PAT",
            "Planteamiento de hipótesis y definición de variables",
            "Revisión de antecedentes investigativos y bases teóricas",
            "Diseño del plan de intervención pedagógica/didáctica",
            "Selección y asignación de grupos (Experimental y Control)",
            "Diseño y pilotaje de instrumentos de medición",
            "Implementación de la intervención y recolección de datos",
            "Aplicación de Pre-test y Post-test a los grupos",
            "Análisis comparativo de datos y validación de hipótesis"
        ]
    }

    nombre = input("\nNombre del Maestrante: ")
    articulo = input("Título del Artículo/Tesis: ")
    oficio = input("N° del Oficio recibido: ")

    info = obtener_datos_interactivos()
    if not info: return

    datos = {
        "MAESTRIA": maestria,
        "responsable": responsable,
        "temas": temas_map.get(op, temas_map["1"]),
        "nombre": nombre,
        "articulo": articulo,
        "oficio": oficio,
        "fecha_final": datetime.combine(info['f9'], datetime.min.time()),
        "fecha_designacion": info['f_desig'],
        "hora": info['hora']
    }
    
    print("\nGenerando documentos...")
    generar_documento_pat03(datos) # Genera el Cronograma (X fijas)
    generar_documento_pat04(datos) # Genera el Oficio
    generar_documento_pat05(datos) # Genera el Registro de Asistencia (Estático)
    generar_documento_pat06(datos) # Genera el Informe de Tutoría
    
    print("\n✅ Proceso completado exitosamente.")

if __name__ == "__main__":
    main()