from repositories import MealTimeRepository, OnboardingRepository
from repositories.notification_preferences_repository import NotificationPreferencesRepository
from models import db, NotificationPreferences, MealTime
import json

class PreferencesService:
    @staticmethod
    def get_meal_times(user_id):
        meal_times = MealTimeRepository.get_meal_times(user_id)
        return [mt.to_dict() for mt in meal_times]
    
    @staticmethod
    def set_meal_times(user_id, meal_times_data):
        meal_times = MealTimeRepository.set_meal_times(user_id, meal_times_data)
        return [mt.to_dict() for mt in meal_times]
    
    @staticmethod
    def get_notification_preferences(user_id):
        """
        Get notification preferences for a user.
        Creates default preferences if they don't exist.
        """
        preferences = NotificationPreferencesRepository.get_or_create_preferences(user_id)
        return preferences.to_dict()
    
    @staticmethod
    def set_notification_preferences(user_id, **kwargs):
        """
        Update notification preferences for a user.
        """
        preferences = NotificationPreferencesRepository.update_preferences(user_id, **kwargs)
        return preferences.to_dict() if preferences else None
    
    @staticmethod
    def save_onboarding_data(user_id, data):
        existing = OnboardingRepository.get_onboarding_data(user_id)
        
        if existing:
            onboarding = OnboardingRepository.update_onboarding_data(user_id, data)
            return onboarding.to_dict(), "updated"
        else:
            onboarding = OnboardingRepository.create_onboarding_data(user_id, data)
            
            # Seed default notification preferences on first onboarding
            notification_prefs = NotificationPreferences(
                user_id=user_id,
                meal_reminders=True,
                hydration_nudges=True,
                weigh_in_prompts=True,
                health_alerts=True,
                weekly_insights=True,
                streak_celebrations=True
            )
            db.session.add(notification_prefs)
            
            # Seed default meal times on first onboarding
            default_meal_times = [
                MealTime(user_id=user_id, meal_type='breakfast', time='07:00', enabled=True),
                MealTime(user_id=user_id, meal_type='lunch', time='12:00', enabled=True),
                MealTime(user_id=user_id, meal_type='dinner', time='19:00', enabled=True),
            ]
            for meal_time in default_meal_times:
                db.session.add(meal_time)
            
            db.session.commit()
            return onboarding.to_dict(), "created"
    
    @staticmethod
    def update_onboarding_fields(user_id, fields):
        existing = OnboardingRepository.get_onboarding_data(user_id)
        if existing:
            updated = OnboardingRepository.update_onboarding_data(user_id, fields)
        else:
            updated = OnboardingRepository.create_onboarding_data(user_id, fields)
        if not updated:
            return None
        data = updated.to_dict()
        for key in ('dietary_preferences', 'cuisine_preferences', 'health_conditions'):
            if data.get(key):
                data[key] = json.loads(data[key])
        return data

    @staticmethod
    def get_onboarding_data(user_id):
        onboarding = OnboardingRepository.get_onboarding_data(user_id)
        if not onboarding:
            return None
        
        data = onboarding.to_dict()
        if data['dietary_preferences']:
            data['dietary_preferences'] = json.loads(data['dietary_preferences'])
        if data['cuisine_preferences']:
            data['cuisine_preferences'] = json.loads(data['cuisine_preferences'])
        if data['health_conditions']:
            data['health_conditions'] = json.loads(data['health_conditions'])
        
        return data
