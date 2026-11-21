from flask import Blueprint, jsonify, request

from src.models.clients import Clients
from src.models.clients import Role as ClientRole
from src.models.users import Role
from src.utils.auth import required_user, token_required

clients_bp = Blueprint('clients_v1', __name__, url_prefix='/api/v1')

@clients_bp.route('/clients', methods=['GET'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def get_clients_paginated():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)
    clients, total_clients_count = Clients.get_paginated(page, per_page)
    total_pages = (total_clients_count + per_page - 1) // per_page # Calculate total pages
    if not clients:
        return jsonify({
            'success': False,
            'message': 'No clients found'
        }), 404

    clients_list = [{
        'id': client.id,
        'document': client.document,
        'name': client.name,
        'last_name': client.last_name,
        'phone_number': client.phone_number,
        'email': client.email,
        'address': client.address,
        'date_created': client.date_created.isoformat(),
        'active': client.active,
        'role': client.role
    } for client in clients]
    return jsonify({
        'success': True,
        'clients': clients_list,
        'meta': {
            'page': page,
            'per_page': per_page,
            'total_clients': total_clients_count,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }), 200


@clients_bp.route('/clients/<int:client_id>', methods=['GET'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def get_client_by_id(client_id):
    client = Clients.get_by_id(client_id)
    if not client:
        return jsonify({'message': 'Client not found'}), 404
    return jsonify({
        'success': True,
        'client': {'id': client.id, 'name': client.name, 'email': client.email, 'phone': client.phone_number, 'role': client.role}
    }), 200

@clients_bp.route('/clients', methods=['POST'])
@token_required
@required_user(Role.ADMIN, Role.SELLER)
def create_client():
    data = request.get_json()

    errors = []

    if not data:
        errors.append('No input data provided')

    [document, name, last_name, phone_number, email, address] = [data.get(field) for field in ['document', 'name', 'last_name', 'phone_number', 'email', 'address']]

    for field in ['name', 'last_name', 'document']:
        if not data.get(field):
            errors.append(f'Client {field} is required')

    existing_client = Clients.get_by_document(document)
    print(existing_client)
    if existing_client:
        errors.append('Client document already exists')
    
    if errors:
        return jsonify({
            'success': False,
            'errors': errors
        }), 400

    new_client = Clients(document=document, name=name, last_name=last_name, phone_number=phone_number, email=email, address=address)
    new_client.save()

    return jsonify({
        'success': True,
        'message': 'Client created successfully',
        'client': {'id': new_client.id, 'name': new_client.name, 'email': new_client.email, 'phone': new_client.phone_number, 'role': ClientRole.CLIENT.value}
    }), 201

@clients_bp.route('/clients/<int:client_id>', methods=['PUT'])
@token_required
@required_user(Role.ADMIN)
def update_client(client_id):
    client = Clients.get_by_id(client_id)

    if not client:
        return jsonify({'message': 'Client not found'}), 404

    data = request.get_json()

    errors = []

    if not data:
        errors.append('No input data provided')

    allowed_fields = ['document', 'name', 'last_name', 'phone_number', 'email', 'address', 'active']

    changed = False

    for field in allowed_fields:
        if field not in data:
            continue

        new_value = data.get(field)
        current_value = getattr(client, field)

        if new_value != current_value:
            changed = True

            if field == 'document' and new_value:
                existing_client = Clients.get_by_document(new_value)
                if existing_client and existing_client.id != client.id:
                    errors.append('Client document already exists')

            setattr(client, field, new_value)

    if not changed:
        errors.append('No changes detected')

    if errors:
        return jsonify({
            'success': False,
            'errors': errors
        }), 400

    client.update()

    return jsonify({
        'success': True,
        'message': 'Client updated successfully',
        'client': {'id': client.id, 'name': client.name, 'email': client.email, 'phone': client.phone_number, 'active': client.active}
    }), 200