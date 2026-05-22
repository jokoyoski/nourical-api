from flask import Blueprint, jsonify
from services import GoalsService

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
    Get available cuisines (mock data)
    ---
    tags:
      - Goals
    responses:
      200:
        description: List of available cuisines
        schema:
          type: object
          properties:
            cuisines:
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
    cuisines = GoalsService.get_cuisines()
    
    return jsonify({
        "cuisines": cuisines
    }), 200

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
