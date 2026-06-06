from flask import Blueprint, jsonify, request
from utils import jwt_required
from services.analytics_service import AnalyticsService
from repositories.daily_streak_repository import DailyStreakRepository
from datetime import datetime, date
import calendar

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


@analytics_bp.route('/summary', methods=['GET'])
@jwt_required
def get_summary():
    """
    Get analytics summary (total logged, streak, avg calories, trends, macros, weight, health alerts)
    ---
    tags:
      - Analytics
    security:
      - Bearer: []
    parameters:
      - name: period
        in: query
        type: string
        default: week
        description: "Use 'week' for the last 7 days, or a month name for a full calendar month (e.g. january, february, june)"
    responses:
      200:
        description: Analytics summary
        schema:
          type: object
          properties:
            period:
              type: string
            total_logged_kcal:
              type: number
            current_streak_days:
              type: integer
            avg_calories:
              type: number
            avg_sugar_g:
              type: number
            calorie_target:
              type: number
            calories_trend:
              type: array
            today_macros:
              type: object
            weight_trend:
              type: array
            health_alerts:
              type: array
    """
    MONTH_NAMES = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }
    period = request.args.get('period', 'week').lower()
    if period not in ('week',) and period not in MONTH_NAMES:
        return jsonify({'error': "period must be 'week' or a month name (e.g. 'january')"}), 400

    user_id = request.current_user_id
    month_number = MONTH_NAMES.get(period)
    summary = AnalyticsService.get_summary(user_id, period, month_number=month_number)
    return jsonify(summary), 200


@analytics_bp.route('/weight', methods=['POST'])
@jwt_required
def log_weight():
    """
    Log a weight entry
    ---
    tags:
      - Analytics
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - weight_kg
          properties:
            weight_kg:
              type: number
              description: Weight in kilograms
            logged_at:
              type: string
              format: date-time
              description: "ISO 8601 datetime (e.g. 2026-06-05T08:00:00). Defaults to now."
    responses:
      201:
        description: Weight logged successfully
      400:
        description: Bad request
    """
    data = request.get_json()
    if not data or 'weight_kg' not in data:
        return jsonify({'error': 'weight_kg is required'}), 400

    weight_kg = data['weight_kg']
    if not isinstance(weight_kg, (int, float)) or weight_kg <= 0:
        return jsonify({'error': 'weight_kg must be a positive number'}), 400

    logged_at = None
    if data.get('logged_at'):
        try:
            logged_at = datetime.fromisoformat(data['logged_at'])
        except ValueError:
            return jsonify({'error': 'logged_at must be a valid ISO 8601 datetime'}), 400

    user_id = request.current_user_id
    entry = AnalyticsService.log_weight(user_id, weight_kg, logged_at)
    return jsonify({'message': 'Weight logged successfully', 'entry': entry}), 201


@analytics_bp.route('/streaks', methods=['GET'])
@jwt_required
def get_streaks():
    """
    Get streak calendar for a given month
    ---
    tags:
      - Analytics
    security:
      - Bearer: []
    parameters:
      - name: year
        in: query
        type: integer
        description: Year (e.g. 2026). Defaults to current year.
      - name: month
        in: query
        type: integer
        description: Month number 1-12. Defaults to current month.
    responses:
      200:
        description: Streak calendar data
        schema:
          type: object
          properties:
            year:
              type: integer
            month:
              type: integer
            current_streak:
              type: integer
            longest_streak:
              type: integer
            days:
              type: array
              description: One entry per day in the month
    """
    today = date.today()
    year = request.args.get('year', today.year, type=int)
    month = request.args.get('month', today.month, type=int)

    if not (1 <= month <= 12):
        return jsonify({'error': 'month must be between 1 and 12'}), 400

    user_id = request.current_user_id
    streak_dates = DailyStreakRepository.get_streak_dates_for_month(user_id, year, month)
    current_streak = DailyStreakRepository.get_current_streak(user_id)
    longest_streak = DailyStreakRepository.get_longest_streak(user_id)

    last_day = calendar.monthrange(year, month)[1]
    days = []
    for day in range(1, last_day + 1):
        d = date(year, month, day)
        has_streak = d in streak_dates
        is_future = d > today
        days.append({
            'date': d.isoformat(),
            'day': day,
            'has_streak': has_streak,
            'is_future': is_future
        })

    return jsonify({
        'year': year,
        'month': month,
        'current_streak': current_streak,
        'longest_streak': longest_streak,
        'days': days
    }), 200


@analytics_bp.route('/weight', methods=['GET'])
@jwt_required
def get_weight_trend():
    """
    Get weight trend history
    ---
    tags:
      - Analytics
    security:
      - Bearer: []
    parameters:
      - name: days
        in: query
        type: integer
        default: 30
        description: Number of past days to retrieve
    responses:
      200:
        description: Weight log history
    """
    from repositories.weight_log_repository import WeightLogRepository
    days = request.args.get('days', 30, type=int)
    user_id = request.current_user_id
    logs = WeightLogRepository.get_logs(user_id, days=days)
    return jsonify({'weight_trend': [w.to_dict() for w in logs]}), 200
