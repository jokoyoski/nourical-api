from models import db, UserTargets
from datetime import datetime


class UserTargetsRepository:
    @staticmethod
    def get(user_id):
        return UserTargets.query.filter_by(user_id=user_id).first()

    @staticmethod
    def save(user_id, calories, protein_g, carbs_g, fat_g, reasoning=None):
        existing = UserTargets.query.filter_by(user_id=user_id).first()
        if existing:
            existing.calories = calories
            existing.protein_g = protein_g
            existing.carbs_g = carbs_g
            existing.fat_g = fat_g
            existing.reasoning = reasoning
            existing.generated_at = datetime.utcnow()
        else:
            existing = UserTargets(
                user_id=user_id,
                calories=calories,
                protein_g=protein_g,
                carbs_g=carbs_g,
                fat_g=fat_g,
                reasoning=reasoning
            )
            db.session.add(existing)
        db.session.commit()
        return existing

    @staticmethod
    def clear(user_id):
        UserTargets.query.filter_by(user_id=user_id).delete()
        db.session.commit()
