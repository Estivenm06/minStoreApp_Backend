from src.routes.v1.products_routes import products_bp

def register_routes(app):
    return app.register_blueprint(products_bp)
