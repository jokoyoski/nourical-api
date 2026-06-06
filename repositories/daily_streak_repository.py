from models import db, DailyStreak
from datetime import date, timedelta
from sqlalchemy.dialects.postgresql import insert as pg_insert


class DailyStreakRepository:
    @staticmethod
    def record_today(user_id, for_date=None):
        """Mark a day as a streak day (idempotent — safe to call multiple times)."""
        streak_date = for_date or date.today()
        existing = DailyStreak.query.filter_by(user_id=user_id, streak_date=streak_date).first()
        if existing:
            return existing
        entry = DailyStreak(user_id=user_id, streak_date=streak_date)
        try:
            db.session.add(entry)
            db.session.commit()
        except Exception:
            db.session.rollback()
            existing = DailyStreak.query.filter_by(user_id=user_id, streak_date=streak_date).first()
            return existing
        return entry

    @staticmethod
    def get_streak_dates_for_month(user_id, year, month):
        from calendar import monthrange
        last_day = monthrange(year, month)[1]
        start = date(year, month, 1)
        end = date(year, month, last_day)
        rows = DailyStreak.query.filter(
            DailyStreak.user_id == user_id,
            DailyStreak.streak_date >= start,
            DailyStreak.streak_date <= end
        ).all()
        return {row.streak_date for row in rows}

    @staticmethod
    def get_current_streak(user_id):
        streak = 0
        check = date.today()
        while True:
            exists = DailyStreak.query.filter_by(user_id=user_id, streak_date=check).first()
            if exists:
                streak += 1
                check -= timedelta(days=1)
            else:
                break
        return streak

    @staticmethod
    def get_longest_streak(user_id):
        rows = (
            DailyStreak.query
            .filter_by(user_id=user_id)
            .order_by(DailyStreak.streak_date.asc())
            .all()
        )
        if not rows:
            return 0
        longest = current = 1
        for i in range(1, len(rows)):
            if (rows[i].streak_date - rows[i - 1].streak_date).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        return longest
