import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'postgresql://nourical_user:nourical_password@localhost:5432/nourical_db'
    RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
    FIREBASE_CREDENTIALS_PATH = os.environ.get('FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json')
    ENV = os.environ.get('ENV', 'local')
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
