from flask import Flask

def init_app():
    """
    Core Flask application.
    """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    
    with app.app_context():
        # Import parts of our core Flask app
        # from . import routes
        from dashboard.dash_app import routes
        
        # Import Dash application
        # from .dash_app.dash_plotly import create_dashboard
        # app = create_dashboard(app)

        app.register_blueprint(dash_bp)

        # Constructing dash apps
        from dashboard.dash_app.dash_plotly.dash_app import create_dashboard
        app = create_dashboard(app)

        return app