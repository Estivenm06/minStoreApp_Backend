from datetime import UTC, datetime, timedelta
from functools import wraps

import jwt
from flask import current_app, g, jsonify, request

from src.models.users import Role, Users


def generate_token(user, expires_in_hours=2):
    payload = {
        'user_id': user.id,
        'exp': datetime.now(tz=UTC) + timedelta(hours=expires_in_hours), # Token expires in expires_in_hours hours or 2 hours by default
        'role': user.role,
        'name': user.name,
        "iat": datetime.now(tz=UTC) # Issued at time
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            auth_header = auth_header.strip()  # Remove leading/trailing whitespace
            if auth_header.lower().startswith('bearer'):
                token = auth_header.split(' ')[1]
        if not token:
            return jsonify({'success': False, 'error': 'Token is missing!'}), 401

        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = Users.get_user_by_id(payload['user_id'])

            if not current_user:
                return jsonify({'success': False, 'error': 'User not found!'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'error': 'Invalid token!'}), 401

        g.current_user = current_user
        return f(*args, **kwargs)
    return decorated

def required_user(*roles):

    allowed_roles = [role.value if isinstance(role, Role) else role for role in roles]

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            current_user = getattr(g, 'current_user', None)
            if current_user is None:
                return jsonify({'success': False, 'error': 'You do not have the required permissions.'}), 401
            if current_user.role.lower() not in allowed_roles:
                return jsonify({'success': False, 'error': 'You do not have enough permissions to access this resource.'}), 403

            return f(*args, **kwargs)
        return decorated
    return decorator