from models import db, FoodToAvoid
from sqlalchemy.exc import IntegrityError


class FoodToAvoidRepository:
    @staticmethod
    def get_all(user_id):
        return FoodToAvoid.query.filter_by(user_id=user_id).order_by(FoodToAvoid.food_name).all()

    @staticmethod
    def add(user_id, food_name):
        entry = FoodToAvoid(user_id=user_id, food_name=food_name.strip().lower())
        db.session.add(entry)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return FoodToAvoid.query.filter_by(user_id=user_id, food_name=food_name.strip().lower()).first()
        return entry

    @staticmethod
    def add_bulk(user_id, food_names):
        results = []
        for name in food_names:
            entry = FoodToAvoidRepository.add(user_id, name)
            if entry:
                results.append(entry)
        return results

    @staticmethod
    def delete(user_id, food_id):
        entry = FoodToAvoid.query.filter_by(id=food_id, user_id=user_id).first()
        if not entry:
            return False
        db.session.delete(entry)
        db.session.commit()
        return True

    @staticmethod
    def get_names(user_id):
        rows = FoodToAvoid.query.filter_by(user_id=user_id).all()
        return [r.food_name for r in rows]
