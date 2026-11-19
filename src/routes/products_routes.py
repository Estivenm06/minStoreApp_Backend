from flask import Blueprint, jsonify, request
from src.models.products import Products
from src.utils.helper import validator_data

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

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Products.get_by_id(product_id)

    if not product:
        return jsonify({
            'success': False,
            'message': f'Product with id {product_id} not found'
        }), 404
    
    return jsonify({
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
    }), 200

@products_bp.route('/products', methods=['POST'])
def create_product():

    data = request.get_json()
    
    validation_error = validator_data(['name', 'barcode', 'price_sell', 'price_buy', 'id_category', 'id_supplier'], data)
    if validation_error:
        return validation_error
        
    new_product = Products(
        name=data['name'],
        barcode=data['barcode'],
        description=data.get('description'),
        price_sell=data['price_sell'],
        price_buy=data['price_buy'],
        stock=data['stock'] if 'stock' in data else 0,
        id_category=data['id_category'],
        id_supplier=data['id_supplier']
    )

    new_product.create_product()

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

@products_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Products.get_by_id(product_id)

    if not product:
        return jsonify({
            'success': False,
            'message': f'Product with id {product_id} not found'
        }), 404

    data = request.get_json()
    validation_error = validator_data(['name', 'barcode', 'price_sell', 'price_buy', 'id_category', 'id_supplier'], data, update=False)

    if validation_error:
        return validation_error

    for key in ['name', 'barcode', 'description', 'price_sell', 'price_buy', 'stock', 'id_category', 'id_supplier']:
        if key in data:
            print(f"Updating {key} to {data[key]}")
            setattr(product, key, data[key])
    #product.update_product()

    return jsonify({
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
    }), 200