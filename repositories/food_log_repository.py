from models import db, FoodLog
from datetime import datetime, date
from repositories.daily_streak_repository import DailyStreakRepository

class FoodLogRepository:
    @staticmethod
    def log_food(user_id, food_name, calories, protein_g, carbs_g, fat_g, meal_type=None, logged_at=None):
        streak_date = logged_at.date() if logged_at else date.today()

        # Upsert: if same user + meal_type + date already exists, override it
        existing = None
        if meal_type:
            existing = FoodLog.query.filter(
                FoodLog.user_id == user_id,
                FoodLog.meal_type == meal_type,
                db.func.date(FoodLog.logged_at) == streak_date
            ).first()

        if existing:
            existing.food_name = food_name
            existing.calories = calories
            existing.protein_g = protein_g
            existing.carbs_g = carbs_g
            existing.fat_g = fat_g
            existing.logged_at = logged_at or existing.logged_at
            db.session.commit()
            DailyStreakRepository.record_today(user_id, for_date=streak_date)
            return existing

        log = FoodLog(
            user_id=user_id,
            food_name=food_name,
            calories=calories,
            protein_g=protein_g,
            carbs_g=carbs_g,
            fat_g=fat_g,
            meal_type=meal_type,
            **({"logged_at": logged_at} if logged_at else {})
        )
        db.session.add(log)
        db.session.commit()
        DailyStreakRepository.record_today(user_id, for_date=streak_date)
        return log

    @staticmethod
    def get_logs_for_date(user_id, target_date=None):
        if target_date is None:
            target_date = date.today()
        return FoodLog.query.filter(
            FoodLog.user_id == user_id,
            db.func.date(FoodLog.logged_at) == target_date
        ).all()

    @staticmethod
    def delete_log(log_id, user_id):
        log = FoodLog.query.filter_by(id=log_id, user_id=user_id).first()
        if not log:
            return False
        db.session.delete(log)
        db.session.commit()
        return True
