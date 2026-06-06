from flask import Blueprint, jsonify, request
from services import GoalsService
from services.ai_suggestion_service import AISuggestionService

goals_bp = Blueprint('goals', __name__, url_prefix='/api/goals')

@goals_bp.route('/', methods=['GET'])
def get_goals():
    """
    Get available health goals
    ---
    tags:
      - Goals
    responses:
      200:
        description: List of available goals
        schema:
          type: object
          properties:
            goals:
              type: array
              items:
                type: object
                properties:
                  value:
                    type: string
                  label:
                    type: string
                  description:
                    type: string
    """
    goals = GoalsService.get_goals()
    
    return jsonify({
        "goals": goals
    }), 200

@goals_bp.route('/activity-levels', methods=['GET'])
def get_activity_levels():
    """
    Get available activity levels
    ---
    tags:
      - Goals
    responses:
      200:
        description: List of available activity levels
        schema:
          type: object
          properties:
            activity_levels:
              type: array
              items:
                type: object
                properties:
                  value:
                    type: string
                  label:
                    type: string
                  description:
                    type: string
    """
    activity_levels = GoalsService.get_activity_levels()
    
    return jsonify({
        "activity_levels": activity_levels
    }), 200

@goals_bp.route('/regions', methods=['GET'])
def get_regions():
    """
    Get available regions
    ---
    tags:
      - Goals
    responses:
      200:
        description: List of available regions
        schema:
          type: object
          properties:
            regions:
              type: array
              items:
                type: object
                properties:
                  value:
                    type: string
                  label:
                    type: string
                  continent:
                    type: string
    """
    regions = GoalsService.get_regions()
    
    return jsonify({
        "regions": regions
    }), 200

@goals_bp.route('/cuisines', methods=['GET'])
def get_cuisines():
    """
    Get cuisines for a given region using AI (cached per region)
    ---
    tags:
      - Goals
    parameters:
      - name: region
        in: query
        type: string
        required: true
        description: Region value e.g. west_africa, europe, asia
    responses:
      200:
        description: List of cuisines with image URLs
      400:
        description: region param missing
      500:
        description: AI error
    """
    region = request.args.get('region', '').strip().lower()
    if not region:
        return jsonify({'error': 'region query param is required'}), 400

    try:
        cuisines = AISuggestionService.get_cuisines_by_region(region)
        return jsonify({'region': region, 'cuisines': cuisines}), 200
    except Exception as e:
        print(f'[AI CUISINES ERROR] {e}')
        return jsonify({'error': 'Failed to fetch cuisines. Please try again.'}), 500

@goals_bp.route('/health-conditions', methods=['GET'])
def get_health_conditions():
    """
    Get available health conditions (mock data)
    ---
    tags:
      - Goals
    responses:
      200:
        description: List of available health conditions
        schema:
          type: object
          properties:
            health_conditions:
              type: array
              items:
                type: object
                properties:
                  value:
                    type: string
                  label:
                    type: string
                  description:
                    type: string
    """
    health_conditions = GoalsService.get_health_conditions()
    
    return jsonify({
        "health_conditions": health_conditions
    }), 200
