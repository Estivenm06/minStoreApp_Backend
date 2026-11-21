from flask import Blueprint, jsonify, request
from src.models.detailed_invoice import DetailedInvoices

from src.utils.auth import token_required, required_user
from src.models.users import Role

detailed_invoices_bp = Blueprint('detailed_invoices_v1', __name__, url_prefix='/api/v1')

@detailed_invoices_bp.route('/detailed_invoices', methods=['GET'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def get_detailed_invoices():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)
    detailed_invoices, total_detailed_invoices = DetailedInvoices.get_paginted(page, per_page)    
    total_pages = (total_detailed_invoices + per_page - 1) // per_page # Calculate total pages

    return jsonify({
        'detailed_invoices' : 
        [{
        'id': detailed_invoice.id,
        'id_invoice': detailed_invoice.id_invoice,
        'id_product': detailed_invoice.id_product,
        'quantity': detailed_invoice.quantity,
        'unit_price': detailed_invoice.unit_price,
        'subtotal': detailed_invoice.subtotal
    } for detailed_invoice in detailed_invoices],
    'meta': {
        'page': page,
        'per_page': per_page,
        'total_detailed_invoices': total_detailed_invoices,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1
    }
    }), 200

@detailed_invoices_bp.route('/detailed_invoices/<int:detailed_invoice_id>', methods=['GET'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def get_detailed_invoice(detailed_invoice_id):
    detailed_invoice = DetailedInvoices.get_by_id(detailed_invoice_id)

    if not detailed_invoice:
        return jsonify({
            'success': False,
            'message': f'Detailed invoice with id {detailed_invoice_id} not found'
        }), 404
    
    return jsonify({
        'id': detailed_invoice.id,
        'id_invoice': detailed_invoice.id_invoice,
        'id_product': detailed_invoice.id_product,
        'quantity': detailed_invoice.quantity,
        'unit_price': detailed_invoice.unit_price,
        'subtotal': detailed_invoice.subtotal
    }), 200

@detailed_invoices_bp.route('/detailed_invoices/invoice/<int:invoice_id>', methods=['GET'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def get_detailed_invoices_by_invoice_id(invoice_id):
    detailed_invoices = DetailedInvoices.get_by_invoice_id(invoice_id)

    if not detailed_invoices:
        return jsonify({
            'success': False,
            'message': f'Detailed invoices for invoice id {invoice_id} not found'
        }), 404
    
    return jsonify([{
        'id': detailed_invoice.id,
        'id_invoice': detailed_invoice.id_invoice,
        'id_product': detailed_invoice.id_product,
        'quantity': detailed_invoice.quantity,
        'unit_price': detailed_invoice.unit_price,
        'subtotal': detailed_invoice.subtotal
    } for detailed_invoice in detailed_invoices]), 200

@detailed_invoices_bp.route('/detailed_invoices', methods=['POST'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def create_detailed_invoice():
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'error': 'No input data provided'}), 400

    required_fields = ['id_invoice', 'id_product', 'quantity', 'unit_price', 'subtotal']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400

    detailed_invoice = DetailedInvoices(
        id_invoice=data['id_invoice'],
        id_product=data['id_product'],
        quantity=data['quantity'],
        unit_price=data['unit_price'],
        subtotal=data['subtotal']
    )

    detailed_invoice.save()

    return jsonify({
        'success': True,
        'message': 'Detailed invoice created successfully',
        'detailed_invoice': {
            'id': detailed_invoice.id,
            'id_invoice': detailed_invoice.id_invoice,
            'id_product': detailed_invoice.id_product,
            'quantity': detailed_invoice.quantity,
            'unit_price': detailed_invoice.unit_price,
            'subtotal': detailed_invoice.subtotal
        }
    }), 201

@detailed_invoices_bp.route('/detailed_invoices/<int:detailed_invoice_id>', methods=['PUT'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def update_detailed_invoice(detailed_invoice_id):
    detailed_invoice = DetailedInvoices.get_by_id(detailed_invoice_id)

    if not detailed_invoice:
        return jsonify({
            'success': False,
            'message': f'Detailed invoice with id {detailed_invoice_id} not found'
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'error': 'No input data provided'}), 400

    for key in ['id_invoice', 'id_product', 'quantity', 'unit_price', 'subtotal']:
        if key in data:
            setattr(detailed_invoice, key, data[key])

    detailed_invoice.update()

    return jsonify({
        'success': True,
        'message': 'Detailed invoice updated successfully',
        'detailed_invoice': {
            'id': detailed_invoice.id,
            'id_invoice': detailed_invoice.id_invoice,
            'id_product': detailed_invoice.id_product,
            'quantity': detailed_invoice.quantity,
            'unit_price': detailed_invoice.unit_price,
            'subtotal': detailed_invoice.subtotal
        }
    }), 200