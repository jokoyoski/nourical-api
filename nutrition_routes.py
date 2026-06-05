from flask import Blueprint, jsonify, request
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

    user_id = request.current_user_id
    log = NutritionService.log_food(
        user_id=user_id,
        food_name=food_name,
        calories=calories,
        protein_g=data.get('protein_g', 0),
        carbs_g=data.get('carbs_g', 0),
        fat_g=data.get('fat_g', 0),
        meal_type=data.get('meal_type')
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


@nutrition_bp.route('/meal-plan/item/<int:item_id>/eat', methods=['PATCH'])
@jwt_required
def mark_item_eaten(item_id):
    """
    Mark a meal plan food item as eaten (also logs it to daily food log)
    ---
    tags:
      - Nutrition
    security:
      - Bearer: []
    parameters:
      - name: item_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Item marked as eaten
      404:
        description: Item not found
    """
    user_id = request.current_user_id
    item = MealPlanRepository.mark_eaten(item_id, user_id)
    if not item:
        return jsonify({'error': 'Meal plan item not found'}), 404

    # Auto-log to daily food log
    FoodLogRepository.log_food(
        user_id=user_id,
        food_name=item.food_name,
        calories=item.calories,
        protein_g=item.protein_g,
        carbs_g=item.carbs_g,
        fat_g=item.fat_g,
        meal_type=item.meal_type
    )

    return jsonify({
        'message': f'{item.food_name} marked as eaten',
        'item': item.to_dict()
    }), 200


@nutrition_bp.route('/meal-plan/item/<int:item_id>/uneat', methods=['PATCH'])
@jwt_required
def mark_item_uneaten(item_id):
    """
    Unmark a meal plan food item as eaten
    ---
    tags:
      - Nutrition
    security:
      - Bearer: []
    parameters:
      - name: item_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Item unmarked
      404:
        description: Item not found
    """
    user_id = request.current_user_id
    item = MealPlanRepository.mark_uneaten(item_id, user_id)
    if not item:
        return jsonify({'error': 'Meal plan item not found'}), 404
    return jsonify({
        'message': f'{item.food_name} unmarked as eaten',
        'item': item.to_dict()
    }), 200
