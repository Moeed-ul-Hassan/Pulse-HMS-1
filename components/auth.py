import streamlit as st
import bcrypt
import json
import os
from typing import Dict, Optional

class AuthManager:
    """Authentication and session management for PulseAI"""
    
    def __init__(self, users_file: str = "data/users.json"):
        self.users_file = users_file
        self.users = self._load_users()
        
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
        """Authenticate user credentials"""
        if username in self.users:
            hashed = self.users[username]["password"].encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), hashed)
        return False
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Get user information"""
        return self.users.get(username)
    
    def login_form(self):
        """Display login form"""
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; min-height: 60vh;">
            <div style="background: linear-gradient(135deg, rgba(11, 61, 11, 0.2) 0%, rgba(49, 120, 115, 0.2) 100%); 
                        border: 2px solid rgba(0, 255, 136, 0.3); border-radius: 20px; padding: 40px; 
                        backdrop-filter: blur(10px); max-width: 400px; width: 100%;">
                <h2 style="text-align: center; color: #00ff88; margin-bottom: 30px; font-family: 'Orbitron', monospace;">
                    🔐 PulseAI Login
                </h2>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if self.authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_info = self.get_user_info(username)
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
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current logged in user"""
        return st.session_state.get('user_info')