# Models
from src.models.categories import Categories
from src.models.suppliers import Suppliers
from src.models.products import Products
from src.models.users import Users

from flask import Flask

from src.models import Base, engine
from src.routes import register_routes

app = Flask(__name__)

register_routes(app)
app.config['JWT_SECRET_KEY'] = '$|s?W%Y^w32dPbldOF?-uNS${vQCrw&n'
 
Base.metadata.create_all(engine)

@app.route('/')
def health():
    return {
        'success': True,
        "health": "OK",
    }


if __name__ == '__main__':
    app.run(debug=True)