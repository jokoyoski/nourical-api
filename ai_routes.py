from flask import Blueprint, jsonify, request
from utils import jwt_required
from services.ai_suggestion_service import AISuggestionService
from repositories import OnboardingRepository, MealTimeRepository

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')

@ai_bp.route('/suggestions', methods=['GET'])
@jwt_required
def get_ai_suggestions():
    """
    Get AI-powered weekly meal plan based on user profile
    ---
    tags:
      - AI
    security:
      - Bearer: []
    responses:
      200:
        description: Weekly meal plan (Monday to Friday)
        schema:
          type: object
          properties:
            data:
              type: object
              description: Meal plan keyed by day
      400:
        description: Onboarding or meal times not set up
      500:
        description: AI service error
    """
    user_id = request.current_user_id

    onboarding = OnboardingRepository.get_onboarding_data(user_id)
    if not onboarding:
        return jsonify({'error': 'Please complete onboarding before getting AI suggestions'}), 400

    meal_times = MealTimeRepository.get_meal_times(user_id)
    if not meal_times:
        return jsonify({'error': 'Please set up your meal times before getting AI suggestions'}), 400

    import json

    onboarding_dict = onboarding.to_dict()
    for field in ['dietary_preferences', 'cuisine_preferences', 'health_conditions']:
        val = onboarding_dict.get(field)
        if val:
            try:
                onboarding_dict[field] = json.loads(val)
            except (json.JSONDecodeError, TypeError):
                pass

    meal_times_list = [mt.to_dict() for mt in meal_times]

    try:
        meal_plan = AISuggestionService.get_meal_plan(onboarding_dict, meal_times_list)
        return jsonify({'data': meal_plan}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"[AI ERROR] {e}")
        return jsonify({'error': 'Failed to generate meal plan. Please try again.'}), 500
