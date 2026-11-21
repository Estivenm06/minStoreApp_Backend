# Models
from src.models.detailed_invoice import DetailedInvoices
from src.models.categories import Categories
from src.models.suppliers import Suppliers
from src.models.invoices import Invoices
from src.models.products import Products
from src.models.clients import Clients
from src.models.users import Users

from flask import Flask

# Routes
from src.routes import register_routes
from src.models import Base, engine

app = Flask(__name__)

register_routes(app) # Register the routes with the Flask app
app.config['JWT_SECRET_KEY'] = '$|s?W%Y^w32dPbldOF?-uNS${vQCrw&n' # Set a secret key for JWT authentication
 
Base.metadata.create_all(engine) # Create tables in the database if they don't exist

@app.route('/') # Set a health check route for the application
def health():
    return {
        'success': True,
        "health": "OK",
    }

if __name__ == '__main__':
    app.run(debug=True)