from flask import Blueprint, jsonify, request

from src.models.users import Users
from src.utils.auth import generate_token

auth_bp = Blueprint('auth_v1', __name__, url_prefix='/api/v1')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'error': 'Missing JSON data'}), 400

    errors = []

    [username, password, name, role] = [data.get('username'), data.get('password'), data.get('name'), data.get('role')]

    for field in ['username', 'password', 'name', 'role']:
        if field not in data or not data[field]:
            errors.append(f"Missing field: {field}")

    if len(password) < 6:
        errors.append('password must be at least 6 characters long')

    if username and Users.get_user_by_username(username):
        errors.append('username already exists') 

    if errors:
        return jsonify({'success': False,'errors': errors}), 400
    new_user = Users(username, name, password, role)

    new_user.save()

    return jsonify({
        'success': True,
        'message': 'User registered successfully',
    })

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'error': 'Missing JSON data'}), 400

    errors = []

    [username, password] = [data.get('username')], [data.get('password')]
    
    for field in ['username', 'password']:
        if field not in data:
            errors.append(f"Missing field: {field}")

    if len(password[0]) < 6:
        errors.append('password must be at least 6 characters long')

    if errors:
        return jsonify({'success': False,'errors': errors}), 400

    user = Users.get_user_by_username(username[0])

    if user and user.login(password[0]):
        return jsonify({
            'token_type': 'Bearer',
            'expires_in': 2 * 60 * 60,  # Token expires in 2 hours
            'access_token': generate_token(user),
            'user': {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'role': user.role
            }
            }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'Invalid username or password'
            }), 401
