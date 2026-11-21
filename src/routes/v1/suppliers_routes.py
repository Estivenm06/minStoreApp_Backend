from flask import Blueprint, jsonify, request

from src.models.suppliers import Suppliers
from src.models.users import Role
from src.utils.auth import required_user, token_required

suppliers_bp = Blueprint('suppliers_v1', __name__, url_prefix='/api/v1')

@suppliers_bp.route('/suppliers', methods=['GET'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def get_suppliers():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)
    suppliers, total_suppliers = Suppliers.get_paginated(page, per_page)    
    total_pages = (total_suppliers + per_page - 1) // per_page # Calculate total pages

    if not suppliers:
        return jsonify({
            'success': False,
            'message': 'No suppliers found'
        }), 404

    return jsonify({
        'suppliers' : 
        [{
        'id': supplier.id,
        'name': supplier.name,
        'nit': supplier.nit,
        'contact_name': supplier.contact_name,
        'phone_number': supplier.phone_number,
        'email': supplier.email,
        'address': supplier.address,
        'active': supplier.active
    } for supplier in suppliers],
    'meta': {
        'page': page,
        'per_page': per_page,
        'total_suppliers': total_suppliers,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1
    }
    }), 200

@suppliers_bp.route('/suppliers/<int:supplier_id>', methods=['GET'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def get_supplier(supplier_id):
    supplier = Suppliers.get_by_id(supplier_id)

    if not supplier:
        return jsonify({
            'success': False,
            'message': f'Supplier with id {supplier_id} not found'
        }), 404
    
    return jsonify({
        'id': supplier.id,
        'name': supplier.name,
        'nit': supplier.nit,
        'contact_name': supplier.contact_name,
        'phone_number': supplier.phone_number,
        'email': supplier.email,
        'address': supplier.address,
        'active': supplier.active
    }), 200

@suppliers_bp.route('/suppliers/name/<string:name>', methods=['GET'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def get_supplier_by_name(name):
    supplier = Suppliers.get_by_name(name)

    if not supplier:
        return jsonify({
            'success': False,
            'message': f'Supplier with name {name} not found'
        }), 404
    
    return jsonify({
        'id': supplier.id,
        'name': supplier.name,
        'nit': supplier.nit,
        'contact_name': supplier.contact_name,
        'phone_number': supplier.phone_number,
        'email': supplier.email,
        'address': supplier.address,
        'active': supplier.active
    }), 200

@suppliers_bp.route('/suppliers', methods=['POST'])
@token_required
@required_user(Role.ADMIN)
def create_supplier():
    data = request.get_json()

    errors = []

    if not data:
        return jsonify({'success': False, 'message': 'No input data provided'}), 400
    
    [name, nit, contact_name, phone_number, email, address] = [data.get(field) for field in ['name', 'nit', 'contact_name', 'phone_number', 'email', 'address']]

    if not name:
        errors.append('Supplier name is required')

    existing_supplier = Suppliers.get_by_name(name)
    existing_supplier_nit = Suppliers.get_by_nit(nit) if nit else None
    if existing_supplier:
        errors.append(f'Supplier with name {name} already exists')
    if existing_supplier_nit:
        errors.append(f'Supplier with nit {nit} already exists')

    if errors:
        return jsonify({'success': False, 'message': 'Validation errors', 'errors': errors}), 400

    new_supplier = Suppliers(name=name, nit=nit, contact_name=contact_name, phone_number=phone_number, email=email, address=address)
    new_supplier.save()

    return jsonify({
        'success': True,
        'message': 'Supplier created successfully',
        'supplier': {
            'id': new_supplier.id,
            'name': new_supplier.name,
            'nit': new_supplier.nit,
            'contact_name': new_supplier.contact_name,
            'phone_number': new_supplier.phone_number,
            'email': new_supplier.email,
            'address': new_supplier.address,
            'active': new_supplier.active
        }
    }), 201

@suppliers_bp.route('/suppliers/<int:supplier_id>', methods=['PUT'])
@token_required
@required_user(Role.ADMIN)
def update_supplier(supplier_id):
    supplier = Suppliers.get_by_id(supplier_id)

    if not supplier:
        return jsonify({
            'success': False,
            'message': f'Supplier with id {supplier_id} not found'
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'message': 'No input data provided'}), 400

    [name, nit, contact_name, phone_number, email, address, active] = [data.get(field) for field in ['name', 'nit', 'contact_name', 'phone_number', 'email', 'address', 'active']]

    errors = []

    # Check for existing supplier with the same name or nit (if provided)
    existing_supplier = Suppliers.get_by_name(name) if name else None
    existing_supplier_nit = Suppliers.get_by_nit(nit) if nit else None
    if existing_supplier and existing_supplier.id != supplier_id:
        errors.append(f'Supplier with name {name} already exists')
    if existing_supplier_nit and existing_supplier_nit.id != supplier_id:
        errors.append(f'Supplier with nit {nit} already exists')

    if name == supplier.name and nit == supplier.nit:
        errors.append('No changes detected in the supplier data')

    if errors:
        return jsonify({'success': False, 'message': 'Validation errors', 'errors': errors}), 400


    supplier.update(name=name, nit=nit, contact_name=contact_name, phone_number=phone_number, email=email, address=address, active=active)

    return jsonify({
        'success': True,
        'message': 'Supplier updated successfully',
        'supplier': {
            'id': supplier.id,
            'name': supplier.name,
            'nit': supplier.nit,
            'contact_name': supplier.contact_name,
            'phone_number': supplier.phone_number,
            'email': supplier.email,
            'address': supplier.address,
            'active': supplier.active
        }
    }), 200