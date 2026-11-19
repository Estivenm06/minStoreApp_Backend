from flask import jsonify
from src.models.products import Products

def validator_data(required_fields, data, update):
    if not data:
        return jsonify({
            'success': False,
            'message': 'No input data provided',
            'validation_error': 'Request body is empty or not in JSON format'
        }), 400

    return fields_validator(required_fields, data, update)

def fields_validator(required_fields, data, update):
    errors = []
    for key in required_fields:
        if key not in data:
            errors.append({key: f'{key} is required'})
        else:
            existing_product = Products.get_by_name(data['name']) if key == 'name' else None
            if update and existing_product:
                errors.append({key: f"{data[key]} must be unique"})
            if not update and existing_product:
                 errors.append({key: f"{data[key]} already exists"})
            

    for key in ['price_sell', 'price_buy', 'id_category', 'id_supplier']:
        if key in data:
                    try:
                        data[key] = int(data[key])
                        if data[key] < 0:
                            errors.append({key: f'{key} must be a non-negative integer'})
                    except ValueError:
                        errors.append({key: f'{key} must be an integer'})

    if errors:
        return jsonify({
            'success': False,
            'message': 'Missing required fields',
            'validation_error': f'Missing fields: {errors}'
        }), 400
