from flask import Blueprint, request, jsonify
from services import AuthService
from utils import jwt_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

auth_service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user and send OTP
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - full_name
            - email
            - password
          properties:
            full_name:
              type: string
            email:
              type: string
            password:
              type: string
    responses:
      201:
        description: User registered successfully
      400:
        description: Bad request
    """
    data = request.get_json()
    
    if not data or not all(k in data for k in ['full_name', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user, otp_code = auth_service.register_user(data['full_name'], data['email'], data['password'])
    
    if not user:
        return jsonify({'error': otp_code}), 400
    
    return jsonify({
        'message': 'User registered successfully. Please check your email for OTP.',
        'user_id': user.id,
    }), 201

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """
    Verify OTP and activate account
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - otp
          properties:
            email:
              type: string
            otp:
              type: string
    responses:
      200:
        description: OTP verified successfully
      400:
        description: Invalid or expired OTP
      404:
        description: User not found
    """
    data = request.get_json()
    
    if not data or not all(k in data for k in ['email', 'otp']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user, error = auth_service.verify_otp(data['email'], data['otp'])
    
    if not user:
        return jsonify({'error': error}), 400 if error != "User not found" else 404
    
    return jsonify({
        'message': 'Account verified successfully'
    }), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login with email and password
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          example:
            email: jookoyoski@gmail.com
            password: password123
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
      403:
        description: Account not verified
    """
    data = request.get_json()
    
    if not data or not all(k in data for k in ['email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user, token, error = auth_service.login_user(data['email'], data['password'])
    
    if not user:
        status_code = 403 if "verify" in error else 401
        return jsonify({'error': error}), status_code
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'token': token
    }), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Request password reset - send OTP to user's email
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
          properties:
            email:
              type: string
    responses:
      200:
        description: OTP sent successfully
      404:
        description: User not found
    """
    data = request.get_json()
    
    if not data or 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400
    
    user, otp_code = auth_service.forgot_password(data['email'])
    
    if not user:
        return jsonify({'error': otp_code}), 404
    
    return jsonify({
        'message': 'Password reset OTP sent to your email',
    }), 200

@auth_bp.route('/verify-reset-otp', methods=['POST'])
def verify_reset_otp():
    """
    Verify OTP for password reset
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - otp
          properties:
            email:
              type: string
            otp:
              type: string
    responses:
      200:
        description: OTP verified successfully
      400:
        description: Invalid or expired OTP
      404:
        description: User not found
    """
    data = request.get_json()
    
    if not data or not all(k in data for k in ['email', 'otp']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    reset_token, error = auth_service.verify_reset_otp(data['email'], data['otp'])
    
    if not reset_token:
        status_code = 404 if error == "User not found" else 400
        return jsonify({'error': error}), status_code
    
    return jsonify({
        'message': 'OTP verified successfully. You can now reset your password.',
        'reset_token': reset_token
    }), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Reset password with new password
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - new_password
            - reset_token
          properties:
            email:
              type: string
            new_password:
              type: string
            reset_token:
              type: string
    responses:
      200:
        description: Password reset successful
      404:
        description: User not found
    """
    data = request.get_json()
    
    if not data or not all(k in data for k in ['email', 'new_password', 'reset_token']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user, error = auth_service.reset_password(data['email'], data['new_password'])
    
    if not user:
        return jsonify({'error': error}), 404
    
    return jsonify({
        'message': 'Password reset successfully. You can now login with your new password.'
    }), 200

@auth_bp.route('/verify-password', methods=['POST'])
@jwt_required
def verify_password():
    """
    Verify current password before changing it
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - current_password
          properties:
            current_password:
              type: string
    responses:
      200:
        description: Password verified successfully
      400:
        description: Missing fields
      401:
        description: Password does not match
    """
    data = request.get_json()
    if not data or 'current_password' not in data:
        return jsonify({'error': 'current_password is required'}), 400

    user_id = request.current_user_id
    valid, error = auth_service.verify_current_password(user_id, data['current_password'])
    if not valid:
        return jsonify({'error': error}), 401

    return jsonify({'message': 'Password verified successfully'}), 200


@auth_bp.route('/change-password', methods=['PATCH'])
@jwt_required
def change_password():
    """
    Change password using current password confirmation
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - current_password
            - new_password
            - confirm_new_password
          properties:
            current_password:
              type: string
            new_password:
              type: string
              minLength: 8
            confirm_new_password:
              type: string
    responses:
      200:
        description: Password updated successfully
      400:
        description: Validation error
      401:
        description: Current password does not match
    """
    data = request.get_json()
    if not data or not all(k in data for k in ['current_password', 'new_password', 'confirm_new_password']):
        return jsonify({'error': 'current_password, new_password and confirm_new_password are required'}), 400

    if data['new_password'] != data['confirm_new_password']:
        return jsonify({'error': "Passwords don't match. Double-check and try again."}), 400

    if len(data['new_password']) < 8:
        return jsonify({'error': 'New password must be at least 8 characters long'}), 400

    user_id = request.current_user_id
    success, error = auth_service.change_password(user_id, data['current_password'], data['new_password'])
    if not success:
        return jsonify({'error': error}), 401

    return jsonify({'message': 'Password updated successfully. Please log in with your new password.'}), 200


@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    """
    Resend OTP to user's email
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
          properties:
            email:
              type: string
    responses:
      200:
        description: OTP sent successfully
      404:
        description: User not found
    """
    data = request.get_json()
    
    if not data or 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400
    
    user, otp_code = auth_service.resend_otp(data['email'])
    
    if not user:
        return jsonify({'error': otp_code}), 404
    
    return jsonify({
        'message': 'OTP sent successfully',
    }), 200
