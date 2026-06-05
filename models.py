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

class WeeklyMealPlan(db.Model):
    __tablename__ = 'weekly_meal_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    week_start = db.Column(db.Date, nullable=False)  # Monday of the week
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('meal_plans', lazy=True, cascade='all, delete-orphan'))
    items = db.relationship('MealPlanItem', backref='plan', lazy=True, cascade='all, delete-orphan')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'week_start', name='unique_user_week_plan'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'week_start': self.week_start.isoformat(),
            'created_at': self.created_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }


class MealPlanItem(db.Model):
    __tablename__ = 'meal_plan_items'

    id = db.Column(db.Integer, primary_key=True)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('weekly_meal_plans.id'), nullable=False)
    day = db.Column(db.String(20), nullable=False)       # monday, tuesday, ...
    meal_type = db.Column(db.String(20), nullable=False) # breakfast, lunch, dinner
    meal_time = db.Column(db.String(5))                  # HH:MM
    food_name = db.Column(db.String(200), nullable=False)
    calories = db.Column(db.Float, default=0)
    protein_g = db.Column(db.Float, default=0)
    carbs_g = db.Column(db.Float, default=0)
    fat_g = db.Column(db.Float, default=0)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    is_eaten = db.Column(db.Boolean, default=False, nullable=False)
    eaten_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'meal_plan_id': self.meal_plan_id,
            'day': self.day,
            'meal_type': self.meal_type,
            'meal_time': self.meal_time,
            'food_name': self.food_name,
            'calories': self.calories,
            'protein_g': self.protein_g,
            'carbs_g': self.carbs_g,
            'fat_g': self.fat_g,
            'description': self.description,
            'image_url': self.image_url,
            'is_eaten': self.is_eaten,
            'eaten_at': self.eaten_at.isoformat() if self.eaten_at else None
        }


class FoodLog(db.Model):
    __tablename__ = 'food_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_name = db.Column(db.String(200), nullable=False)
    calories = db.Column(db.Float, default=0, nullable=False)
    protein_g = db.Column(db.Float, default=0, nullable=False)
    carbs_g = db.Column(db.Float, default=0, nullable=False)
    fat_g = db.Column(db.Float, default=0, nullable=False)
    meal_type = db.Column(db.String(50))  # breakfast, lunch, dinner, snack
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('food_logs', lazy=True, cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'food_name': self.food_name,
            'calories': self.calories,
            'protein_g': self.protein_g,
            'carbs_g': self.carbs_g,
            'fat_g': self.fat_g,
            'meal_type': self.meal_type,
            'logged_at': self.logged_at.isoformat()
        }

class NotificationPreferences(db.Model):
    __tablename__ = 'notification_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    meal_reminders = db.Column(db.Boolean, default=True, nullable=False)
    hydration_nudges = db.Column(db.Boolean, default=True, nullable=False)
    weigh_in_prompts = db.Column(db.Boolean, default=True, nullable=False)
    health_alerts = db.Column(db.Boolean, default=True, nullable=False)
    weekly_insights = db.Column(db.Boolean, default=True, nullable=False)
    streak_celebrations = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('notification_preferences', uselist=False, cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'meal_reminders': self.meal_reminders,
            'hydration_nudges': self.hydration_nudges,
            'weigh_in_prompts': self.weigh_in_prompts,
            'health_alerts': self.health_alerts,
            'weekly_insights': self.weekly_insights,
            'streak_celebrations': self.streak_celebrations,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
