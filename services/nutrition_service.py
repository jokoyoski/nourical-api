from repositories.food_log_repository import FoodLogRepository
from repositories.meal_plan_repository import MealPlanRepository
from repositories.onboarding_repository import OnboardingRepository
from repositories.user_targets_repository import UserTargetsRepository
from datetime import date

ACTIVITY_MULTIPLIERS = {
    'sedentary': 1.2,
    'lightly_active': 1.375,
    'moderately_active': 1.55,
    'very_active': 1.725,
    'extra_active': 1.9,
}

GOAL_ADJUSTMENTS = {
    'lose_weight': -500,
    'gain_weight': 500,
    'gain_muscle': 300,
    'maintain_weight': 0,
    'eat_healthy': 0,
}

def calculate_targets(onboarding):
    weight = onboarding.weight_kg or 70
    height = onboarding.height_cm or 170
    age = onboarding.age or 25
    gender = (onboarding.gender or 'male').lower()
    activity = (onboarding.activity_level or 'sedentary').lower().replace(' ', '_')
    goal = (onboarding.main_goal or 'eat_healthy').lower().replace(' ', '_')

    # Harris-Benedict BMR
    if 'female' in gender or 'woman' in gender:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)

    multiplier = ACTIVITY_MULTIPLIERS.get(activity, 1.2)
    adjustment = GOAL_ADJUSTMENTS.get(goal, 0)
    calorie_target = round(bmr * multiplier + adjustment)
    calorie_target = max(calorie_target, 1200)  # minimum safe floor

    # Macro targets
    protein_target = max(round(weight * 1.6), 50)    # 1.6g per kg, min 50g
    fat_target = max(round((calorie_target * 0.25) / 9), 20)  # 25% of calories, min 20g
    carb_target = round((calorie_target - (protein_target * 4) - (fat_target * 9)) / 4)

    return {
        'calories': calorie_target,
        'protein_g': protein_target,
        'carbs_g': max(carb_target, 50),
        'fat_g': fat_target,
    }


class NutritionService:
    @staticmethod
    def log_food(user_id, food_name, calories, protein_g, carbs_g, fat_g, meal_type=None, logged_at=None):
        log = FoodLogRepository.log_food(
            user_id, food_name, calories, protein_g, carbs_g, fat_g, meal_type, logged_at
        )

        if meal_type and logged_at:
            day_name = logged_at.strftime('%A').lower()
            MealPlanRepository.replace_meal_for_day(
                user_id=user_id,
                day_name=day_name,
                meal_type=meal_type,
                food_name=food_name,
                calories=calories,
                protein_g=protein_g,
                carbs_g=carbs_g,
                fat_g=fat_g,
                eaten_at=logged_at
            )

        return log.to_dict()

    @staticmethod
    def get_today_summary(user_id):
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
            import json as _json
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

        logs = FoodLogRepository.get_logs_for_date(user_id, date.today())

        consumed = {
            'calories': round(sum(l.calories for l in logs), 1),
            'protein_g': round(sum(l.protein_g for l in logs), 1),
            'carbs_g': round(sum(l.carbs_g for l in logs), 1),
            'fat_g': round(sum(l.fat_g for l in logs), 1),
        }

        remaining_calories = max(targets['calories'] - consumed['calories'], 0)

        return {
            'date': date.today().isoformat(),
            'consumed': consumed,
            'targets': targets,
            'remaining_calories': remaining_calories,
            'logs': [l.to_dict() for l in logs]
        }

    @staticmethod
    def delete_log(log_id, user_id):
        return FoodLogRepository.delete_log(log_id, user_id)
