from repositories import UserRepository, OTPRepository
from utils import generate_jwt_token
import random
import os
import resend
from flask import render_template
import base64

class AuthService:
    def __init__(self):
        resend.api_key = os.environ.get('RESEND_API_KEY')
    
    def generate_otp(self):
        return str(random.randint(100000, 999999))
    
    def send_otp_email(self, email, otp):
        try:
            logo_url = "https://res.cloudinary.com/jokoyoski/image/upload/v1778957769/kanga_ej79hv.png"
            html_content = render_template('email/otp_verification.html', otp=otp, email=email, logo_url=logo_url)
            
            params = {
                "from": "Nourical <info@nourical.com>",
                "to": [email],
                "subject": "Verify Your Email - Nourical",
                "html": html_content
            }
            resend.Emails.send(params)
            print(f"[EMAIL SERVICE] OTP {otp} sent to {email}")
            return True
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send email: {e}")
            print(f"[FALLBACK] OTP for {email}: {otp}")
            return True
    
    def register_user(self, full_name, email, password):
        user = UserRepository.get_user_by_email(email)
        if user:
            return None, "User already exists"
        
        user = UserRepository.create_user(full_name, email, password)
        otp_code = self.generate_otp()
        OTPRepository.create_otp(user.id, otp_code)
        self.send_otp_email(email, otp_code)
        
        return user, otp_code
    
    def verify_otp(self, email, otp_code):
        user = UserRepository.get_user_by_email(email)
        if not user:
            return None, "User not found"
        
        otp = OTPRepository.get_valid_otp(user.id, str(otp_code))
        if not otp or not otp.is_valid():
            return None, "Invalid or expired OTP"
        
        OTPRepository.mark_otp_used(otp)
        user = UserRepository.verify_user(user)
        
        return user, None
    
    def login_user(self, email, password):
        user = UserRepository.get_user_by_email(email)
        if not user or not user.check_password(password):
            return None, None, "Invalid email or password"

        if not user.is_verified:
            return None, None, "Please verify your account with OTP before logging in"
        
        token = generate_jwt_token(user.id)
        return user, token, None
    
    def forgot_password(self, email):
        user = UserRepository.get_user_by_email(email)
        if not user:
            return None, "User not found"
        
        otp_code = self.generate_otp()
        OTPRepository.create_otp(user.id, otp_code)
        self.send_otp_email(email, otp_code)
        
        return user, otp_code
    
    def verify_reset_otp(self, email, otp_code):
        user = UserRepository.get_user_by_email(email)
        if not user:
            return None, "User not found"
        
        otp = OTPRepository.get_valid_otp(user.id, str(otp_code))
        if not otp or not otp.is_valid():
            return None, "Invalid or expired OTP"
        
        OTPRepository.mark_otp_used(otp)
        
        import secrets
        reset_token = secrets.token_urlsafe(32)
        
        return reset_token, None
    
    def reset_password(self, email, new_password):
        user = UserRepository.get_user_by_email(email)
        if not user:
            return None, "User not found"
        
        UserRepository.update_password(user, new_password)
        return user, None
    
    def resend_otp(self, email):
        """Resend OTP for registration or password reset"""
        user = UserRepository.get_user_by_email(email)
        if not user:
            return None, "User not found"
        
        otp_code = self.generate_otp()
        OTPRepository.create_otp(user.id, otp_code)
        self.send_otp_email(email, otp_code)
        
        return user, otp_code
