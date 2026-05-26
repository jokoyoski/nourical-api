import os
import firebase_admin
from firebase_admin import credentials, messaging

_initialized = False

def _init_firebase():
    global _initialized
    if not _initialized:
        cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        _initialized = True

def send_push_notification(device_token, title, body, data=None):
    """
    Send a push notification to a specific device token.
    
    Args:
        device_token (str): FCM device token
        title (str): Notification title
        body (str): Notification body
        data (dict, optional): Additional data payload
    
    Returns:
        str: Message ID if successful, None otherwise
    """
    _init_firebase()
    
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=device_token,
        data=data
    )
    
    try:
        response = messaging.send(message)
        return response
    except Exception as e:
        print(f"Error sending push notification: {e}")
        return None

def send_multicast_notification(device_tokens, title, body, data=None):
    """
    Send a push notification to multiple device tokens.
    
    Args:
        device_tokens (list): List of FCM device tokens
        title (str): Notification title
        body (str): Notification body
        data (dict, optional): Additional data payload
    
    Returns:
        dict: Response with success count and failure count
    """
    _init_firebase()
    
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        tokens=device_tokens,
        data=data
    )
    
    try:
        response = messaging.send_multicast(message)
        return {
            'success_count': response.success_count,
            'failure_count': response.failure_count
        }
    except Exception as e:
        print(f"Error sending multicast notification: {e}")
        return {
            'success_count': 0,
            'failure_count': len(device_tokens)
        }
