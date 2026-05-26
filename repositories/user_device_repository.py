from models import db, UserDevice
from datetime import datetime

class UserDeviceRepository:
    @staticmethod
    def register_device(user_id, device_token, platform):
        """
        Register or update a device token for a user.
        
        Args:
            user_id (str or int): User ID (from JWT, may be string)
            device_token (str): FCM device token
            platform (str): Platform (ios, android, or web)
        
        Returns:
            UserDevice: The created or updated device record
        """
        # Convert user_id to int if it's a string
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        # Check if device token already exists for this user
        existing_device = UserDevice.query.filter_by(
            user_id=user_id,
            device_token=device_token
        ).first()
        
        if existing_device:
            # Update platform and timestamp
            existing_device.platform = platform
            existing_device.updated_at = datetime.utcnow()
            db.session.commit()
            return existing_device
        else:
            # Create new device record
            device = UserDevice(
                user_id=user_id,
                device_token=device_token,
                platform=platform
            )
            db.session.add(device)
            db.session.commit()
            return device
    
    @staticmethod
    def get_user_devices(user_id):
        """
        Get all devices for a user.
        
        Args:
            user_id (str or int): User ID (from JWT, may be string)
        
        Returns:
            list: List of UserDevice objects
        """
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        return UserDevice.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_device(device_id, user_id):
        """
        Get a specific device by ID and user ID.
        
        Args:
            device_id (int): Device ID
            user_id (str or int): User ID (from JWT, may be string)
        
        Returns:
            UserDevice: The device record or None
        """
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        return UserDevice.query.filter_by(id=device_id, user_id=user_id).first()
    
    @staticmethod
    def delete_device(device_id, user_id):
        """
        Delete a device by ID and user ID.
        
        Args:
            device_id (int): Device ID
            user_id (str or int): User ID (from JWT, may be string)
        
        Returns:
            bool: True if deleted, False otherwise
        """
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        device = UserDevice.query.filter_by(id=device_id, user_id=user_id).first()
        if device:
            db.session.delete(device)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_user_device_tokens(user_id):
        """
        Get all device tokens for a user.
        
        Args:
            user_id (str or int): User ID (from JWT, may be string)
        
        Returns:
            list: List of device token strings
        """
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        devices = UserDevice.query.filter_by(user_id=user_id).all()
        return [device.device_token for device in devices]
