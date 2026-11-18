from flask import Blueprint, jsonify, request
from src.models.products import Products

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():

    products = Products.get_all()    
    return jsonify([{
        'id': product.id,
        'barcode': product.barcode,
        'name': product.name,
        'description': product.description,
        'price_sell': product.price_sell,
        'price_buy': product.price_buy,
        'stock': product.stock,
        'id_category': product.id_category,
        'id_supplier': product.id_supplier,
        'active': product.active
    } for product in products])

@products_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    if not all(key in data for key in ['name', 'barcode', 'price_sell', 'price_buy', 'stock', 'id_category', 'id_supplier']):
        return jsonify({'error': 'Missing required fields'}), 400
    new_product = Products(
        name=data['name'],
        barcode=data['barcode'],
        description=data.get('description'),
        price_sell=data['price_sell'],
        price_buy=data['price_buy'],
        stock=data['stock'],
        id_category=data['id_category'],
        id_supplier=data['id_supplier']
    )

    Products.create_product(new_product)

    return jsonify({
        'id': new_product.id,
        'barcode': new_product.barcode,
        'name': new_product.name,
        'description': new_product.description,
        'price_sell': new_product.price_sell,
        'price_buy': new_product.price_buy,
        'stock': new_product.stock,
        'id_category': new_product.id_category,
        'id_supplier': new_product.id_supplier,
        'active': new_product.active
    }), 201