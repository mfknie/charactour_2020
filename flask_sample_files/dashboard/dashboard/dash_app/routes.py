from flask import Blueprint
from flask import current_app as app

dash_bp = Blueprint(
    'dash_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@dash_bp.route('/', methods=['GET'])
def home():
    """Main dashboard page"""
    