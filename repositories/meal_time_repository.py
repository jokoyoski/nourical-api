from models import db, MealTime

class MealTimeRepository:
    @staticmethod
    def get_meal_times(user_id):
        return MealTime.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def set_meal_times(user_id, meal_times_data):
        # Delete existing meal times for this user
        MealTime.query.filter_by(user_id=user_id).delete()
        
        # Add new meal times
        for mt_data in meal_times_data:
            meal_time = MealTime(
                user_id=user_id,
                meal_type=mt_data['meal_type'],
                time=mt_data['time'],
                enabled=mt_data.get('enabled', True)
            )
            db.session.add(meal_time)
        
        db.session.commit()
        return MealTime.query.filter_by(user_id=user_id).all()
