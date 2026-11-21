from flask import Blueprint, jsonify, request

from src.models.users import Role, Users
from src.utils.auth import required_user, token_required

users_bp = Blueprint('users_v1', __name__, url_prefix='/api/v1')

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
@required_user(Role.ADMIN)
def update_user_role(user_id):
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'error': 'Missing JSON data'}), 400

    user = Users.get_user_by_id(user_id)

    if not user:
        return jsonify({'success': False, 'error': f'User with id {user_id} not found'}), 404

    # Update user fields

    if 'role' in data and data['role'] not in [role.value for role in Role]:
        return jsonify({'success': False, 'error': f"Invalid role: {data['role']}"}), 400

    if 'role' in data and data['role'].upper() == user.role:
        return jsonify({'success': False, 'error': f"User already has role: {data['role']}"}), 400
    else:
        user.role = data['role'].upper() if 'role' in data else user.role
    user.update()

    return jsonify({
        'success': True,
        'message': f'User with id {user_id} updated role successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'role': user.role
        }
    }), 200