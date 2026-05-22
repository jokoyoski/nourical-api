from models import db, OnboardingData
from datetime import datetime
import json

class OnboardingRepository:
    @staticmethod
    def create_onboarding_data(user_id, data):
        onboarding = OnboardingData(
            user_id=user_id,
            main_goal=data.get('main_goal'),
            age=data.get('age'),
            gender=data.get('gender'),
            height_cm=data.get('height_cm'),
            weight_kg=data.get('weight_kg'),
            target_weight_kg=data.get('target_weight_kg'),
            activity_level=data.get('activity_level'),
            region=data.get('region'),
            dietary_preferences=json.dumps(data.get('dietary_preferences', [])),
            cuisine_preferences=json.dumps(data.get('cuisine_preferences', [])),
            health_conditions=json.dumps(data.get('health_conditions', []))
        )
        db.session.add(onboarding)
        db.session.commit()
        return onboarding
    
    @staticmethod
    def update_onboarding_data(user_id, data):
        onboarding = OnboardingData.query.filter_by(user_id=user_id).first()
        if not onboarding:
            return None
        
        if 'main_goal' in data:
            onboarding.main_goal = data['main_goal']
        if 'age' in data:
            onboarding.age = data['age']
        if 'gender' in data:
            onboarding.gender = data['gender']
        if 'height_cm' in data:
            onboarding.height_cm = data['height_cm']
        if 'weight_kg' in data:
            onboarding.weight_kg = data['weight_kg']
        if 'target_weight_kg' in data:
            onboarding.target_weight_kg = data['target_weight_kg']
        if 'activity_level' in data:
            onboarding.activity_level = data['activity_level']
        if 'region' in data:
            onboarding.region = data['region']
        if 'dietary_preferences' in data:
            onboarding.dietary_preferences = json.dumps(data['dietary_preferences'])
        if 'cuisine_preferences' in data:
            onboarding.cuisine_preferences = json.dumps(data['cuisine_preferences'])
        if 'health_conditions' in data:
            onboarding.health_conditions = json.dumps(data['health_conditions'])
        
        onboarding.updated_at = datetime.utcnow()
        db.session.commit()
        return onboarding
    
    @staticmethod
    def get_onboarding_data(user_id):
        return OnboardingData.query.filter_by(user_id=user_id).first()
