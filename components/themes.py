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
        """Get theme configuration"""
        theme = ThemeManager.get_theme()
        
        if theme == 'dark':
            return {
                'primary_color': '#00ff88',
                'secondary_color': '#00ccff',
                'background_color': '#0a0a0a',
                'surface_color': 'rgba(11, 61, 11, 0.15)',
                'text_color': '#ffffff',
                'border_color': 'rgba(0, 255, 136, 0.3)',
                'card_background': 'linear-gradient(135deg, rgba(11, 61, 11, 0.15) 0%, rgba(49, 120, 115, 0.15) 100%)',
                'gradient_bg': '''
                background: 
                    radial-gradient(circle at 20% 20%, rgba(0, 255, 136, 0.1) 0%, transparent 30%),
                    radial-gradient(circle at 80% 80%, rgba(0, 204, 255, 0.1) 0%, transparent 30%),
                    radial-gradient(circle at 40% 60%, rgba(255, 0, 136, 0.1) 0%, transparent 30%),
                    linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
                '''
            }
        else:
            return {
                'primary_color': '#2e7d32',
                'secondary_color': '#1976d2',
                'background_color': '#ffffff',
                'surface_color': 'rgba(46, 125, 50, 0.05)',
                'text_color': '#000000',
                'border_color': 'rgba(46, 125, 50, 0.3)',
                'card_background': 'linear-gradient(135deg, rgba(46, 125, 50, 0.05) 0%, rgba(25, 118, 210, 0.05) 100%)',
                'gradient_bg': '''
                background: 
                    radial-gradient(circle at 20% 20%, rgba(46, 125, 50, 0.1) 0%, transparent 30%),
                    radial-gradient(circle at 80% 80%, rgba(25, 118, 210, 0.1) 0%, transparent 30%),
                    linear-gradient(135deg, #f5f5f5 0%, #e3f2fd 50%, #f1f8e9 100%);
                '''
            }
    
    @staticmethod
    def apply_theme():
        """Apply current theme styles"""
        config = ThemeManager.get_theme_config()
        theme_name = ThemeManager.get_theme()
        
        st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
        
        .stApp {{
            {config['gradient_bg']}
            font-family: 'Orbitron', monospace;
            color: {config['text_color']};
        }}
        
        .theme-card {{
            background: {config['card_background']};
            border: 2px solid {config['border_color']};
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            backdrop-filter: blur(10px);
        }}
        
        .metric-card {{
            background: {config['surface_color']};
            border: 1px solid {config['border_color']};
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 255, 136, 0.2);
        }}
        
        .alert-card {{
            background: linear-gradient(135deg, rgba(255, 68, 68, 0.1) 0%, rgba(255, 0, 136, 0.1) 100%);
            border: 2px solid rgba(255, 68, 68, 0.3);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }}
        
        .success-card {{
            background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(11, 61, 11, 0.1) 100%);
            border: 2px solid {config['primary_color']};
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }}
        
        .sidebar .sidebar-content {{
            background: {config['surface_color']};
        }}
        
        /* Custom button styles */
        .stButton > button {{
            background: linear-gradient(45deg, {config['primary_color']}, {config['secondary_color']});
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 255, 136, 0.3);
        }}
        
        /* Theme toggle button */
        .theme-toggle {{
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 1000;
            background: {config['primary_color']};
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .theme-toggle:hover {{
            transform: scale(1.1);
        }}
        </style>
        """, unsafe_allow_html=True)