from flask import Blueprint, request, jsonify
from services import PreferencesService
from repositories.user_targets_repository import UserTargetsRepository
from repositories.food_to_avoid_repository import FoodToAvoidRepository
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
    Upsert user's meal times (creates if not exist, updates if they do)
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
            hydration_nudges:
              type: boolean
            weigh_in_prompts:
              type: boolean
            health_alerts:
              type: boolean
            weekly_insights:
              type: boolean
            streak_celebrations:
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
    preferences = PreferencesService.set_notification_preferences(user_id, **data)
    
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
          example:
            main_goal: lose_weight
            age: 30
            gender: male
            height_cm: 175
            weight_kg: 80
            target_weight_kg: 75
            activity_level: moderately_active
            region: west_africa
            dietary_preferences: ["vegetarian"]
            cuisine_preferences: ["nigerian"]
            health_conditions: ["diabetes"]
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

    VALID_MAIN_GOALS = {'lose_weight', 'maintain_weight', 'gain_muscle', 'improve_overall_health', 'manage_conditions'}
    VALID_GENDERS = {'male', 'female', 'other'}
    VALID_ACTIVITY_LEVELS = {'sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extremely_active'}
    VALID_REGIONS = {'europe', 'north_america', 'latin_america', 'south_america', 'east_africa', 'southern_africa', 'west_africa', 'north_africa', 'asia', 'oceania'}
    VALID_DIETARY_PREFERENCES = {'vegetarian', 'vegan', 'pescatarian', 'halal', 'kosher', 'gluten_free', 'dairy_free', 'none'}
    VALID_CUISINE_PREFERENCES = {'nigerian', 'ghanaian', 'ethiopian', 'kenyan', 'south_african', 'mediterranean', 'asian', 'american', 'european', 'other', 'ivorian', 'senegalese', 'cameroonian'}
    VALID_HEALTH_CONDITIONS = {'diabetes', 'high_blood_pressure', 'high_cholesterol', 'cancer', 'heart_disease', 'kidney_disease', 'pregnancy', 'other', 'prefer_not_to_say'}

    errors = {}

    if 'main_goal' in data and data['main_goal'] not in VALID_MAIN_GOALS:
        errors['main_goal'] = f"Must be one of: {', '.join(sorted(VALID_MAIN_GOALS))}"

    if 'gender' in data and data['gender'] not in VALID_GENDERS:
        errors['gender'] = f"Must be one of: {', '.join(sorted(VALID_GENDERS))}"

    if 'activity_level' in data and data['activity_level'] not in VALID_ACTIVITY_LEVELS:
        errors['activity_level'] = f"Must be one of: {', '.join(sorted(VALID_ACTIVITY_LEVELS))}"

    if 'region' in data and data['region'] not in VALID_REGIONS:
        errors['region'] = f"Must be one of: {', '.join(sorted(VALID_REGIONS))}"

    if 'dietary_preferences' in data:
        invalid = [v for v in data['dietary_preferences'] if v not in VALID_DIETARY_PREFERENCES]
        if invalid:
            errors['dietary_preferences'] = f"Invalid values {invalid}. Must be from: {', '.join(sorted(VALID_DIETARY_PREFERENCES))}"

    if 'cuisine_preferences' in data:
        invalid = [v for v in data['cuisine_preferences'] if v not in VALID_CUISINE_PREFERENCES]
        if invalid:
            errors['cuisine_preferences'] = f"Invalid values {invalid}. Must be from: {', '.join(sorted(VALID_CUISINE_PREFERENCES))}"

    if 'health_conditions' in data:
        invalid = [v for v in data['health_conditions'] if v not in VALID_HEALTH_CONDITIONS]
        if invalid:
            errors['health_conditions'] = f"Invalid values {invalid}. Must be from: {', '.join(sorted(VALID_HEALTH_CONDITIONS))}"

    if errors:
        return jsonify({'error': 'Validation failed', 'details': errors}), 400

    user_id = request.current_user_id
    onboarding_data, status = PreferencesService.save_onboarding_data(user_id, data)
    
    status_code = 200 if status == "updated" else 201
    
    return jsonify({
        'message': f'Onboarding data {status} successfully',
        'data': onboarding_data
    }), status_code

@preferences_bp.route('/goals', methods=['PATCH'])
@jwt_required
def update_goals():
    """
    Update user's primary health goal
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
            - main_goal
          properties:
            main_goal:
              type: string
              enum: [lose_weight, maintain_weight, gain_muscle, improve_overall_health, manage_conditions]
    responses:
      200:
        description: Goal updated successfully
      400:
        description: Bad request
      404:
        description: Onboarding data not found
    """
    data = request.get_json()
    if not data or 'main_goal' not in data:
        return jsonify({'error': 'main_goal is required'}), 400

    VALID_MAIN_GOALS = {'lose_weight', 'maintain_weight', 'gain_muscle', 'improve_overall_health', 'manage_conditions'}
    if data['main_goal'] not in VALID_MAIN_GOALS:
        return jsonify({'error': f"main_goal must be one of: {', '.join(sorted(VALID_MAIN_GOALS))}"}), 400

    user_id = request.current_user_id
    updated = PreferencesService.update_onboarding_fields(user_id, {'main_goal': data['main_goal']})
    if not updated:
        return jsonify({'error': 'Onboarding data not found. Complete onboarding first.'}), 404

    UserTargetsRepository.clear(user_id)
    return jsonify({'message': 'Goal updated successfully', 'data': updated}), 200


