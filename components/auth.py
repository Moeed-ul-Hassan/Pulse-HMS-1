import streamlit as st
import bcrypt
import json
import os
from typing import Dict, Optional
import logging
import time

class AuthManager:
    """Authentication and session management for PulseAI
    Security Layers:
    1. Authentication (hashed passwords)
    2. Authorization (role-based access)
    3. Input validation
    4. Session management (timeout)
    5. Logging (login attempts)
    6. Data encryption (see comments)
    7. Secure deployment (see comments)
    """
    SESSION_TIMEOUT_MINUTES = 30
    
    def __init__(self, users_file: str = "data/users.json"):
        self.users_file = users_file
        self.users = self._load_users()
        self._setup_logger()
        
    def _setup_logger(self):
        self.logger = logging.getLogger("PulseAIAuth")
        if not self.logger.hasHandlers():
            handler = logging.FileHandler("auth.log")
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _load_users(self) -> Dict:
        """Load user data from JSON file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return self._create_default_users()
        else:
            return self._create_default_users()
    
    def _create_default_users(self) -> Dict:
        """Create default admin user"""
        default_users = {
            "admin": {
                "password": bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                "role": "admin",
                "name": "System Administrator",
                "email": "admin@pulseai.com"
            }
        }
        self._save_users(default_users)
        return default_users
    
    def _save_users(self, users: Dict) -> None:
        """Save users to file"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user credentials with input validation and logging"""
        if not username or not password or len(username) > 32 or len(password) > 128:
            self.logger.warning(f"Invalid login input for user: {username}")
            return False
        if username in self.users:
            hashed = self.users[username]["password"].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hashed):
                self.logger.info(f"Login success for user: {username}")
                self._update_session_time()
                return True
            else:
                self.logger.warning(f"Login failed for user: {username}")
        else:
            self.logger.warning(f"Login failed for user: {username}")
        return False
    
    def _update_session_time(self):
        st.session_state['last_active'] = int(time.time())
    
    def is_session_active(self) -> bool:
        last = st.session_state.get('last_active')
        if last is None:
            return False
        return (int(time.time()) - last) < self.SESSION_TIMEOUT_MINUTES * 60
    
    def require_auth(self, role=None):
        """Decorator to require authentication and (optionally) a specific role"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not self.is_authenticated() or not self.is_session_active():
                    st.error("Session expired. Please log in again.")
                    self.logout()
                    return
                if role and self.get_current_user() and self.get_current_user().get('role') != role:
                    st.error("You do not have permission to access this page.")
                    return
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Get user information"""
        return self.users.get(username)
    
    def login_form(self):
        """Display login form with input validation and session timeout"""
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; min-height: 60vh;">
            <div style="background: #fff; border: 1px solid #e5e7eb; border-radius: 20px; padding: 40px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); max-width: 400px; width: 100%;">
                <h2 style="text-align: center; color: #2563eb; margin-bottom: 30px; font-family: 'Poppins', sans-serif;">
                    🔒 PulseAI Login
                </h2>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username", max_chars=32)
            password = st.text_input("Password", type="password", placeholder="Enter password", max_chars=128)
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if self.authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_info = self.get_user_info(username)
                    self._update_session_time()
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials!")
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        st.info("Default login: username=admin, password=admin123")
    
    def logout(self):
        """Logout user"""
        for key in ['authenticated', 'username', 'user_info']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated and session is active"""
        return st.session_state.get('authenticated', False) and self.is_session_active()
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current logged in user"""
        return st.session_state.get('user_info')

# Note: For full data encryption at rest, use encrypted storage or a database with encryption support.
# For secure deployment, always use HTTPS, environment variables for secrets, and restrict access to sensitive files.