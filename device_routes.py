from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from repositories.user_device_repository import UserDeviceRepository

device_bp = Blueprint('device', __name__)

@device_bp.route('/device', methods=['POST'])
@jwt_required()
def register_device():
    """
    Register a device token for push notifications
    ---
    tags:
      - Device
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - device_token
            - platform
          properties:
            device_token:
              type: string
              description: FCM device token from client app
            platform:
              type: string
              enum: [ios, android, web]
              description: Device platform
    responses:
      201:
        description: Device token registered successfully
      400:
        description: Bad request
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    device_token = data.get('device_token')
    platform = data.get('platform')
    
    if not device_token:
        return jsonify({'error': 'device_token is required'}), 400
    
    if not platform:
        return jsonify({'error': 'platform is required'}), 400
    
    if platform not in ['ios', 'android', 'web']:
        return jsonify({'error': 'platform must be one of: ios, android, web'}), 400
    
    user_id = get_jwt_identity()
    device = UserDeviceRepository.register_device(user_id, device_token, platform)
    
    return jsonify({
        'message': 'Device token registered',
        'data': device.to_dict()
    }), 201

@device_bp.route('/device', methods=['GET'])
@jwt_required()
def get_devices():
    """
    Get all device tokens for the authenticated user
    ---
    tags:
      - Device
    security:
      - Bearer: []
    responses:
      200:
        description: List of device tokens
      401:
        description: Unauthorized
    """
    user_id = get_jwt_identity()
    devices = UserDeviceRepository.get_user_devices(user_id)
    
    return jsonify({
        'data': [device.to_dict() for device in devices]
    }), 200

@device_bp.route('/device/<int:device_id>', methods=['DELETE'])
@jwt_required()
def delete_device(device_id):
    """
    Delete a device token
    ---
    tags:
      - Device
    security:
      - Bearer: []
    parameters:
      - name: device_id
        in: path
        type: integer
        required: true
        description: Device ID
    responses:
      200:
        description: Device token deleted successfully
      404:
        description: Device not found
      401:
        description: Unauthorized
    """
    user_id = get_jwt_identity()
    deleted = UserDeviceRepository.delete_device(device_id, user_id)
    
    if not deleted:
        return jsonify({'error': 'Device not found'}), 404
    
    return jsonify({
        'message': 'Device token removed successfully'
    }), 200
