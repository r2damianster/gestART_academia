from flask import Blueprint

actas_bp = Blueprint('actas', __name__)

@actas_bp.route('/generar_acta_tecnica', methods=['POST'])
def generar_acta_tecnica():
    return "Esta sección se encuentra en construcción.", 200