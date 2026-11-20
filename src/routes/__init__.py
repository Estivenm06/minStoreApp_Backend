from src.routes.v1.auth_routes import auth_bp
from src.routes.v1.products_routes import products_bp


def register_routes(app):
    app.register_blueprint(products_bp)
    app.register_blueprint(auth_bp)
