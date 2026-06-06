from datetime import datetime, date, timedelta
from repositories.food_log_repository import FoodLogRepository
from repositories.weight_log_repository import WeightLogRepository
from repositories.onboarding_repository import OnboardingRepository
from repositories.daily_streak_repository import DailyStreakRepository
from repositories.user_targets_repository import UserTargetsRepository
from models import db, FoodLog, WeightLog
import json as _json


def _get_period_dates(period, month_number=None):
    today = date.today()
    if month_number:
        year = today.year if month_number <= today.month else today.year - 1
        import calendar as _cal
        first_day = date(year, month_number, 1)
        last_day = date(year, month_number, _cal.monthrange(year, month_number)[1])
        return first_day, min(last_day, today)
    else:  # week default
        return today - timedelta(days=6), today


def _get_daily_logs(user_id, since, today):
    logs = (
        FoodLog.query
        .filter(
            FoodLog.user_id == user_id,
            db.func.date(FoodLog.logged_at) >= since,
            db.func.date(FoodLog.logged_at) <= today
        )
        .all()
    )
    # Group by date
    by_date = {}
    d = since
    while d <= today:
        by_date[d.isoformat()] = []
        d += timedelta(days=1)
    for log in logs:
        key = log.logged_at.date().isoformat()
        if key in by_date:
            by_date[key].append(log)
    return by_date


def _calculate_streak(by_date):
    streak = 0
    today = date.today()
    check = today
    while True:
        key = check.isoformat()
        if key in by_date and by_date[key]:
            streak += 1
            check -= timedelta(days=1)
        else:
            break
    return streak


def _build_calories_trend(by_date):
    trend = []
    for day_str, logs in by_date.items():
        total = round(sum(l.calories for l in logs), 1)
        trend.append({'date': day_str, 'calories': total})
    return trend


def _build_weekly_breakdown(by_date):
    weeks = {}
    for day_str, logs in by_date.items():
        d = date.fromisoformat(day_str)
        # week number relative to the earliest date in by_date
        first = date.fromisoformat(min(by_date.keys()))
        week_num = (d - first).days // 7 + 1
        label = f"week_{week_num}"
        if label not in weeks:
            weeks[label] = {'calories': 0, 'protein_g': 0, 'carbs_g': 0, 'fat_g': 0, 'logged_days': 0}
        if logs:
            weeks[label]['calories'] += round(sum(l.calories for l in logs), 1)
            weeks[label]['protein_g'] += round(sum(l.protein_g for l in logs), 1)
            weeks[label]['carbs_g'] += round(sum(l.carbs_g for l in logs), 1)
            weeks[label]['fat_g'] += round(sum(l.fat_g for l in logs), 1)
            weeks[label]['logged_days'] += 1
    return weeks


def _build_health_alerts(by_date, targets, today_logs):
    alerts = []
    today_calories = sum(l.calories for l in today_logs)
    today_protein = sum(l.protein_g for l in today_logs)

    if today_calories < 1200 and today_calories > 0:
        alerts.append({
            'type': 'warning',
            'message': f'Calorie intake below 1,200 today — consider logging more meals'
        })

    # Protein streak check (last 7 days)
    protein_target = targets.get('protein_g', 50)
    protein_hit_days = sum(
        1 for logs in list(by_date.values())[-7:]
        if sum(l.protein_g for l in logs) >= protein_target
    )
    if protein_hit_days >= 3:
        alerts.append({
            'type': 'success',
            'message': f"You've hit your protein goal {protein_hit_days}/7 days this week — great streak!"
        })

    return alerts


class AnalyticsService:
    @staticmethod
    def get_summary(user_id, period='week', month_number=None):
        since, today = _get_period_dates(period, month_number)
        by_date = _get_daily_logs(user_id, since, today)
        today_logs = by_date.get(today.isoformat(), [])

        db_targets = UserTargetsRepository.get(user_id)
        if db_targets:
            targets = {
                'calories': db_targets.calories,
                'protein_g': db_targets.protein_g,
                'carbs_g': db_targets.carbs_g,
                'fat_g': db_targets.fat_g
            }
        else:
            from services.ai_suggestion_service import AISuggestionService
            onboarding = OnboardingRepository.get_onboarding_data(user_id)
            if onboarding:
                onboarding_dict = onboarding.to_dict()
                for field in ['dietary_preferences', 'cuisine_preferences', 'health_conditions']:
                    val = onboarding_dict.get(field)
                    if val:
                        try:
                            onboarding_dict[field] = _json.loads(val)
                        except (ValueError, TypeError):
                            pass
                result = AISuggestionService.get_daily_targets(onboarding_dict)
                saved = UserTargetsRepository.save(
                    user_id=user_id,
                    calories=result['calories'],
                    protein_g=result['protein_g'],
                    carbs_g=result['carbs_g'],
                    fat_g=result['fat_g'],
                    reasoning=result.get('reasoning')
                )
                targets = {'calories': saved.calories, 'protein_g': saved.protein_g, 'carbs_g': saved.carbs_g, 'fat_g': saved.fat_g}
            else:
                targets = {'calories': 2000, 'protein_g': 50, 'carbs_g': 250, 'fat_g': 65}

        logged_days = [logs for logs in by_date.values() if logs]
        total_calories = round(sum(l.calories for logs in by_date.values() for l in logs), 1)
        avg_calories = round(total_calories / len(logged_days), 1) if logged_days else 0
        # Today's macros
        today_macros = {
            'protein': {'consumed': round(sum(l.protein_g for l in today_logs), 1), 'target': targets['protein_g']},
            'carbs':   {'consumed': round(sum(l.carbs_g for l in today_logs), 1),   'target': targets['carbs_g']},
            'fat':     {'consumed': round(sum(l.fat_g for l in today_logs), 1),     'target': targets['fat_g']},
        }

        # Weight trend
        days = (today - since).days + 1 if month_number else 7
        weight_logs = WeightLogRepository.get_logs(user_id, days=days)

        response = {
            'period': period,
            'total_logged_kcal': total_calories,
            'streak_days': DailyStreakRepository.get_current_streak(user_id),
            'avg_calories': avg_calories,
            'calorie_target': targets['calories'],
            'calories_trend': _build_calories_trend(by_date),
            'today_macros': today_macros,
            'weight_trend': [w.to_dict() for w in weight_logs],
            'health_alerts': _build_health_alerts(by_date, targets, today_logs)
        }

        if month_number:
            response['weekly_breakdown'] = _build_weekly_breakdown(by_date)

        return response

    @staticmethod
    def log_weight(user_id, weight_kg, logged_at=None):
        entry = WeightLogRepository.log_weight(user_id, weight_kg, logged_at)
        return entry.to_dict()
