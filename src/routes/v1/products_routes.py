from flask import Blueprint, jsonify, request

from src.models.products import Products
from src.models.users import Role
from src.utils.auth import required_user, token_required
from src.utils.helper import validator_data

products_bp = Blueprint('products_v1', __name__, url_prefix='/api/v1')

@products_bp.route('/products', methods=['GET'])
@token_required
@required_user(Role.ADMIN, Role.SELLER, Role.USER)
def get_products():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)
    products, total_products = Products.get_paginated(page, per_page)    
    total_pages = (total_products + per_page - 1) // per_page # Calculate total pages

    return jsonify({
        'products' : 
        [{
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
    } for product in products],
    'meta': {
        'page': page,
        'per_page': per_page,
        'total_products': total_products,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1
    }
    }), 200

@products_bp.route('/products/<int:product_id>', methods=['GET'])
@token_required
@required_user(Role.ADMIN, Role.SELLER, Role.USER)
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
@token_required
@required_user(Role.ADMIN)
def create_product():

    data = request.get_json()
    
    validation_error = validator_data(['name', 'barcode', 'price_sell', 'price_buy', 'id_category', 'id_supplier'], data, update=False)
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
@token_required
@required_user(Role.ADMIN)
def update_product(product_id):
    product = Products.get_by_id(product_id)

    if not product:
        return jsonify({
            'success': False,
            'message': f'Product with id {product_id} not found'
        }), 404

    data = request.get_json()
    validation_error = validator_data(['name', 'barcode', 'price_sell', 'price_buy', 'id_category', 'id_supplier'], data, update=True)

    if validation_error:
        return validation_error

    for key in ['name', 'barcode', 'description', 'price_sell', 'price_buy', 'stock', 'id_category', 'id_supplier']:
        if key in data:
            setattr(product, key, data[key])
    
    product.update_product()

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