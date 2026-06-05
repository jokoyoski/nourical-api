from models import db, FoodLog
from datetime import datetime, date

class FoodLogRepository:
    @staticmethod
    def log_food(user_id, food_name, calories, protein_g, carbs_g, fat_g, meal_type=None):
        log = FoodLog(
            user_id=user_id,
            food_name=food_name,
            calories=calories,
            protein_g=protein_g,
            carbs_g=carbs_g,
            fat_g=fat_g,
            meal_type=meal_type
        )
        db.session.add(log)
        db.session.commit()
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
