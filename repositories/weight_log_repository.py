from models import db, WeightLog
from datetime import datetime, timedelta

class WeightLogRepository:
    @staticmethod
    def log_weight(user_id, weight_kg, logged_at=None):
        entry = WeightLog(
            user_id=user_id,
            weight_kg=weight_kg,
            logged_at=logged_at or datetime.utcnow()
        )
        db.session.add(entry)
        db.session.commit()
        return entry

    @staticmethod
    def get_logs(user_id, days=30):
        since = datetime.utcnow() - timedelta(days=days)
        return (
            WeightLog.query
            .filter(WeightLog.user_id == user_id, WeightLog.logged_at >= since)
            .order_by(WeightLog.logged_at.asc())
            .all()
        )

    @staticmethod
    def get_latest(user_id):
        return (
            WeightLog.query
            .filter_by(user_id=user_id)
            .order_by(WeightLog.logged_at.desc())
            .first()
        )
