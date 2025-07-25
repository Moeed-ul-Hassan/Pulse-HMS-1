import streamlit as st
from typing import Dict

class ThemeManager:
    """Theme management for dark/light mode"""
    
    @staticmethod
    def get_theme() -> str:
        """Get current theme"""
        return st.session_state.get('theme', 'dark')
    
    @staticmethod
    def toggle_theme():
        """Toggle between dark and light theme"""
        current = ThemeManager.get_theme()
        st.session_state.theme = 'light' if current == 'dark' else 'dark'
        st.rerun()
    
    @staticmethod
    def get_theme_config() -> Dict:
        """Get minimalist, professional theme configuration"""
        theme = ThemeManager.get_theme()
        if theme == 'dark':
            return {
                'primary_color': '#2563eb',  # blue-600
                'secondary_color': '#64748b',  # slate-500
                'background_color': '#18181b',  # zinc-900
                'surface_color': '#23272f',  # zinc-800
                'text_color': '#f4f4f5',  # zinc-100
                'border_color': '#334155',  # slate-700
                'card_background': '#23272f',
                'gradient_bg': 'background: #18181b;'
            }
        else:
            return {
                'primary_color': '#2563eb',
                'secondary_color': '#64748b',
                'background_color': '#f4f4f5',
                'surface_color': '#ffffff',
                'text_color': '#18181b',
                'border_color': '#e5e7eb',
                'card_background': '#ffffff',
                'gradient_bg': 'background: #f4f4f5;'
            }
    
    @staticmethod
    def apply_theme():
        config = ThemeManager.get_theme_config()
        st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        .stApp {{
            {config['gradient_bg']}
            font-family: 'Poppins', sans-serif;
            color: {config['text_color']};
        }}
        .theme-card {{
            background: {config['card_background']};
            border: 1px solid {config['border_color']};
            border-radius: 12px;
            padding: 18px;
            margin: 10px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }}
        .metric-card {{
            background: {config['surface_color']};
            border: 1px solid {config['border_color']};
            border-radius: 10px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 1px 4px rgba(0,0,0,0.02);
        }}
        .metric-card:hover {{
            transform: none;
            box-shadow: 0 2px 8px rgba(37,99,235,0.08);
        }}
        .alert-card, .success-card {{
            background: {config['surface_color']};
            border: 1px solid {config['border_color']};
            border-radius: 10px;
            padding: 14px;
            margin: 10px 0;
        }}
        .sidebar .sidebar-content {{
            background: {config['surface_color']};
        }}
        .stButton > button {{
            background: {config['primary_color']};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 18px;
            font-weight: 600;
            font-family: 'Poppins', sans-serif;
            box-shadow: 0 1px 4px rgba(37,99,235,0.08);
        }}
        .stButton > button:hover {{
            background: {config['secondary_color']};
        }}
        .theme-toggle {{
            display: none;
        }}
        </style>
        """, unsafe_allow_html=True)