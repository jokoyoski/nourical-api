from models import db, NotificationPreferences
from datetime import datetime

class NotificationPreferencesRepository:
    @staticmethod
    def get_or_create_preferences(user_id):
        """
        Get existing preferences or create default preferences for a user.
        
        Args:
            user_id (int): User ID
        
        Returns:
            NotificationPreferences: The preferences object
        """
        preferences = NotificationPreferences.query.filter_by(user_id=user_id).first()
        
        if not preferences:
            # Create default preferences with all set to True
            preferences = NotificationPreferences(
                user_id=user_id,
                meal_reminders=True,
                hydration_nudges=True,
                weigh_in_prompts=True,
                health_alerts=True,
                weekly_insights=True,
                streak_celebrations=True
            )
            db.session.add(preferences)
            db.session.commit()
        
        return preferences
    
    @staticmethod
    def get_preferences(user_id):
        """
        Get notification preferences for a user.
        
        Args:
            user_id (int): User ID
        
        Returns:
            NotificationPreferences: The preferences object or None
        """
        return NotificationPreferences.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def update_preferences(user_id, **kwargs):
        """
        Update notification preferences for a user.
        
        Args:
            user_id (int): User ID
            **kwargs: Any of the preference fields to update
        
        Returns:
            NotificationPreferences: The updated preferences object or None
        """
        preferences = NotificationPreferences.query.filter_by(user_id=user_id).first()
        
        if not preferences:
            return None
        
        # Update only the fields that are provided
        valid_fields = {
            'meal_reminders', 'hydration_nudges', 'weigh_in_prompts',
            'health_alerts', 'weekly_insights', 'streak_celebrations'
        }
        
        for key, value in kwargs.items():
            if key in valid_fields and value is not None:
                setattr(preferences, key, value)
        
        preferences.updated_at = datetime.utcnow()
        db.session.commit()
        
        return preferences
