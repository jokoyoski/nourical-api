from models import db, User, OTP
from datetime import datetime, timedelta

class UserRepository:
    @staticmethod
    def create_user(full_name, email, password):
        user = User(
            full_name=full_name,
            email=email.lower()
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email.lower()).first()
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def verify_user(user):
        user.is_verified = True
        db.session.commit()
        return user
    
    @staticmethod
    def update_password(user, new_password):
        user.set_password(new_password)
        db.session.commit()
        return user

class OTPRepository:
    @staticmethod
    def create_otp(user_id, code):
        otp = OTP(
            user_id=user_id,
            code=code,
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        db.session.add(otp)
        db.session.commit()
        return otp
    
    @staticmethod
    def get_valid_otp(user_id, code):
        return OTP.query.filter_by(
            user_id=user_id,
            code=code,
            is_used=False
        ).order_by(OTP.created_at.desc()).first()
    
    @staticmethod
    def mark_otp_used(otp):
        otp.is_used = True
        db.session.commit()
        return otp
