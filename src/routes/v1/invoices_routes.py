from datetime import UTC, datetime

from flask import Blueprint, jsonify, request

from src.models.clients import Clients
from src.models.invoices import Invoices, PaymentMethods, Status
from src.models.users import Role, Users
from src.utils.auth import required_user, token_required

invoices_bp = Blueprint('invoices_v1', __name__, url_prefix='/api/v1')

@invoices_bp.route('/invoices', methods=['GET'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def get_invoices():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)
    invoices, total_invoices = Invoices.get_paginated(page, per_page)
    total_pages = (total_invoices + per_page - 1) // per_page

    if not invoices:
        return jsonify({
            'success': False,
            'message': 'No invoices found'
        }), 404

    return jsonify({
        'invoices': [{
            'id': invoice.id,
            'id_user': invoice.id_user,
            'date': invoice.date_issued,
            'total': invoice.total
        } for invoice in invoices],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total_invoices': total_invoices,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }), 200

@invoices_bp.route('/invoices/<int:invoice_id>', methods=['GET'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def get_invoice(invoice_id):
    invoice = Invoices.get_by_id(invoice_id)

    if not invoice:
        return jsonify({
            'success': False,
            'message': f'Invoice with id {invoice_id} not found'
        }), 404

    return jsonify({
        'id': invoice.id,
        'id_user': invoice.id_user,
        'date': invoice.date_issued,
        'total': invoice.total
    }), 200

@invoices_bp.route('/invoices/user/<int:user_id>', methods=['GET'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def get_invoices_by_user(user_id):

    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)
    invoices, total_invoices = Invoices.get_paginated_by_user(user_id, page, per_page)
    total_pages = (total_invoices + per_page - 1) // per_page

    if not invoices:
        return jsonify({
            'success': False,
            'message': 'No invoices created by this user'
        }), 404

    return jsonify({
        'invoices': [{
            'id': invoice.id,
            'id_user': invoice.id_user,
            'date': invoice.date_issued,
            'total': invoice.total
        } for invoice in invoices],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total_invoices': total_invoices,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }), 200

@invoices_bp.route('/invoices/<int:client_id>', methods=['POST'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def create_invoice(client_id):
    data = request.get_json()

    if not data:
        return jsonify({
            'success': False,
            'message': 'Request body must be JSON'
        }), 400

    [id_user, total, payment_method, tax, subtotal, invoice_number] = [data.get(field) for field in ['id_user', 'total', 'payment_method', 'tax', 'subtotal', 'invoice_number']]
    date_issued = datetime.now(UTC).date()

    invoice_already_exists = Invoices.get_by_invoice_number(invoice_number)
    if invoice_already_exists:
        return jsonify({
            'success': False,
            'message': f'Invoice with number {invoice_number} already exists'
        }), 400
    
    client = Clients.get_by_id(client_id)
    if not client:
        return jsonify({
            'success': False,
            'message': f'Client with id {client_id} not found'
        }), 404

    for field in ['id_user', 'total', 'payment_method', 'tax', 'subtotal', 'total', 'invoice_number', ]:
        if field not in data:
            return jsonify({
                'success': False,
                'message': f'Missing required field: {field}'
            }), 400
        if field == 'payment_method' and data[field] not in [PaymentMethods.CASH, PaymentMethods.CREDIT_CARD, PaymentMethods.DEBIT_CARD, PaymentMethods.PAYPAL, PaymentMethods.BANK_TRANSFER]:
            return jsonify({
                'success': False,
                'message': f'Invalid payment method: {data[field]}'
            }), 400


    invoice = Invoices(id_user=id_user, payment_method=payment_method, tax=tax, subtotal=subtotal, total=total, invoice_number=invoice_number, id_client=client_id, date_issued=date_issued)
    invoice.save()

    return jsonify({
        'success': True,
        'message': 'Invoice created successfully',
        'invoice': {
            'id': invoice.id,
            'id_client': invoice.id_client,
            'id_user': invoice.id_user,
            'date': invoice.date_issued,
            'total': invoice.total,
            'status': invoice.status,
            'payment_method': invoice.payment_method,
            'invoice_number': invoice.invoice_number,
            'date_issued': invoice.date_issued,
            'subtotal': invoice.subtotal,
            'tax': invoice.tax,
        }
    }), 201

@invoices_bp.route('/invoices/<int:invoice_id>', methods=['PUT'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def update_invoice(invoice_id):
    invoice = Invoices.get_by_id(invoice_id)
    if not invoice:
        return jsonify({
            'success': False,
            'message': f'Invoice with id {invoice_id} not found'
        }), 404

    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': 'Request body must be JSON'
        }), 400

    [id_user, id_client, invoice_number, status] = [data.get(field) for field in ['id_user', 'id_client', 'invoice_number', 'status']]

    if not status and not id_user and not id_client and not invoice_number:
        return jsonify({
            'success': False,
            'message': 'No valid fields provided for update'
        }), 400

    if invoice.id_client != id_client and id_client is not None:
        return jsonify({
            'success': False,
            'message': 'You cannot change the client of an invoice'
        }), 400

    if invoice.id_user != id_user and id_user is not None:
        return jsonify({
            'success': False,
            'message': 'You cannot change the user of an invoice'
        }), 400

    if invoice.status != status and status is not None and status not in [Status.PENDING, Status.PAID, Status.CANCELLED]:
        return jsonify({
            'success': False,
            'message': f'Invalid status: {status}. Valid statuses are: {Status.PENDING}, {Status.PAID}, {Status.CANCELLED}'
        }), 400

    if invoice.status == Status.PAID and status == Status.CANCELLED:
        return jsonify({
            'success': False,
            'message': 'You cannot change the status of a paid invoice to cancelled'
        }), 400

    if invoice.status == Status.CANCELLED and status == Status.PAID:
        return jsonify({
            'success': False,
            'message': 'You cannot change the status of a cancelled invoice to paid'
        }), 400

    if invoice.status == status and status is not None:
        return jsonify({
            'success': False,
            'message': f'Invoice is already in status {status}'
        }), 400
    
    user = Users.get_user_by_id(id_user)
    client = Clients.get_by_id(id_client)
    existing_invoice = Invoices.get_by_invoice_number(invoice_number)

    if not user:
        return jsonify({
                'success': False,
                'message': f'User with id {id_user} not found'
            }), 404
    if not client:
            return jsonify({
                'success': False,
                'message': f'Client with id {id_client} not found'
            }), 404

    if existing_invoice and existing_invoice.id != invoice_id:
            return jsonify({
                'success': False,
                'message': f'Invoice with number {invoice_number} already exists, you cannot update to this number'
            }), 400


    invoice.status = data.get('status', invoice.status)

    invoice.update()

    return jsonify({
        'success': True,
        'message': 'Invoice status updated successfully',
        'invoice': {
            'id': invoice.id,
            'id_user': invoice.id_user,
            'id_client': invoice.id_client,
            'invoice_number': invoice.invoice_number,
            'date': invoice.date_issued,
            'total': invoice.total,
            'status': invoice.status
        }
    }), 200
