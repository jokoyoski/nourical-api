from flask import Blueprint, jsonify, request
from datetime import datetime, date
from utils import jwt_required
from services.nutrition_service import NutritionService
from repositories.meal_plan_repository import MealPlanRepository
from repositories.food_log_repository import FoodLogRepository

nutrition_bp = Blueprint('nutrition', __name__, url_prefix='/api/nutrition')

@nutrition_bp.route('/today', methods=['GET'])
@jwt_required
def get_today_summary():
    """
    Get today's calorie and macro summary
    ---
    tags:
      - Nutrition
    security:
      - Bearer: []
    responses:
      200:
        description: Today's nutrition summary
        schema:
          type: object
          properties:
            date:
              type: string
            consumed:
              type: object
              properties:
                calories:
                  type: number
                protein_g:
                  type: number
                carbs_g:
                  type: number
                fat_g:
                  type: number
            targets:
              type: object
              properties:
                calories:
                  type: number
                protein_g:
                  type: number
                carbs_g:
                  type: number
                fat_g:
                  type: number
            remaining_calories:
              type: number
            logs:
              type: array
    """
    user_id = request.current_user_id
    summary = NutritionService.get_today_summary(user_id)
    return jsonify(summary), 200


@nutrition_bp.route('/log', methods=['POST'])
@jwt_required
def log_food():
    """
    Log a food item as eaten
    ---
    tags:
      - Nutrition
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - food_name
            - calories
          properties:
            food_name:
              type: string
            calories:
              type: number
            protein_g:
              type: number
            carbs_g:
              type: number
            fat_g:
              type: number
            meal_type:
              type: string
              enum: [breakfast, lunch, dinner, snack]
            meal_date:
              type: string
              format: date
              description: "Date the food was eaten (e.g. 2026-06-05). Defaults to today if omitted."
            meal_time:
              type: string
              description: "Time the food was eaten in HH:MM format (e.g. 12:00). Optional."
    responses:
      201:
        description: Food logged successfully
      400:
        description: Bad request
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    food_name = data.get('food_name')
    calories = data.get('calories')

    if not food_name or calories is None:
        return jsonify({'error': 'food_name and calories are required'}), 400

    logged_at = None
    meal_date_str = data.get('meal_date')
    meal_time_str = data.get('meal_time') or ''
    if meal_date_str:
        try:
            dt_str = f"{meal_date_str}T{meal_time_str}" if meal_time_str else meal_date_str
            logged_at = datetime.fromisoformat(dt_str)
        except ValueError:
            return jsonify({'error': 'meal_date must be YYYY-MM-DD and meal_time must be HH:MM'}), 400

    user_id = request.current_user_id
    log = NutritionService.log_food(
        user_id=user_id,
        food_name=food_name,
        calories=calories,
        protein_g=data.get('protein_g', 0),
        carbs_g=data.get('carbs_g', 0),
        fat_g=data.get('fat_g', 0),
        meal_type=data.get('meal_type'),
        logged_at=logged_at
    )
    return jsonify({'message': 'Food logged successfully', 'log': log}), 201


@nutrition_bp.route('/log/<int:log_id>', methods=['DELETE'])
@jwt_required
def delete_log(log_id):
    """
    Delete a food log entry
    ---
    tags:
      - Nutrition
    security:
      - Bearer: []
    parameters:
      - name: log_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Log deleted
      404:
        description: Log not found
    """
    user_id = request.current_user_id
    deleted = NutritionService.delete_log(log_id, user_id)
    if not deleted:
        return jsonify({'error': 'Log not found'}), 404
    return jsonify({'message': 'Log deleted successfully'}), 200


@nutrition_bp.route('/today/meals', methods=['GET'])
@jwt_required
def get_today_meals():
    """
    Get today's meals from the saved weekly meal plan
    ---
    tags:
      - Nutrition
    security:
      - Bearer: []
    responses:
      200:
        description: Today's meal plan items grouped by meal type
      404:
        description: No meal plan saved for this week
    """
    user_id = request.current_user_id
    plan = MealPlanRepository.get_current_plan(user_id)
    if not plan:
        return jsonify({'error': 'No meal plan saved for this week'}), 404

    today_name = date.today().strftime('%A').lower()  # e.g. "monday"
    today_items = [item.to_dict() for item in plan.items if item.day == today_name]

    grouped = {}
    for item in today_items:
        meal_type = item['meal_type']
        if meal_type not in grouped:
            grouped[meal_type] = {'meal_type': meal_type, 'time': item['meal_time'], 'foods': []}
        grouped[meal_type]['foods'].append(item)

    sorted_meals = sorted(grouped.values(), key=lambda x: x['time'] or '00:00')

    return jsonify({
        'day': today_name,
        'date': date.today().isoformat(),
        'meals': sorted_meals
    }), 200


@nutrition_bp.route('/meal-plan', methods=['POST'])
@jwt_required
def save_meal_plan():
    """
    Save the AI-generated weekly meal plan for the current week
    ---
    tags:
      - Nutrition
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - data
          properties:
            data:
              type: object
              description: The 'data' field returned from GET /api/ai/suggestions
    responses:
      201:
        description: Meal plan saved
      400:
        description: Bad request
    """
    body = request.get_json()
    if not body or 'data' not in body:
        return jsonify({'error': "'data' field is required (pass the response from /api/ai/suggestions)"}), 400

    user_id = request.current_user_id
    plan = MealPlanRepository.save_plan(user_id, body['data'])
    return jsonify({
        'message': 'Meal plan saved successfully',
        'meal_plan': plan.to_dict()
    }), 201


@nutrition_bp.route('/meal-plan', methods=['GET'])
@jwt_required
def get_meal_plan():
    """
    Get the current week's saved meal plan
    ---
    tags:
      - Nutrition
    security:
      - Bearer: []
    responses:
      200:
        description: Current week meal plan
      404:
        description: No meal plan found for this week
    """
    user_id = request.current_user_id
    plan = MealPlanRepository.get_current_plan(user_id)
    if not plan:
        return jsonify({'error': 'No meal plan saved for this week. Call POST /api/ai/suggestions then save it.'}), 404
    return jsonify({'meal_plan': plan.to_dict()}), 200