@preferences_bp.route('/health-conditions', methods=['PATCH'])
@jwt_required
def update_health_conditions():
    """
    Update user's health conditions
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
            - health_conditions
          properties:
            health_conditions:
              type: array
              items:
                type: string
                enum:
                  - type_2_diabetes
                  - hypertension
                  - high_cholesterol
                  - pcos
                  - gout
                  - kidney_disease
                  - heart_disease
                  - anemia
                  - celiac_disease
                  - lactose_intolerance
                  - ibs
                  - hypothyroidism
                  - cancer
                  - pregnancy
                  - other
                  - prefer_not_to_say
    responses:
      200:
        description: Health conditions updated successfully
      400:
        description: Bad request
      404:
        description: Onboarding data not found
    """
    data = request.get_json()
    if not data or 'health_conditions' not in data:
        return jsonify({'error': 'health_conditions is required'}), 400

    VALID_CONDITIONS = {
        'type_2_diabetes', 'hypertension', 'high_cholesterol', 'pcos', 'gout',
        'kidney_disease', 'heart_disease', 'anemia', 'celiac_disease',
        'lactose_intolerance', 'ibs', 'hypothyroidism', 'cancer', 'pregnancy',
        'other', 'prefer_not_to_say'
    }
    invalid = [v for v in data['health_conditions'] if v not in VALID_CONDITIONS]
    if invalid:
        return jsonify({'error': f"Invalid conditions: {invalid}. Must be from: {', '.join(sorted(VALID_CONDITIONS))}"}), 400

    user_id = request.current_user_id
    updated = PreferencesService.update_onboarding_fields(user_id, {'health_conditions': data['health_conditions']})
    if not updated:
        return jsonify({'error': 'Onboarding data not found. Complete onboarding first.'}), 404

    UserTargetsRepository.clear(user_id)
    return jsonify({'message': 'Health conditions updated successfully', 'data': updated}), 200


@preferences_bp.route('/body-measurements', methods=['PATCH'])
@jwt_required
def update_body_measurements():
    """
    Update user's body measurements
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
            weight_kg:
              type: number
              description: Current weight in kilograms
            height_cm:
              type: number
              description: Height in centimeters
            target_weight_kg:
              type: number
              description: Target weight in kilograms
    responses:
      200:
        description: Body measurements updated successfully
      400:
        description: Bad request
      404:
        description: Onboarding data not found
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    allowed = {'weight_kg', 'height_cm', 'target_weight_kg'}
    fields = {k: v for k, v in data.items() if k in allowed}
    if not fields:
        return jsonify({'error': f"At least one of {sorted(allowed)} is required"}), 400

    for field, value in fields.items():
        if not isinstance(value, (int, float)) or value <= 0:
            return jsonify({'error': f"{field} must be a positive number"}), 400

    user_id = request.current_user_id
    updated = PreferencesService.update_onboarding_fields(user_id, fields)
    if not updated:
        return jsonify({'error': 'Onboarding data not found. Complete onboarding first.'}), 404

    UserTargetsRepository.clear(user_id)
    return jsonify({'message': 'Body measurements updated successfully', 'data': updated}), 200


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


@preferences_bp.route('/foods-to-avoid', methods=['GET'])
@jwt_required
def get_foods_to_avoid():
    """
    Get all foods the user wants to avoid in meal plans
    ---
    tags:
      - Preferences
    security:
      - Bearer: []
    responses:
      200:
        description: List of foods to avoid
    """
    user_id = request.current_user_id
    items = FoodToAvoidRepository.get_all(user_id)
    return jsonify({'foods_to_avoid': [i.to_dict() for i in items]}), 200


@preferences_bp.route('/foods-to-avoid', methods=['POST'])
@jwt_required
def add_foods_to_avoid():
    """
    Add one or more foods to avoid (excluded from AI meal plan suggestions)
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
            foods:
              type: array
              items:
                type: string
              example: ["peanuts", "dairy", "mustard"]
    responses:
      201:
        description: Foods added
      400:
        description: Bad request
    """
    user_id = request.current_user_id
    data = request.get_json()
    foods = data.get('foods') if data else None
    if not foods or not isinstance(foods, list):
        return jsonify({'error': '"foods" must be a non-empty list of strings'}), 400
    added = FoodToAvoidRepository.add_bulk(user_id, foods)
    return jsonify({'message': f'{len(added)} food(s) added', 'foods_to_avoid': [i.to_dict() for i in added]}), 201


@preferences_bp.route('/foods-to-avoid/<int:food_id>', methods=['DELETE'])
@jwt_required
def delete_food_to_avoid(food_id):
    """
    Remove a food from the avoid list
    ---
    tags:
      - Preferences
    security:
      - Bearer: []
    parameters:
      - name: food_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Food removed
      404:
        description: Not found
    """
    user_id = request.current_user_id
    deleted = FoodToAvoidRepository.delete(user_id, food_id)
    if not deleted:
        return jsonify({'error': 'Food not found'}), 404
    return jsonify({'message': 'Food removed from avoid list'}), 200
