from src.routes.v1.auth_routes import auth_bp
from src.routes.v1.categories_routes import categories_bp
from src.routes.v1.clients_routes import clients_bp
from src.routes.v1.detailed_invoices_routes import detailed_invoices_bp
from src.routes.v1.invoices_routes import invoices_bp
from src.routes.v1.products_routes import products_bp
from src.routes.v1.suppliers_routes import suppliers_bp
from src.routes.v1.users_routes import users_bp


def register_routes(app):
    app.register_blueprint(products_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(detailed_invoices_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(suppliers_bp)