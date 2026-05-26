from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    otps = db.relationship('OTP', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat()
        }

class OTP(db.Model):
    __tablename__ = 'otps'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def is_valid(self):
        return not self.is_used and datetime.utcnow() < self.expires_at

class MealTime(db.Model):
    __tablename__ = 'meal_times'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    meal_type = db.Column(db.String(50), nullable=False)  # breakfast, lunch, dinner
    time = db.Column(db.String(5), nullable=False)  # HH:MM format
    enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('meal_times', lazy=True, cascade='all, delete-orphan'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'meal_type': self.meal_type,
            'time': self.time,
            'enabled': self.enabled
        }

class OnboardingData(db.Model):
    __tablename__ = 'onboarding_data'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    main_goal = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    height_cm = db.Column(db.Integer)
    weight_kg = db.Column(db.Float)
    target_weight_kg = db.Column(db.Float)
    activity_level = db.Column(db.String(100))
    region = db.Column(db.String(100))
    dietary_preferences = db.Column(db.Text)  # Store as comma-separated string or JSON
    cuisine_preferences = db.Column(db.Text)  # Store as comma-separated string or JSON
    health_conditions = db.Column(db.Text)  # Store as comma-separated string or JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('onboarding_data', uselist=False, cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'main_goal': self.main_goal,
            'age': self.age,
            'gender': self.gender,
            'height_cm': self.height_cm,
            'weight_kg': self.weight_kg,
            'target_weight_kg': self.target_weight_kg,
            'activity_level': self.activity_level,
            'region': self.region,
            'dietary_preferences': self.dietary_preferences,
            'cuisine_preferences': self.cuisine_preferences,
            'health_conditions': self.health_conditions
        }

class UserDevice(db.Model):
    __tablename__ = 'user_devices'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    device_token = db.Column(db.String(500), nullable=False)
    platform = db.Column(db.String(20), nullable=False)  # ios, android, or web
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('devices', lazy=True, cascade='all, delete-orphan'))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'device_token', name='unique_user_device_token'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'device_token': self.device_token,
            'platform': self.platform,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
