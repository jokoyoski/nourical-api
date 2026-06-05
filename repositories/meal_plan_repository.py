from models import db, WeeklyMealPlan, MealPlanItem
from datetime import date, timedelta

def get_week_start(for_date=None):
    """Return the Monday of the current (or given) week."""
    d = for_date or date.today()
    return d - timedelta(days=d.weekday())

class MealPlanRepository:
    @staticmethod
    def save_plan(user_id, meal_plan_data):
        """
        Save or replace the weekly meal plan for the current week.
        meal_plan_data: the 'data' dict from the AI suggestions endpoint.
        """
        week_start = get_week_start()

        # Remove existing plan for this week
        existing = WeeklyMealPlan.query.filter_by(user_id=user_id, week_start=week_start).first()
        if existing:
            db.session.delete(existing)
            db.session.flush()

        plan = WeeklyMealPlan(user_id=user_id, week_start=week_start)
        db.session.add(plan)
        db.session.flush()  # get plan.id

        for day, meals in meal_plan_data.items():
            for meal_type, meal_data in meals.items():
                for food in meal_data.get('foods', []):
                    item = MealPlanItem(
                        meal_plan_id=plan.id,
                        day=day,
                        meal_type=meal_type,
                        meal_time=meal_data.get('time'),
                        food_name=food.get('name', ''),
                        calories=food.get('calories', 0),
                        protein_g=food.get('protein_g', 0),
                        carbs_g=food.get('carbs_g', 0),
                        fat_g=food.get('fat_g', 0),
                        description=food.get('description'),
                        image_url=food.get('image_url'),
                        is_eaten=False
                    )
                    db.session.add(item)

        db.session.commit()
        return plan

    @staticmethod
    def get_current_plan(user_id):
        week_start = get_week_start()
        return WeeklyMealPlan.query.filter_by(user_id=user_id, week_start=week_start).first()

    @staticmethod
    def get_item(item_id, user_id):
        return (
            MealPlanItem.query
            .join(WeeklyMealPlan)
            .filter(MealPlanItem.id == item_id, WeeklyMealPlan.user_id == user_id)
            .first()
        )

    @staticmethod
    def mark_eaten(item_id, user_id):
        from datetime import datetime
        item = MealPlanRepository.get_item(item_id, user_id)
        if not item:
            return None
        item.is_eaten = True
        item.eaten_at = datetime.utcnow()
        db.session.commit()
        return item

    @staticmethod
    def mark_uneaten(item_id, user_id):
        item = MealPlanRepository.get_item(item_id, user_id)
        if not item:
            return None
        item.is_eaten = False
        item.eaten_at = None
        db.session.commit()
        return item
