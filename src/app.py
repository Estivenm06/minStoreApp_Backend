from flask import Flask
from src.models import Base, engine
from src.models.products import Products
from src.models.categories import Categories
from src.models.suppliers import Suppliers

from src.routes import register_routes

app = Flask(__name__)

register_routes(app)
 
Base.metadata.create_all(engine)

@app.route('/')
def health():
    return {
        'success': True,
        "health": "OK",
    }


if __name__ == '__main__':
    app.run(debug=True)