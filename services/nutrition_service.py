from repositories.food_log_repository import FoodLogRepository
from repositories.onboarding_repository import OnboardingRepository
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

    # Macro targets
    protein_target = round(weight * 1.6)             # 1.6g per kg
    fat_target = round((calorie_target * 0.25) / 9)  # 25% of calories from fat
    carb_target = round((calorie_target - (protein_target * 4) - (fat_target * 9)) / 4)

    return {
        'calories': calorie_target,
        'protein_g': protein_target,
        'carbs_g': max(carb_target, 0),
        'fat_g': fat_target,
    }


class NutritionService:
    @staticmethod
    def log_food(user_id, food_name, calories, protein_g, carbs_g, fat_g, meal_type=None):
        log = FoodLogRepository.log_food(
            user_id, food_name, calories, protein_g, carbs_g, fat_g, meal_type
        )
        return log.to_dict()

    @staticmethod
    def get_today_summary(user_id):
        onboarding = OnboardingRepository.get_onboarding_data(user_id)
        targets = calculate_targets(onboarding) if onboarding else {
            'calories': 2000, 'protein_g': 50, 'carbs_g': 250, 'fat_g': 65
        }

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
