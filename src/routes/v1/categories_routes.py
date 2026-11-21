from flask import Blueprint, jsonify, request

from src.models.categories import Categories
from src.utils.auth import required_user, token_required

categories_bp = Blueprint('categories_v1', __name__, url_prefix='/api/v1')

@categories_bp.route('/categories', methods=['GET'])
@token_required
@required_user('admin', 'seller', 'user', 'client')
def get_categories():
    categories = Categories.get_all()
    print(categories)
    if len(categories) == 0:
        return jsonify({'message': 'No categories found'}), 404
    categories_list = [{'id': category.id, 'name': category.name, 'description': category.description} for category in categories]
    return jsonify({
        'success': True,
        'categories': categories_list
    }), 200

@categories_bp.route('/categories/<int:category_id>', methods=['GET'])
@token_required
@required_user('admin', 'seller', 'user', 'client')
def get_category_by_id(category_id):
    category = Categories.get_by_id(category_id)
    if not category:
        return jsonify({'message': 'Category not found'}), 404
    return jsonify({
        'success': True,
        'category': {'id': category.id, 'name': category.name, 'description': category.description}
    }), 200

@categories_bp.route('/categories', methods=['POST'])
@token_required
@required_user('admin')
def create_category():
    data = request.get_json()

    errors = []

    if not data:
        errors.append('No input data provided')
    
    name = data.get('name')
    description = data.get('description')

    if not name:
        errors.append('Category name is required')
    else:
        existing_category = Categories.get_by_name(name)
        if existing_category:
            errors.append('Category name already exists')

    if errors:
        return jsonify({
            'success': False,
            'errors': errors
        }), 400
    
    new_category = Categories(name=name, description=description)
    new_category.save()

    return jsonify({
        'success': True,
        'message': 'Category created successfully',
        'category': {'id': new_category.id, 'name': new_category.name, 'description': new_category.description}
    }), 201

@categories_bp.route('/categories/<int:category_id>', methods=['PUT'])
@token_required
@required_user('admin')
def update_category(category_id):
    category = Categories.get_by_id(category_id)
    if not category:
        return jsonify({'message': 'Category not found'}), 404

    data = request.get_json()

    errors = []

    if not data:
        errors.append('No input data provided')
    
    name = data.get('name')
    description = data.get('description')

    if not name:
        errors.append('Category name is required')
    else:
        existing_category = Categories.get_by_name(name)
        if existing_category:
            if existing_category.id != category_id:
                errors.append('Category name already exists')
            else:
                errors.append('This category already has the same name')

    if errors:
        return jsonify({
            'success': False,
            'errors': errors
        }), 400

    category.name = name
    category.description = description
    category.update()

    return jsonify({
        'success': True,
        'message': 'Category updated successfully',
        'category': {'id': category.id, 'name': category.name, 'description': category.description}
    }), 200