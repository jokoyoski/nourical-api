from flask import Blueprint, request, jsonify
from services import PreferencesService
from utils import jwt_required

preferences_bp = Blueprint('preferences', __name__, url_prefix='/api/preferences')

@preferences_bp.route('/meal-times', methods=['GET'])
@jwt_required
def get_meal_times():
    """
    Get user's meal times
    ---
    tags:
      - Preferences
    security:
      - Bearer: []
    responses:
      200:
        description: List of meal times
      401:
        description: Unauthorized
    """
    user_id = request.current_user_id
    meal_times = PreferencesService.get_meal_times(user_id)
    return jsonify({
        'meal_times': meal_times
    }), 200

@preferences_bp.route('/meal-times', methods=['POST'])
@jwt_required
def set_meal_times():
    """
    Set user's meal times
    ---
    tags:
      - Preferences
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - meal_times
          properties:
            meal_times:
              type: array
              items:
                type: object
                properties:
                  meal_type:
                    type: string
                    enum: [breakfast, lunch, dinner]
                  time:
                    type: string
                    pattern: "^([01]?[0-9]|2[0-3]):[0-5][0-9]$"
                  enabled:
                    type: boolean
    responses:
      201:
        description: Meal times saved successfully
      400:
        description: Bad request
    """
    data = request.get_json()
    
    if not data or 'meal_times' not in data:
        return jsonify({'error': 'meal_times is required'}), 400
    
    user_id = request.current_user_id
    meal_times = PreferencesService.set_meal_times(user_id, data['meal_times'])
    
    return jsonify({
        'message': 'Meal times saved successfully',
        'meal_times': meal_times
    }), 201

@preferences_bp.route('/notifications', methods=['GET'])
@jwt_required
def get_notification_preferences():
    """
    Get user's notification preferences
    ---
    tags:
      - Preferences
    security:
      - Bearer: []
    responses:
      200:
        description: Notification preferences retrieved
      401:
        description: Unauthorized
    """
    user_id = request.current_user_id
    preferences = PreferencesService.get_notification_preferences(user_id)
    
    return jsonify({
        'preferences': preferences
    }), 200

@preferences_bp.route('/notifications', methods=['POST'])
@jwt_required
def set_notification_preferences():
    """
    Set user's notification preferences
    ---
    tags:
      - Preferences
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            meal_reminders:
              type: boolean
            daily_summary:
              type: boolean
    responses:
      200:
        description: Notification preferences saved
      400:
        description: Bad request
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    user_id = request.current_user_id
    preferences = PreferencesService.set_notification_preferences(
        user_id,
        meal_reminders=data.get('meal_reminders'),
        daily_summary=data.get('daily_summary')
    )
    
    return jsonify({
        'message': 'Notification preferences saved successfully',
        'preferences': preferences
    }), 200

@preferences_bp.route('/onboarding', methods=['POST'])
@jwt_required
def save_onboarding_data():
    """
    Save user's onboarding data
    ---
    tags:
      - Preferences
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            main_goal:
              type: string
            age:
              type: integer
            gender:
              type: string
            height_cm:
              type: integer
            weight_kg:
              type: number
            target_weight_kg:
              type: number
            activity_level:
              type: string
            region:
              type: string
            dietary_preferences:
              type: array
              items:
                type: string
            cuisine_preferences:
              type: array
              items:
                type: string
            health_conditions:
              type: array
              items:
                type: string
    responses:
      201:
        description: Onboarding data saved successfully
      200:
        description: Onboarding data updated successfully
      400:
        description: Bad request
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    user_id = request.current_user_id
    onboarding_data, status = PreferencesService.save_onboarding_data(user_id, data)
    
    status_code = 200 if status == "updated" else 201
    
    return jsonify({
        'message': f'Onboarding data {status} successfully',
        'data': onboarding_data
    }), status_code

@preferences_bp.route('/onboarding', methods=['GET'])
@jwt_required
def get_onboarding_data():
    """
    Get user's onboarding data
    ---
    tags:
      - Preferences
    security:
      - Bearer: []
    responses:
      200:
        description: Onboarding data retrieved
      404:
        description: Onboarding data not found
    """
    data = PreferencesService.get_onboarding_data(request.current_user_id)
    
    if not data:
        return jsonify({'error': 'Onboarding data not found'}), 404
    
    return jsonify({
        'data': data
    }), 200
