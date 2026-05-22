from repositories import MealTimeRepository, OnboardingRepository
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
    def set_notification_preferences(user_id, meal_reminders, daily_summary):
        # In production, save to database
        return {
            'user_id': user_id,
            'meal_reminders': meal_reminders,
            'daily_summary': daily_summary
        }
    
    @staticmethod
    def save_onboarding_data(user_id, data):
        existing = OnboardingRepository.get_onboarding_data(user_id)
        
        if existing:
            onboarding = OnboardingRepository.update_onboarding_data(user_id, data)
            return onboarding.to_dict(), "updated"
        else:
            onboarding = OnboardingRepository.create_onboarding_data(user_id, data)
            return onboarding.to_dict(), "created"
    
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
