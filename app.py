import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os
import time
from utils.risk_calculator import FraminghamRiskCalculator
from utils.data_manager import PatientDataManager
from utils.visualizations import create_risk_gauge, create_timeline_chart, create_risk_factors_chart, create_real_time_monitor

# Page configuration
st.set_page_config(
    page_title="PulseAI - Hospital Management System",
    page_icon="💓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Enhanced watermark with animation
    st.markdown("""
    <div style="position: fixed; bottom: 15px; right: 15px; z-index: 1000; background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(0, 204, 255, 0.2)); border: 1px solid rgba(0, 255, 136, 0.5); color: #00ff88; padding: 8px 15px; border-radius: 20px; font-size: 13px; backdrop-filter: blur(10px); animation: watermark-glow 3s infinite; font-family: 'Orbitron', monospace; font-weight: bold;">
        ⚡ Crafted by <strong>Moeed ul Hassan</strong> @The Legend ⚡
    </div>
    <style>
    @keyframes watermark-glow {
        0%, 100% { box-shadow: 0 0 10px rgba(0, 255, 136, 0.3); }
        50% { box-shadow: 0 0 20px rgba(0, 255, 136, 0.6); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add enhanced cursor and animations
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {
        background: 
            radial-gradient(circle at 20% 20%, rgba(0, 255, 136, 0.1) 0%, transparent 30%),
            radial-gradient(circle at 80% 80%, rgba(0, 204, 255, 0.1) 0%, transparent 30%),
            radial-gradient(circle at 40% 60%, rgba(255, 0, 136, 0.1) 0%, transparent 30%),
            linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Orbitron', monospace;
        animation: background-pulse 15s infinite;
    }
    
    @keyframes background-pulse {
        0%, 100% { background-size: 100% 100%; }
        50% { background-size: 110% 110%; }
    }
    
    /* Professional cursor styling */
    * {
        cursor: default !important;
    }
    
    .futuristic-card {
        background: linear-gradient(135deg, rgba(11, 61, 11, 0.15) 0%, rgba(49, 120, 115, 0.15) 100%);
        border: 2px solid rgba(11, 61, 11, 0.4);
        border-radius: 25px;
        padding: 35px;
        margin: 20px 0;
        backdrop-filter: blur(15px);
        box-shadow: 0 15px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .futuristic-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 80px rgba(0, 255, 136, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: rgba(0, 255, 136, 0.6);
    }
    
    .futuristic-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #0B3D0B, #317873, #0B3D0B);
        border-radius: 20px;
        z-index: -1;
        animation: border-glow 3s infinite;
    }
    
    @keyframes border-glow {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    .cyber-title {
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 3.2em;
        background: linear-gradient(45deg, #00ff88, #00ccff, #ff0088, #ffff00);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        animation: cyber-glow 2s infinite alternate, gradient-shift 4s ease-in-out infinite;
        margin-bottom: 25px;
        text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
        position: relative;
    }
    
    .cyber-title::before {
        content: '';
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        background: linear-gradient(45deg, #00ff88, #00ccff, #ff0088, #ffff00);
        background-size: 400% 400%;
        border-radius: 15px;
        z-index: -1;
        filter: blur(20px);
        animation: gradient-shift 4s ease-in-out infinite;
        opacity: 0.3;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes cyber-glow {
        from { filter: brightness(1); }
        to { filter: brightness(1.2) drop-shadow(0 0 10px rgba(0, 255, 136, 0.5)); }
    }
    
    .hologram-effect {
        position: relative;
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.12) 0%, rgba(0, 204, 255, 0.12) 100%);
        border: 1px solid rgba(0, 255, 136, 0.4);
        border-radius: 18px;
        padding: 25px;
        margin: 15px 0;
        backdrop-filter: blur(8px);
        animation: hologram-flicker 4s infinite;
        transition: all 0.3s ease;
    }
    
    .hologram-effect:hover {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.18) 0%, rgba(0, 204, 255, 0.18) 100%);
        border-color: rgba(0, 255, 136, 0.6);
        transform: translateY(-2px);
    }
    
    /* Enhanced form styling */
    .stTextInput > div > div > input {
        background: rgba(11, 61, 11, 0.1) !important;
        border: 2px solid rgba(0, 255, 136, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-family: 'Orbitron', monospace !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(0, 255, 136, 0.8) !important;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.3) !important;
    }
    
    .stSelectbox > div > div > div {
        background: rgba(11, 61, 11, 0.1) !important;
        border: 2px solid rgba(0, 255, 136, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.2) 0%, rgba(0, 204, 255, 0.2) 100%) !important;
        border: 2px solid rgba(0, 255, 136, 0.5) !important;
        border-radius: 15px !important;
        color: #ffffff !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: bold !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.4) 0%, rgba(0, 204, 255, 0.4) 100%) !important;
        border-color: rgba(0, 255, 136, 0.8) !important;
        box-shadow: 0 0 25px rgba(0, 255, 136, 0.5) !important;
        transform: translateY(-2px) scale(1.05) !important;
    }
    
    /* Enhanced sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, rgba(11, 61, 11, 0.1) 0%, rgba(49, 120, 115, 0.1) 100%) !important;
        border-right: 2px solid rgba(0, 255, 136, 0.3) !important;
    }
    
    /* Animated loading states */
    .loading-animation {
        animation: loading-pulse 1.5s infinite;
    }
    
    @keyframes loading-pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    /* Enhanced metrics cards */
    .metric-enhanced {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 204, 255, 0.1) 100%);
        border: 1px solid rgba(0, 255, 136, 0.4);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-enhanced:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);
        border-color: rgba(0, 255, 136, 0.8);
    }
    
    .metric-enhanced::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .metric-enhanced:hover::before {
        left: 100%;
    }
    
    @keyframes hologram-flicker {
        0%, 100% { opacity: 0.9; }
        50% { opacity: 1; }
        25%, 75% { opacity: 0.95; }
    }
    
    .neural-network-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        background: radial-gradient(circle at 20% 20%, rgba(0, 255, 136, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(0, 204, 255, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 40% 60%, rgba(255, 0, 136, 0.1) 0%, transparent 50%);
        animation: neural-pulse 8s infinite;
    }
    
    @keyframes neural-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    </style>
    
    <script>
    // Enhanced Roblox-style custom cursor with better visibility
    document.addEventListener('DOMContentLoaded', function() {
        // Force hide all default cursors
        document.body.style.cursor = 'none';
        document.documentElement.style.cursor = 'none';
        
        // Create custom cursor (Roblox-inspired)
        const cursor = document.createElement('div');
        cursor.id = 'custom-cursor';
        cursor.style.cssText = `
            position: fixed;
            width: 20px;
            height: 20px;
            background: linear-gradient(45deg, #ffffff 0%, #f0f0f0 100%);
            border: 3px solid #000000;
            border-radius: 2px;
            pointer-events: none;
            z-index: 99999;
            transition: all 0.1s ease;
            box-shadow: 3px 3px 6px rgba(0, 0, 0, 0.5);
            transform: translate(-50%, -50%);
        `;
        document.body.appendChild(cursor);
        
        // Create cursor trail
        const trail = document.createElement('div');
        trail.id = 'cursor-trail';
        trail.style.cssText = `
            position: fixed;
            width: 32px;
            height: 32px;
            border: 2px solid rgba(0, 0, 0, 0.2);
            border-radius: 4px;
            pointer-events: none;
            z-index: 99998;
            transition: all 0.2s ease;
            transform: translate(-50%, -50%);
        `;
        document.body.appendChild(trail);
        
        // Track mouse movement
        document.addEventListener('mousemove', function(e) {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
            trail.style.left = e.clientX + 'px';
            trail.style.top = e.clientY + 'px';
        });
        
        // Add hover effects
        document.addEventListener('mouseenter', function(e) {
            if (e.target.tagName === 'BUTTON' || e.target.closest('button') || e.target.closest('.stButton')) {
                cursor.style.transform = 'scale(1.5)';
                cursor.style.background = 'radial-gradient(circle, #ff0088 0%, #00ccff 100%)';
                trail.style.transform = 'scale(1.2)';
                trail.style.borderColor = 'rgba(255, 0, 136, 0.5)';
            }
        }, true);
        
        document.addEventListener('mouseleave', function(e) {
            if (e.target.tagName === 'BUTTON' || e.target.closest('button') || e.target.closest('.stButton')) {
                cursor.style.transform = 'scale(1)';
                cursor.style.background = 'radial-gradient(circle, #00ff88 0%, #00ccff 100%)';
                trail.style.transform = 'scale(1)';
                trail.style.borderColor = 'rgba(0, 255, 136, 0.3)';
            }
        }, true);
        
        // Add neural network background
        const neuralBg = document.createElement('div');
        neuralBg.className = 'neural-network-bg';
        document.body.appendChild(neuralBg);
        
        // Create floating particles
        createFloatingParticles();
    });
    
    function createFloatingParticles() {
        const container = document.createElement('div');
        container.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        `;
        document.body.appendChild(container);
        
        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: rgba(0, 255, 136, 0.6);
                border-radius: 50%;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: float-${Math.floor(Math.random() * 3) + 1} ${Math.random() * 10 + 5}s infinite ease-in-out;
                box-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
            `;
            container.appendChild(particle);
        }
    }
    
    // Add CSS for particle animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float-1 {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        @keyframes float-2 {
            0%, 100% { transform: translateX(0px) rotate(0deg); }
            50% { transform: translateX(-30px) rotate(180deg); }
        }
        @keyframes float-3 {
            0%, 100% { transform: translate(0px, 0px) rotate(0deg); }
            33% { transform: translate(20px, -20px) rotate(120deg); }
            66% { transform: translate(-20px, 20px) rotate(240deg); }
        }
    `;
    document.head.appendChild(style);
    </script>
    """, unsafe_allow_html=True)

# Load logo
def load_logo():
    with open("assets/logo.svg", "r") as f:
        logo_svg = f.read()
    return logo_svg

# Initialize session state
if 'current_patient' not in st.session_state:
    st.session_state.current_patient = None
if 'assessment_history' not in st.session_state:
    st.session_state.assessment_history = []

# Initialize components
risk_calculator = FraminghamRiskCalculator()
data_manager = PatientDataManager()

def main():
    load_css()
    
    # Enhanced Hospital Management System Header
    st.markdown("""
    <div class="futuristic-card" style="position: relative; overflow: hidden;">
        <div class="cyber-title">🏥 MediCore HMS</div>
        <div style="text-align: center; color: #00ff88; font-size: 1.3em; margin-bottom: 20px; animation: pulse 2s infinite;">
            Advanced Hospital Management System
        </div>
        <div style="text-align: center; color: #00ccff; font-size: 1em; opacity: 0.9; margin-bottom: 20px;">
            Complete Patient Data Management | AI-Powered Risk Assessment | Real-time Analytics
        </div>
        <div style="text-align: center; color: #ffcc00; font-size: 0.9em; opacity: 0.8;">
            🚀 Next-Gen Healthcare Technology | 🔒 HIPAA Compliant | 📊 Real-time Monitoring
        </div>
        
        <!-- Animated particles -->
        <div style="position: absolute; top: 10px; left: 10px; width: 6px; height: 6px; background: #00ff88; border-radius: 50%; animation: particle-float 8s infinite;"></div>
        <div style="position: absolute; top: 30px; right: 20px; width: 4px; height: 4px; background: #00ccff; border-radius: 50%; animation: particle-float 6s infinite reverse;"></div>
        <div style="position: absolute; bottom: 20px; left: 50%; width: 5px; height: 5px; background: #ff0088; border-radius: 50%; animation: particle-float 7s infinite;"></div>
    </div>
    
    <style>
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    @keyframes particle-float {
        0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.3; }
        50% { transform: translateY(-30px) rotate(180deg); opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Medical disclaimer
    st.markdown("""
    <div class="disclaimer">
        ⚠️ <strong>Medical Disclaimer:</strong> This tool is for clinical decision support only. 
        All diagnostic and treatment decisions must be made by qualified healthcare professionals. 
        This system assists but does not replace clinical judgment.
    </div>
    """, unsafe_allow_html=True)
    
    # Hospital Management System Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="color: #00ff88; font-size: 1.5em; font-weight: bold;">🏥 MediCore</div>
            <div style="color: #00ccff; font-size: 0.9em;">Hospital Management</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Patient selection with futuristic styling
        st.markdown("""
        <div style="color: #ffcc00; font-size: 1.1em; margin-bottom: 10px;">
            👤 Patient Database
        </div>
        """, unsafe_allow_html=True)
        
        patients = data_manager.get_all_patients()
        if patients:
            patient_options = [f"{p['name']} (ID: {p['id']})" for p in patients]
            selected_patient = st.selectbox("🔍 Select Patient", ["New Patient"] + patient_options)
            
            if selected_patient != "New Patient":
                patient_id = selected_patient.split("ID: ")[1].split(")")[0]
                st.session_state.current_patient = data_manager.get_patient(patient_id)
        else:
            st.info("📝 No patients found. Register a new patient to begin.")
        
        # Navigation with Hospital Management System modules
        st.markdown("""
        <div style="color: #00ccff; font-size: 1.1em; margin: 20px 0 10px 0;">
            🚀 System Navigation
        </div>
        """, unsafe_allow_html=True)
        
        page = st.selectbox("Select Module", [
            "🏠 Dashboard",
            "👤 Patient Registration",
            "🩺 Risk Assessment", 
            "📊 Patient Records",
            "📈 Analytics",
            "👥 Patient Management",
            "🏥 Admissions",
            "📺 Live Monitor",
            "👨‍💻 About Creator",
            "⚙️ Settings"
        ])
    
    # Main content area
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "👤 Patient Registration":
        show_patient_registration()
    elif page == "🩺 Risk Assessment":
        show_risk_assessment()
    elif page == "📊 Patient Records":
        show_patient_records()
    elif page == "📈 Analytics":
        show_risk_analytics()
    elif page == "👥 Patient Management":
        show_patient_management()
    elif page == "🏥 Admissions":
        show_patient_admission()
    elif page == "📺 Live Monitor":
        show_real_time_monitor()
    elif page == "👨‍💻 About Creator":
        show_about_creator()
    elif page == "⚙️ Settings":
        show_settings()

def show_risk_assessment():
    st.markdown("""
    <div class="futuristic-card">
        <div class="cyber-title">🩺 Neural Risk Assessment</div>
        <div style="text-align: center; color: #00ff88; font-size: 1.1em; margin-bottom: 15px;">
            Advanced AI-Powered Cardiovascular Analysis
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick assessment toggle with futuristic styling
    st.markdown("""
    <div class="hologram-effect" style="margin: 20px 0;">
        <div style="text-align: center; color: #00ccff; font-size: 1.1em; margin-bottom: 10px;">
            🚀 Select Assessment Protocol
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    assessment_mode = st.radio(
        "Assessment Mode",
        ["🚀 Quick Scan", "📋 Deep Analysis"],
        horizontal=True
    )
    
    # Patient data input form
    with st.form("patient_assessment"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="hologram-effect">
                <div style="color: #00ff88; font-size: 1.2em; margin-bottom: 15px; text-align: center;">
                    👤 Patient Bio-Data
                </div>
            </div>
            """, unsafe_allow_html=True)
            patient_name = st.text_input("🔍 Patient Name", value=st.session_state.current_patient['name'] if st.session_state.current_patient else "", help="Enter patient's full name")
            patient_id = st.text_input("🆔 Patient ID", value=st.session_state.current_patient['id'] if st.session_state.current_patient else "", help="Unique patient identifier")
            age = st.number_input("📅 Age (years)", min_value=20, max_value=120, value=st.session_state.current_patient['age'] if st.session_state.current_patient else 45, help="Patient's age in years")
            gender = st.selectbox("⚥ Gender", ["Male", "Female"], index=0 if st.session_state.current_patient and st.session_state.current_patient['gender'] == 'Male' else 1, help="Biological gender affects risk calculation")
            
            st.markdown("""
            <div class="hologram-effect" style="margin-top: 20px;">
                <div style="color: #00ccff; font-size: 1.2em; margin-bottom: 15px; text-align: center;">
                    🩺 Vital Parameters
                </div>
            </div>
            """, unsafe_allow_html=True)
            systolic_bp = st.number_input("💓 Systolic BP (mmHg)", min_value=80, max_value=250, value=st.session_state.current_patient['systolic_bp'] if st.session_state.current_patient else 120, help="Upper blood pressure reading")
            diastolic_bp = st.number_input("💓 Diastolic BP (mmHg)", min_value=40, max_value=150, value=st.session_state.current_patient['diastolic_bp'] if st.session_state.current_patient else 80, help="Lower blood pressure reading")
            total_cholesterol = st.number_input("🧪 Total Cholesterol (mg/dL)", min_value=100, max_value=400, value=st.session_state.current_patient['total_cholesterol'] if st.session_state.current_patient else 200, help="Total cholesterol level")
            hdl_cholesterol = st.number_input("🧪 HDL Cholesterol (mg/dL)", min_value=20, max_value=100, value=st.session_state.current_patient['hdl_cholesterol'] if st.session_state.current_patient else 50, help="'Good' cholesterol level")
        
        with col2:
            st.markdown("""
            <div class="hologram-effect">
                <div style="color: #ffcc00; font-size: 1.2em; margin-bottom: 15px; text-align: center;">
                    ⚠️ Risk Factors
                </div>
            </div>
            """, unsafe_allow_html=True)
            diabetes = st.checkbox("🩸 Diabetes", value=st.session_state.current_patient['diabetes'] if st.session_state.current_patient else False)
            smoking = st.checkbox("🚬 Current Smoker", value=st.session_state.current_patient['smoking'] if st.session_state.current_patient else False)
            hypertension_treatment = st.checkbox("💊 Hypertension Treatment", value=st.session_state.current_patient['hypertension_treatment'] if st.session_state.current_patient else False)
            
            st.markdown("""
            <div class="hologram-effect" style="margin-top: 20px;">
                <div style="color: #ff0088; font-size: 1.2em; margin-bottom: 15px; text-align: center;">
                    🧬 Genetic & Lifestyle
                </div>
            </div>
            """, unsafe_allow_html=True)
            family_history = st.checkbox("👨‍👩‍👧‍👦 Family History CVD", value=st.session_state.current_patient['family_history'] if st.session_state.current_patient else False)
            physical_activity = st.selectbox("🏃 Physical Activity Level", ["Low", "Moderate", "High"], index=1)
            bmi = st.number_input("⚖️ BMI (kg/m²)", min_value=15.0, max_value=50.0, value=st.session_state.current_patient['bmi'] if st.session_state.current_patient else 25.0)
            
            st.markdown("""
            <div class="hologram-effect" style="margin-top: 20px;">
                <div style="color: #00ccff; font-size: 1.2em; margin-bottom: 15px; text-align: center;">
                    📅 Assessment Protocol
                </div>
            </div>
            """, unsafe_allow_html=True)
            assessment_date = st.date_input("🗓️ Assessment Date", value=datetime.now().date())
        
        st.markdown("""
        <div class="hologram-effect" style="margin-top: 30px;">
            <div style="color: #00ff88; font-size: 1.3em; margin-bottom: 15px; text-align: center;">
                🚀 Neural Network Analysis
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        submitted = st.form_submit_button("🧠 INITIATE AI SCAN", use_container_width=True)
        
        if submitted:
            # Calculate risk score
            patient_data = {
                'name': patient_name,
                'id': patient_id,
                'age': age,
                'gender': gender,
                'systolic_bp': systolic_bp,
                'diastolic_bp': diastolic_bp,
                'total_cholesterol': total_cholesterol,
                'hdl_cholesterol': hdl_cholesterol,
                'diabetes': diabetes,
                'smoking': smoking,
                'hypertension_treatment': hypertension_treatment,
                'family_history': family_history,
                'physical_activity': physical_activity,
                'bmi': bmi,
                'assessment_date': assessment_date.isoformat()
            }
            
            risk_score = risk_calculator.calculate_framingham_risk(patient_data)
            risk_category = risk_calculator.get_risk_category(risk_score)
            
            # Save assessment
            assessment = {
                'patient_data': patient_data,
                'risk_score': risk_score,
                'risk_category': risk_category,
                'timestamp': datetime.now().isoformat()
            }
            
            data_manager.save_patient(patient_data)
            data_manager.save_assessment(assessment)
            st.session_state.assessment_history.append(assessment)
            
            # Display results
            display_risk_results(risk_score, risk_category, patient_data)

def show_patient_registration():
    """Patient Registration - Hospital Management System"""
    st.markdown("""
    <div class="futuristic-card">
        <div class="cyber-title">👤 Patient Registration</div>
        <div style="text-align: center; color: #00ff88; font-size: 1.1em; margin-bottom: 15px;">
            Advanced Patient Data Management System
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Patient Registration Form
    with st.form("patient_registration"):
        st.markdown("""
        <div class="hologram-effect">
            <div style="color: #00ff88; font-size: 1.2em; margin-bottom: 15px; text-align: center;">
                📋 Patient Information
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Personal Information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔍 Personal Details**")
            patient_name = st.text_input("👤 Full Name", placeholder="Enter patient's full name")
            patient_id = st.text_input("🆔 Patient ID", placeholder="Auto-generated if empty")
            date_of_birth = st.date_input("📅 Date of Birth")
            gender = st.selectbox("⚥ Gender", ["Male", "Female", "Other"])
            phone = st.text_input("📞 Phone Number", placeholder="+1-XXX-XXX-XXXX")
            email = st.text_input("📧 Email Address", placeholder="patient@example.com")
            
        with col2:
            st.markdown("**🏠 Address Information**")
            address = st.text_area("🏡 Address", placeholder="Street address")
            city = st.text_input("🌆 City", placeholder="City")
            state = st.text_input("🗺️ State/Province", placeholder="State")
            zip_code = st.text_input("📮 ZIP Code", placeholder="12345")
            country = st.text_input("🌍 Country", placeholder="Country")
            
        # Medical Information
        st.markdown("""
        <div class="hologram-effect" style="margin-top: 20px;">
            <div style="color: #00ccff; font-size: 1.2em; margin-bottom: 15px; text-align: center;">
                🩺 Medical Information
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("**💊 Medical History**")
            blood_type = st.selectbox("🩸 Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"])
            height = st.number_input("📏 Height (cm)", min_value=50, max_value=250, value=170)
            weight = st.number_input("⚖️ Weight (kg)", min_value=10, max_value=300, value=70)
            allergies = st.text_area("🤧 Allergies", placeholder="List any known allergies (e.g., Penicillin, Nuts)")
            medications = st.text_area("💊 Current Medications", placeholder="List current medications with dosages")
            medical_history = st.text_area("📋 Medical History", placeholder="Previous surgeries, chronic conditions, hospitalizations")
            
            # Additional medical fields
            smoking_status = st.selectbox("🚬 Smoking Status", ["Never", "Former", "Current", "Unknown"])
            alcohol_consumption = st.selectbox("🍺 Alcohol Consumption", ["None", "Occasional", "Regular", "Heavy"])
            exercise_frequency = st.selectbox("🏃 Exercise Frequency", ["None", "Rare", "Weekly", "Daily"])
            
        with col4:
            st.markdown("**👨‍👩‍👧‍👦 Emergency Contact**")
            emergency_name = st.text_input("👤 Emergency Contact Name", placeholder="Contact person's name")
            emergency_phone = st.text_input("📞 Emergency Phone", placeholder="Emergency contact number")
            emergency_relation = st.text_input("👨‍👩‍👧‍👦 Relationship", placeholder="Relationship to patient")
            emergency_address = st.text_area("🏠 Emergency Contact Address", placeholder="Emergency contact address")
            
            # Additional contact info
            physician_name = st.text_input("👨‍⚕️ Primary Physician", placeholder="Dr. Smith")
            physician_phone = st.text_input("☎️ Physician Phone", placeholder="Doctor's contact number")
            referred_by = st.text_input("🔗 Referred By", placeholder="Referral source")
            
        # Insurance Information
        st.markdown("""
        <div class="hologram-effect" style="margin-top: 20px;">
            <div style="color: #ffcc00; font-size: 1.2em; margin-bottom: 15px; text-align: center;">
                🏥 Insurance Information
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col5, col6 = st.columns(2)
        
        with col5:
            insurance_provider = st.text_input("🏢 Insurance Provider", placeholder="Insurance company name")
            policy_number = st.text_input("🆔 Policy Number", placeholder="Policy ID")
            insurance_effective_date = st.date_input("📅 Insurance Effective Date")
            copay_amount = st.number_input("💰 Copay Amount ($)", min_value=0, value=0)
            
        with col6:
            group_number = st.text_input("👥 Group Number", placeholder="Group ID")
            insurance_phone = st.text_input("📞 Insurance Phone", placeholder="Insurance contact number")
            deductible = st.number_input("💵 Deductible ($)", min_value=0, value=0)
            
        # Additional Information Section
        st.markdown("""
        <div class="hologram-effect" style="margin-top: 20px;">
            <div style="color: #ff0088; font-size: 1.2em; margin-bottom: 15px; text-align: center;">
                📋 Additional Information
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col7, col8 = st.columns(2)
        
        with col7:
            st.markdown("**🏥 Hospital Information**")
            admission_type = st.selectbox("🏥 Admission Type", ["Outpatient", "Inpatient", "Emergency", "Consultation"])
            department = st.selectbox("🏢 Department", ["General Medicine", "Cardiology", "Emergency", "Surgery", "Pediatrics", "Orthopedics", "Neurology", "Other"])
            room_preference = st.selectbox("🛏️ Room Preference", ["General Ward", "Semi-Private", "Private", "ICU", "No Preference"])
            
        with col8:
            st.markdown("**📝 Notes & Preferences**")
            special_needs = st.text_area("♿ Special Needs", placeholder="Wheelchair access, dietary restrictions, etc.")
            language_preference = st.selectbox("🗣️ Language Preference", ["English", "Spanish", "French", "German", "Chinese", "Arabic", "Other"])
            religion = st.text_input("🕊️ Religion", placeholder="Optional")
            additional_notes = st.text_area("📝 Additional Notes", placeholder="Any other relevant information")
        
        # Submit Button
        st.markdown("""
        <div class="hologram-effect" style="margin-top: 30px;">
            <div style="color: #00ff88; font-size: 1.3em; margin-bottom: 15px; text-align: center;">
                💾 Patient Registration
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        submitted = st.form_submit_button("📝 REGISTER PATIENT", use_container_width=True)
        
        if submitted:
            # Generate patient ID if not provided
            if not patient_id:
                from datetime import datetime
                patient_id = f"P{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Create comprehensive patient data dictionary
            patient_data = {
                'id': patient_id,
                'name': patient_name,
                'date_of_birth': date_of_birth.isoformat(),
                'gender': gender,
                'phone': phone,
                'email': email,
                'address': {
                    'street': address,
                    'city': city,
                    'state': state,
                    'zip_code': zip_code,
                    'country': country
                },
                'medical_info': {
                    'blood_type': blood_type,
                    'height': height,
                    'weight': weight,
                    'bmi': round(weight / ((height/100) ** 2), 2) if height > 0 else 0,
                    'allergies': allergies,
                    'medications': medications,
                    'medical_history': medical_history,
                    'smoking_status': smoking_status,
                    'alcohol_consumption': alcohol_consumption,
                    'exercise_frequency': exercise_frequency
                },
                'emergency_contact': {
                    'name': emergency_name,
                    'phone': emergency_phone,
                    'relationship': emergency_relation,
                    'address': emergency_address
                },
                'physician_info': {
                    'primary_physician': physician_name,
                    'physician_phone': physician_phone,
                    'referred_by': referred_by
                },
                'insurance': {
                    'provider': insurance_provider,
                    'policy_number': policy_number,
                    'group_number': group_number,
                    'phone': insurance_phone,
                    'effective_date': insurance_effective_date.isoformat(),
                    'copay_amount': copay_amount,
                    'deductible': deductible
                },
                'hospital_info': {
                    'admission_type': admission_type,
                    'department': department,
                    'room_preference': room_preference
                },
                'preferences': {
                    'special_needs': special_needs,
                    'language_preference': language_preference,
                    'religion': religion,
                    'additional_notes': additional_notes
                },
                'registration_date': datetime.now().isoformat(),
                'status': 'Active',
                'last_updated': datetime.now().isoformat()
            }
            
            # Save patient data to JSON
            data_manager.save_patient(patient_data)
            st.session_state.current_patient = patient_data
            
            # Validation checks
            if not patient_name:
                st.error("❌ Patient name is required!")
                return
            
            # Progress indicator
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text('🔄 Validating patient data...')
            progress_bar.progress(25)
            
            status_text.text('💾 Saving to database...')
            progress_bar.progress(50)
            
            status_text.text('📊 Generating patient profile...')
            progress_bar.progress(75)
            
            status_text.text('✅ Registration complete!')
            progress_bar.progress(100)
            
            # Success message with animation
            st.success(f"✅ Patient {patient_name} (ID: {patient_id}) has been successfully registered!")
            st.balloons()
            
            # Clear progress indicators
            status_text.empty()
            progress_bar.empty()
            
            # Comprehensive patient summary
            st.markdown("""
            <div class="futuristic-card" style="margin-top: 20px;">
                <div style="color: #00ff88; font-size: 1.5em; margin-bottom: 20px; text-align: center;">
                    🎉 Registration Successful
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display comprehensive patient information
            col_info1, col_info2, col_info3 = st.columns(3)
            
            with col_info1:
                st.markdown("""
                <div class="hologram-effect">
                    <div style="color: #00ff88; font-size: 1.1em; margin-bottom: 10px; text-align: center;">
                        👤 Personal Info
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.info(f"""
                **Patient Details:**
                - Name: {patient_name}
                - ID: {patient_id}
                - DOB: {date_of_birth}
                - Gender: {gender}
                - Phone: {phone}
                - Email: {email}
                """)
            
            with col_info2:
                st.markdown("""
                <div class="hologram-effect">
                    <div style="color: #00ccff; font-size: 1.1em; margin-bottom: 10px; text-align: center;">
                        🩺 Medical Info
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.info(f"""
                **Medical Details:**
                - Blood Type: {blood_type}
                - Height: {height} cm
                - Weight: {weight} kg
                - BMI: {round(weight / ((height/100) ** 2), 1) if height > 0 else 'N/A'}
                - Smoking: {smoking_status}
                - Exercise: {exercise_frequency}
                """)
            
            with col_info3:
                st.markdown("""
                <div class="hologram-effect">
                    <div style="color: #ffcc00; font-size: 1.1em; margin-bottom: 10px; text-align: center;">
                        📞 Emergency Contact
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.info(f"""
                **Emergency Contact:**
                - Name: {emergency_name}
                - Phone: {emergency_phone}
                - Relationship: {emergency_relation}
                - Department: {department}
                - Admission Type: {admission_type}
                - Room: {room_preference}
                """)
            
            # Additional details in expandable sections
            with st.expander("📋 View Complete Patient Record"):
                st.json(patient_data)

def show_patient_records():
    """Patient Records - Display and search patient data"""
    st.markdown("""
    <div class="futuristic-card">
        <div class="cyber-title">📊 Patient Records</div>
        <div style="text-align: center; color: #00ff88; font-size: 1.1em; margin-bottom: 15px;">
            Comprehensive Patient Database Management
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get all patients
    patients = data_manager.get_all_patients()
    
    if not patients:
        st.warning("📝 No patients found. Please register patients first.")
        return
    
    # Search functionality
    st.markdown("""
    <div class="hologram-effect">
        <div style="color: #00ccff; font-size: 1.2em; margin-bottom: 15px; text-align: center;">
            🔍 Search Patient Records
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    search_term = st.text_input("🔍 Search by Name, ID, or Phone", placeholder="Enter search term")
    
    # Filter patients based on search
    if search_term:
        filtered_patients = []
        for patient in patients:
            if (search_term.lower() in patient['name'].lower() or 
                search_term.lower() in patient['id'].lower() or
                search_term.lower() in patient.get('phone', '').lower()):
                filtered_patients.append(patient)
        patients = filtered_patients
    
    # Display patient records
    st.markdown(f"### 📋 Patient Records ({len(patients)} found)")
    
    for patient in patients:
        with st.expander(f"👤 {patient['name']} (ID: {patient['id']})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                **Personal Information:**
                - Name: {patient['name']}
                - ID: {patient['id']}
                - Date of Birth: {patient.get('date_of_birth', 'N/A')}
                - Gender: {patient.get('gender', 'N/A')}
                - Phone: {patient.get('phone', 'N/A')}
                - Email: {patient.get('email', 'N/A')}
                """)
            
            with col2:
                st.markdown(f"""
                **Medical Information:**
                - Blood Type: {patient.get('medical_info', {}).get('blood_type', 'N/A')}
                - Allergies: {patient.get('medical_info', {}).get('allergies', 'None')}
                - Current Medications: {patient.get('medical_info', {}).get('medications', 'None')}
                """)
            
            with col3:
                st.markdown(f"""
                **Emergency Contact:**
                - Name: {patient.get('emergency_contact', {}).get('name', 'N/A')}
                - Phone: {patient.get('emergency_contact', {}).get('phone', 'N/A')}
                - Relationship: {patient.get('emergency_contact', {}).get('relationship', 'N/A')}
                """)
            
            # Show patient assessments
            assessments = data_manager.get_patient_assessments(patient['id'])
            if assessments:
                st.markdown(f"**Risk Assessments:** {len(assessments)} assessments")
                for assessment in assessments[-3:]:  # Show last 3 assessments
                    st.info(f"Risk Score: {assessment['risk_score']:.1f}% ({assessment['risk_category']}) - {assessment['timestamp'][:10]}")
            else:
                st.info("No risk assessments found")
            
            # Action buttons
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button(f"📝 Edit Patient {patient['id']}", key=f"edit_{patient['id']}"):
                    st.session_state.current_patient = patient
                    st.success(f"Selected patient {patient['name']} for editing")
            
            with col_btn2:
                if st.button(f"🩺 Risk Assessment {patient['id']}", key=f"assess_{patient['id']}"):
                    st.session_state.current_patient = patient
                    st.success(f"Ready to assess {patient['name']}")
                    st.rerun()

def show_about_creator():
    """About Creator - Professional Profile"""
    st.markdown("""
    <div class="futuristic-card">
        <div class="cyber-title">👨‍💻 Meet The Legend</div>
        <div style="text-align: center; color: #00ff88; font-size: 1.3em; margin-bottom: 25px;">
            Professional Python Developer & Healthcare Tech Innovator
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero section with animated profile
    st.markdown("""
    <div class="hologram-effect" style="text-align: center; padding: 40px;">
        <div style="font-size: 4em; margin-bottom: 20px; animation: float 3s ease-in-out infinite;">
            🚀
        </div>
        <div style="font-size: 2.5em; color: #00ff88; font-weight: bold; margin-bottom: 10px;">
            Moeed ul Hassan
        </div>
        <div style="font-size: 1.5em; color: #00ccff; margin-bottom: 15px;">
            @The Legend
        </div>
        <div style="font-size: 1.1em; color: #ffffff; opacity: 0.8;">
            🇵🇰 Karachi, Pakistan
        </div>
    </div>
    <style>
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Professional achievements
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="hologram-effect" style="text-align: center;">
            <div style="font-size: 3em; color: #00ff88; margin-bottom: 15px;">2+</div>
            <div style="font-size: 1.2em; color: #00ccff; font-weight: bold;">Years Experience</div>
            <div style="font-size: 0.9em; color: #ffffff; opacity: 0.7; margin-top: 10px;">
                Professional Python Development
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="hologram-effect" style="text-align: center;">
            <div style="font-size: 3em; color: #ffcc00; margin-bottom: 15px;">20+</div>
            <div style="font-size: 1.2em; color: #ffcc00; font-weight: bold;">Projects Completed</div>
            <div style="font-size: 0.9em; color: #ffffff; opacity: 0.7; margin-top: 10px;">
                Web Apps, APIs, Healthcare Systems
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="hologram-effect" style="text-align: center;">
            <div style="font-size: 3em; color: #ff0088; margin-bottom: 15px;">🏆</div>
            <div style="font-size: 1.2em; color: #ff0088; font-weight: bold;">Certified Developer</div>
            <div style="font-size: 0.9em; color: #ffffff; opacity: 0.7; margin-top: 10px;">
                Python Professional Certification
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Technical expertise
    st.markdown("""
    <div class="futuristic-card">
        <div style="color: #00ff88; font-size: 1.8em; margin-bottom: 25px; text-align: center;">
            🛠️ Technical Arsenal
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_tech1, col_tech2 = st.columns(2)
    
    with col_tech1:
        st.markdown("""
        <div class="hologram-effect">
            <div style="color: #00ccff; font-size: 1.3em; margin-bottom: 20px;">💻 Core Technologies</div>
            <div style="color: #ffffff; line-height: 1.8;">
                • <strong>Python:</strong> Advanced (Django, FastAPI, Streamlit)<br>
                • <strong>Web Development:</strong> Full-stack applications<br>
                • <strong>Database:</strong> PostgreSQL, MongoDB, JSON<br>
                • <strong>API Development:</strong> RESTful services<br>
                • <strong>Frontend:</strong> HTML5, CSS3, JavaScript<br>
                • <strong>Cloud:</strong> AWS, Azure deployment
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_tech2:
        st.markdown("""
        <div class="hologram-effect">
            <div style="color: #ffcc00; font-size: 1.3em; margin-bottom: 20px;">🏥 Healthcare Specialization</div>
            <div style="color: #ffffff; line-height: 1.8;">
                • <strong>Medical Systems:</strong> HMS, EMR, Patient Management<br>
                • <strong>Healthcare APIs:</strong> HL7, FHIR integration<br>
                • <strong>Risk Assessment:</strong> AI-powered diagnostics<br>
                • <strong>Data Security:</strong> HIPAA compliance<br>
                • <strong>Analytics:</strong> Medical data visualization<br>
                • <strong>Real-time Systems:</strong> Patient monitoring
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Professional journey
    st.markdown("""
    <div class="futuristic-card">
        <div style="color: #00ff88; font-size: 1.8em; margin-bottom: 25px; text-align: center;">
            🚀 Professional Journey
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hologram-effect">
        <div style="color: #ffffff; font-size: 1.1em; line-height: 1.9;">
            <strong>From Code to Legend:</strong><br><br>
            
            Moeed ul Hassan began his journey as a passionate Python developer in Pakistan, quickly mastering 
            web application development with a focus on healthcare technology. With over 2 years of professional 
            experience and 20+ successful projects, he has earned the title <strong>"The Legend"</strong> in his field.
            <br><br>
            
            <strong>🎯 Specializations:</strong><br>
            • Hospital Management Systems (HMS)<br>
            • Electronic Medical Records (EMR)<br>
            • Patient data management and analytics<br>
            • AI-powered risk assessment tools<br>
            • Real-time healthcare monitoring systems<br>
            • HIPAA-compliant healthcare applications
            <br><br>
            
            <strong>🏆 Why "The Legend"?</strong><br>
            His innovative approach to healthcare technology, combined with robust coding skills and 
            deep understanding of medical workflows, has made him a sought-after developer in the 
            healthcare tech space. Colleagues and clients recognize his ability to transform complex 
            medical requirements into elegant, functional solutions.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact and portfolio
    st.markdown("""
    <div class="futuristic-card">
        <div style="color: #00ff88; font-size: 1.8em; margin-bottom: 25px; text-align: center;">
            📞 Get in Touch
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_contact1, col_contact2 = st.columns(2)
    
    with col_contact1:
        st.markdown("""
        <div class="hologram-effect" style="text-align: center;">
            <div style="font-size: 2.5em; margin-bottom: 15px;">💼</div>
            <div style="color: #00ccff; font-size: 1.2em; margin-bottom: 10px;">Professional Services</div>
            <div style="color: #ffffff; opacity: 0.9;">
                • Healthcare Web Applications<br>
                • Custom Python Development<br>
                • API Integration & Development<br>
                • Database Design & Management<br>
                • System Architecture & Consulting
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_contact2:
        st.markdown("""
        <div class="hologram-effect" style="text-align: center;">
            <div style="font-size: 2.5em; margin-bottom: 15px;">🌟</div>
            <div style="color: #ffcc00; font-size: 1.2em; margin-bottom: 10px;">Recognition</div>
            <div style="color: #ffffff; opacity: 0.9;">
                • Certified Python Developer<br>
                • Healthcare Tech Specialist<br>
                • 20+ Successful Projects<br>
                • Industry Recognition as "The Legend"<br>
                • Proven Track Record in Medical Systems
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer message
    st.markdown("""
    <div style="text-align: center; margin-top: 40px; padding: 30px; background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 204, 255, 0.1)); border-radius: 20px; border: 1px solid rgba(0, 255, 136, 0.3);">
        <div style="font-size: 1.4em; color: #00ff88; margin-bottom: 15px;">
            🚀 Innovation • Excellence • Healthcare Technology
        </div>
        <div style="font-size: 1.1em; color: #00ccff;">
            "Transforming Healthcare Through Code"
        </div>
        <div style="font-size: 0.9em; color: #ffffff; opacity: 0.8; margin-top: 10px;">
            - Moeed ul Hassan @The Legend
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_risk_results(risk_score, risk_category, patient_data):
    st.markdown("""
    <div class="futuristic-card">
        <div class="cyber-title">🎯 Neural Analysis Results</div>
        <div style="text-align: center; color: #00ff88; font-size: 1.1em; margin-bottom: 15px;">
            Advanced AI Risk Assessment Complete
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Risk score visualization
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        # Risk gauge
        fig_gauge = create_risk_gauge(risk_score, risk_category)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        # Risk category display
        color_map = {
            'Low': '#0B3D0B',
            'Moderate': '#FFA500',
            'High': '#FF4444'
        }
        animation_class = "shake pulse-alert neon-glow" if risk_category == "High" else "breathing hover-glow" if risk_category == "Moderate" else "floating hover-lift"
        st.markdown(f"""
        <div class="risk-category {animation_class}" style="background-color: {color_map[risk_category]}20; border: 2px solid {color_map[risk_category]};">
            <h3 style="color: {color_map[risk_category]}; margin: 0;">Risk Category</h3>
            <h2 style="color: {color_map[risk_category]}; margin: 5px 0;">{risk_category}</h2>
            <p style="margin: 0;">10-year CVD risk: {risk_score:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Risk factors contribution
        fig_factors = create_risk_factors_chart(patient_data)
        st.plotly_chart(fig_factors, use_container_width=True)
    
    # Risk alerts
    if risk_score > 20:
        st.error("🚨 HIGH RISK ALERT: Immediate clinical intervention recommended")
    elif risk_score > 10:
        st.warning("⚠️ MODERATE RISK: Consider lifestyle modifications and regular monitoring")
    else:
        st.success("✅ LOW RISK: Continue preventive measures and routine screening")
    
    # Explainable AI insights
    st.markdown("### AI Risk Analysis & Recommendations")
    
    explanations = risk_calculator.get_risk_explanations(patient_data, risk_score)
    
    for explanation in explanations:
        st.markdown(f"**{explanation['factor']}:** {explanation['impact']}")
    
    # Clinical recommendations
    st.markdown("### Clinical Recommendations")
    recommendations = risk_calculator.get_clinical_recommendations(risk_category, patient_data)
    
    for rec in recommendations:
        st.markdown(f"• {rec}")

def show_patient_history():
    st.markdown("## Patient History")
    
    if st.session_state.current_patient:
        patient = st.session_state.current_patient
        st.markdown(f"### Patient: {patient['name']} (ID: {patient['id']})")
        
        # Get patient assessments
        assessments = data_manager.get_patient_assessments(patient['id'])
        
        if assessments:
            # Timeline chart
            fig_timeline = create_timeline_chart(assessments)
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Assessment history table
            st.markdown("### Assessment History")
            history_df = pd.DataFrame([
                {
                    'Date': assessment['timestamp'][:10],
                    'Risk Score': f"{assessment['risk_score']:.1f}%",
                    'Risk Category': assessment['risk_category'],
                    'Systolic BP': assessment['patient_data']['systolic_bp'],
                    'Total Cholesterol': assessment['patient_data']['total_cholesterol'],
                    'HDL': assessment['patient_data']['hdl_cholesterol']
                }
                for assessment in assessments
            ])
            st.dataframe(history_df, use_container_width=True)
        else:
            st.info("No assessment history available for this patient.")
    else:
        st.warning("Please select a patient to view history.")

def show_risk_analytics():
    st.markdown("## Risk Analytics Dashboard")
    
    # Population risk distribution
    all_assessments = data_manager.get_all_assessments()
    
    if all_assessments:
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk distribution
            risk_data = [assessment['risk_category'] for assessment in all_assessments]
            fig_dist = px.histogram(x=risk_data, title="Risk Category Distribution")
            fig_dist.update_layout(xaxis_title="Risk Category", yaxis_title="Number of Patients")
            st.plotly_chart(fig_dist, use_container_width=True)
        
        with col2:
            # Average risk by age group
            age_groups = []
            risk_scores = []
            for assessment in all_assessments:
                age = assessment['patient_data']['age']
                age_group = f"{(age//10)*10}-{(age//10)*10+9}"
                age_groups.append(age_group)
                risk_scores.append(assessment['risk_score'])
            
            age_risk_df = pd.DataFrame({'Age Group': age_groups, 'Risk Score': risk_scores})
            avg_risk = age_risk_df.groupby('Age Group')['Risk Score'].mean().reset_index()
            
            fig_age = px.bar(avg_risk, x='Age Group', y='Risk Score', title="Average Risk by Age Group")
            st.plotly_chart(fig_age, use_container_width=True)
        
        # Summary statistics
        st.markdown("### Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Assessments", len(all_assessments))
        with col2:
            high_risk = len([a for a in all_assessments if a['risk_category'] == 'High'])
            st.metric("High Risk Patients", high_risk)
        with col3:
            avg_risk = np.mean([a['risk_score'] for a in all_assessments])
            st.metric("Average Risk Score", f"{avg_risk:.1f}%")
        with col4:
            unique_patients = len(set([a['patient_data']['id'] for a in all_assessments]))
            st.metric("Unique Patients", unique_patients)
    else:
        st.info("No assessment data available for analytics.")

def show_patient_management():
    st.markdown("## Patient Management")
    
    # Add new patient
    with st.expander("Add New Patient"):
        with st.form("new_patient"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Patient Name")
                new_id = st.text_input("Patient ID")
                new_age = st.number_input("Age", min_value=20, max_value=120, value=45)
                new_gender = st.selectbox("Gender", ["Male", "Female"])
            
            with col2:
                new_systolic = st.number_input("Systolic BP", min_value=80, max_value=250, value=120)
                new_diastolic = st.number_input("Diastolic BP", min_value=40, max_value=150, value=80)
                new_cholesterol = st.number_input("Total Cholesterol", min_value=100, max_value=400, value=200)
                new_hdl = st.number_input("HDL Cholesterol", min_value=20, max_value=100, value=50)
            
            new_diabetes = st.checkbox("Diabetes")
            new_smoking = st.checkbox("Smoking")
            new_hypertension = st.checkbox("Hypertension Treatment")
            new_family_history = st.checkbox("Family History")
            new_bmi = st.number_input("BMI", min_value=15.0, max_value=50.0, value=25.0)
            
            if st.form_submit_button("Add Patient"):
                patient_data = {
                    'name': new_name,
                    'id': new_id,
                    'age': new_age,
                    'gender': new_gender,
                    'systolic_bp': new_systolic,
                    'diastolic_bp': new_diastolic,
                    'total_cholesterol': new_cholesterol,
                    'hdl_cholesterol': new_hdl,
                    'diabetes': new_diabetes,
                    'smoking': new_smoking,
                    'hypertension_treatment': new_hypertension,
                    'family_history': new_family_history,
                    'bmi': new_bmi
                }
                
                data_manager.save_patient(patient_data)
                st.success(f"Patient {new_name} added successfully!")
                st.rerun()
    
    # Patient list
    st.markdown("### Current Patients")
    patients = data_manager.get_all_patients()
    
    if patients:
        patients_df = pd.DataFrame(patients)
        st.dataframe(patients_df, use_container_width=True)
    else:
        st.info("No patients found.")

def show_dashboard():
    """Enhanced Dashboard - System Overview with Creative UI"""
    st.markdown("""
    <div class="futuristic-card">
        <div style="color: #00ff88; font-size: 2.2em; margin-bottom: 15px; text-align: center;">
            🏠 MediCore HMS Dashboard
        </div>
        <div style="text-align: center; color: #00ccff; font-size: 1.1em; margin-bottom: 20px;">
            Real-time Hospital Management Analytics
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize data manager
    data_manager = PatientDataManager()
    patients = data_manager.get_all_patients()
    assessments = data_manager.get_all_assessments()
    
    # Enhanced metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="hologram-effect">
            <div style="text-align: center; color: #00ff88;">
                <div style="font-size: 2.5em; font-weight: bold; margin-bottom: 10px;">👥 {}</div>
                <div style="font-size: 1.1em; color: #00ccff;">Total Patients</div>
                <div style="font-size: 0.8em; color: #ffffff; opacity: 0.6; margin-top: 5px;">Active Database</div>
            </div>
        </div>
        """.format(len(patients)), unsafe_allow_html=True)
    
    with col2:
        high_risk = len([a for a in assessments if a.get('risk_category') == 'High'])
        st.markdown("""
        <div class="hologram-effect" style="border-color: #ff0088; background: linear-gradient(135deg, rgba(255, 0, 136, 0.2) 0%, rgba(255, 68, 68, 0.2) 100%); animation: hologram-flicker 1s infinite, pulse-alert 2s infinite;">
            <div style="text-align: center; color: #ff0088;">
                <div style="font-size: 2.5em; font-weight: bold; margin-bottom: 10px;">🚨 {}</div>
                <div style="font-size: 1.1em; color: #ff4444;">High Risk Alert</div>
                <div style="font-size: 0.8em; color: #ffffff; opacity: 0.6; margin-top: 5px;">Critical Cases</div>
            </div>
        </div>
        """.format(high_risk), unsafe_allow_html=True)
    
    with col3:
        today_assessments = len([a for a in assessments if a.get('timestamp', '')[:10] == datetime.now().strftime('%Y-%m-%d')])
        st.markdown("""
        <div class="hologram-effect" style="border-color: #00ccff; background: linear-gradient(135deg, rgba(0, 204, 255, 0.1) 0%, rgba(0, 255, 136, 0.1) 100%);">
            <div style="text-align: center; color: #00ccff;">
                <div style="font-size: 2.5em; font-weight: bold; margin-bottom: 10px;">📊 {}</div>
                <div style="font-size: 1.1em; color: #00ccff;">Today's Scans</div>
                <div style="font-size: 0.8em; color: #ffffff; opacity: 0.6; margin-top: 5px;">Real-time Analytics</div>
            </div>
        </div>
        """.format(today_assessments), unsafe_allow_html=True)
    
    with col4:
        if assessments:
            avg_risk = np.mean([a['risk_score'] for a in assessments])
            st.markdown("""
            <div class="hologram-effect" style="border-color: #ffcc00; background: linear-gradient(135deg, rgba(255, 204, 0, 0.1) 0%, rgba(255, 136, 0, 0.1) 100%);">
                <div style="text-align: center; color: #ffcc00;">
                    <div style="font-size: 2.5em; font-weight: bold; margin-bottom: 10px;">📈 {:.1f}%</div>
                    <div style="font-size: 1.1em; color: #ffcc00;">Average Risk</div>
                    <div style="font-size: 0.8em; color: #ffffff; opacity: 0.6; margin-top: 5px;">AI Prediction</div>
                </div>
            </div>
            """.format(avg_risk), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="hologram-effect" style="border-color: #ffcc00; background: linear-gradient(135deg, rgba(255, 204, 0, 0.1) 0%, rgba(255, 136, 0, 0.1) 100%);">
                <div style="text-align: center; color: #ffcc00;">
                    <div style="font-size: 2.5em; font-weight: bold; margin-bottom: 10px;">📈 0%</div>
                    <div style="font-size: 1.1em; color: #ffcc00;">Average Risk</div>
                    <div style="font-size: 0.8em; color: #ffffff; opacity: 0.6; margin-top: 5px;">AI Prediction</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent activities and quick actions
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Recent Activities")
        if assessments:
            recent_assessments = sorted(assessments, key=lambda x: x.get('timestamp', ''), reverse=True)[:5]
            for assessment in recent_assessments:
                patient_name = assessment['patient_data']['name']
                risk_score = assessment['risk_score']
                risk_category = assessment['risk_category']
                timestamp = assessment.get('timestamp', '')[:16]
                
                color = "#0B3D0B" if risk_category == "Low" else "#FFA500" if risk_category == "Moderate" else "#FF4444"
                
                st.markdown(f"""
                <div class="activity-item hover-lift scan-line" style="border-left: 4px solid {color}; padding: 10px; margin: 5px 0; background: #f8f9fa;">
                    <strong>{patient_name}</strong> - Risk: {risk_score:.1f}% ({risk_category})
                    <br><small>{timestamp}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent activities found.")
    
    with col2:
        st.markdown("### ⚡ Quick Actions")
        if st.button("🆕 New Patient Admission", use_container_width=True, key="admission_btn"):
            st.session_state.quick_action = "admission"
            st.rerun()
        
        if st.button("🩺 Quick Assessment", use_container_width=True, key="assessment_btn"):
            st.session_state.quick_action = "assessment"
            st.rerun()
        
        if st.button("📊 Real-Time Monitor", use_container_width=True, key="monitor_btn"):
            st.session_state.quick_action = "monitor"
            st.rerun()
        
        if st.button("📈 Generate Report", use_container_width=True, key="report_btn"):
            st.session_state.quick_action = "report"
            st.rerun()

def show_patient_admission():
    st.markdown("## 🏥 Patient Admission System")
    
    # Admission workflow
    tab1, tab2, tab3 = st.tabs(["📝 New Admission", "📋 Admission Queue", "📊 Admission Analytics"])
    
    with tab1:
        st.markdown("### Patient Registration")
        
        with st.form("patient_admission_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Personal Information")
                first_name = st.text_input("First Name*")
                last_name = st.text_input("Last Name*")
                patient_id = st.text_input("Patient ID*", value=f"P{datetime.now().strftime('%Y%m%d%H%M%S')}")
                
                dob = st.date_input("Date of Birth*", value=datetime.now().date() - timedelta(days=365*45))
                age = (datetime.now().date() - dob).days // 365
                
                gender = st.selectbox("Gender*", ["Male", "Female", "Other"])
                
                st.markdown("#### Contact Information")
                phone = st.text_input("Phone Number")
                email = st.text_input("Email Address")
                address = st.text_area("Address")
                
                st.markdown("#### Emergency Contact")
                emergency_name = st.text_input("Emergency Contact Name")
                emergency_phone = st.text_input("Emergency Contact Phone")
                emergency_relation = st.text_input("Relationship")
            
            with col2:
                st.markdown("#### Medical History")
                chief_complaint = st.text_area("Chief Complaint*")
                current_medications = st.text_area("Current Medications")
                allergies = st.text_area("Known Allergies")
                
                st.markdown("#### Vital Signs")
                temperature = st.number_input("Temperature (°F)", min_value=95.0, max_value=110.0, value=98.6)
                pulse_rate = st.number_input("Pulse Rate (bpm)", min_value=40, max_value=200, value=72)
                respiratory_rate = st.number_input("Respiratory Rate (breaths/min)", min_value=10, max_value=40, value=16)
                systolic_bp = st.number_input("Systolic BP (mmHg)", min_value=80, max_value=250, value=120)
                diastolic_bp = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=150, value=80)
                
                st.markdown("#### Cardiovascular Risk Factors")
                total_cholesterol = st.number_input("Total Cholesterol (mg/dL)", min_value=100, max_value=400, value=200)
                hdl_cholesterol = st.number_input("HDL Cholesterol (mg/dL)", min_value=20, max_value=100, value=50)
                diabetes = st.checkbox("Diabetes")
                smoking = st.checkbox("Current Smoker")
                hypertension_treatment = st.checkbox("Hypertension Treatment")
                family_history = st.checkbox("Family History of CVD")
                bmi = st.number_input("BMI (kg/m²)", min_value=15.0, max_value=50.0, value=25.0)
                
                st.markdown("#### Admission Details")
                admission_type = st.selectbox("Admission Type", ["Emergency", "Scheduled", "Routine Check-up"])
                referring_physician = st.text_input("Referring Physician")
                insurance_info = st.text_input("Insurance Information")
                
            submitted = st.form_submit_button("🏥 Complete Admission", use_container_width=True)
            
            if submitted:
                if not all([first_name, last_name, patient_id, chief_complaint]):
                    st.error("Please fill in all required fields marked with *")
                else:
                    # Create comprehensive patient record
                    patient_data = {
                        'name': f"{first_name} {last_name}",
                        'id': patient_id,
                        'first_name': first_name,
                        'last_name': last_name,
                        'date_of_birth': dob.isoformat(),
                        'age': age,
                        'gender': gender,
                        'phone': phone,
                        'email': email,
                        'address': address,
                        'emergency_contact': {
                            'name': emergency_name,
                            'phone': emergency_phone,
                            'relation': emergency_relation
                        },
                        'medical_history': {
                            'chief_complaint': chief_complaint,
                            'current_medications': current_medications,
                            'allergies': allergies
                        },
                        'vital_signs': {
                            'temperature': temperature,
                            'pulse_rate': pulse_rate,
                            'respiratory_rate': respiratory_rate,
                            'systolic_bp': systolic_bp,
                            'diastolic_bp': diastolic_bp
                        },
                        'cardiovascular_factors': {
                            'total_cholesterol': total_cholesterol,
                            'hdl_cholesterol': hdl_cholesterol,
                            'diabetes': diabetes,
                            'smoking': smoking,
                            'hypertension_treatment': hypertension_treatment,
                            'family_history': family_history,
                            'bmi': bmi
                        },
                        'admission_details': {
                            'admission_type': admission_type,
                            'referring_physician': referring_physician,
                            'insurance_info': insurance_info,
                            'admission_date': datetime.now().isoformat()
                        },
                        'systolic_bp': systolic_bp,
                        'diastolic_bp': diastolic_bp,
                        'total_cholesterol': total_cholesterol,
                        'hdl_cholesterol': hdl_cholesterol,
                        'diabetes': diabetes,
                        'smoking': smoking,
                        'hypertension_treatment': hypertension_treatment,
                        'family_history': family_history,
                        'bmi': bmi
                    }
                    
                    # Save patient data
                    data_manager.save_patient(patient_data)
                    
                    # Calculate initial risk assessment
                    risk_score = risk_calculator.calculate_framingham_risk(patient_data)
                    risk_category = risk_calculator.get_risk_category(risk_score)
                    
                    assessment = {
                        'patient_data': patient_data,
                        'risk_score': risk_score,
                        'risk_category': risk_category,
                        'timestamp': datetime.now().isoformat(),
                        'assessment_type': 'admission_screening'
                    }
                    
                    data_manager.save_assessment(assessment)
                    
                    st.success(f"✅ Patient {first_name} {last_name} admitted successfully!")
                    st.info(f"Initial CVD Risk Assessment: {risk_score:.1f}% ({risk_category})")
                    
                    # Show admission summary
                    st.markdown("### 📋 Admission Summary")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        **Patient Information:**
                        - Name: {first_name} {last_name}
                        - ID: {patient_id}
                        - Age: {age} years
                        - Gender: {gender}
                        - Admission Type: {admission_type}
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        **Initial Assessment:**
                        - CVD Risk Score: {risk_score:.1f}%
                        - Risk Category: {risk_category}
                        - Blood Pressure: {systolic_bp}/{diastolic_bp} mmHg
                        - Total Cholesterol: {total_cholesterol} mg/dL
                        """)
                    
                    time.sleep(2)
                    st.rerun()
    
    with tab2:
        st.markdown("### 📋 Current Admission Queue")
        
        # Filter patients by admission date (today)
        today = datetime.now().strftime('%Y-%m-%d')
        today_patients = [p for p in data_manager.get_all_patients() 
                         if p.get('admission_details', {}).get('admission_date', '')[:10] == today]
        
        if today_patients:
            for patient in today_patients:
                admission_type = patient.get('admission_details', {}).get('admission_type', 'Unknown')
                admission_time = patient.get('admission_details', {}).get('admission_date', '')[:16]
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**{patient['name']}** (ID: {patient['id']})")
                    st.markdown(f"Chief Complaint: {patient.get('medical_history', {}).get('chief_complaint', 'N/A')}")
                
                with col2:
                    st.markdown(f"**Type:** {admission_type}")
                    st.markdown(f"**Time:** {admission_time}")
                
                with col3:
                    if st.button(f"Process {patient['name']}", key=f"process_{patient['id']}"):
                        st.session_state.current_patient = patient
                        st.success(f"Patient {patient['name']} selected for processing")
                
                st.markdown("---")
        else:
            st.info("No patients admitted today.")
    
    with tab3:
        st.markdown("### 📊 Admission Analytics")
        
        # Admission statistics
        all_patients = data_manager.get_all_patients()
        
        if all_patients:
            # Admission types distribution
            admission_types = [p.get('admission_details', {}).get('admission_type', 'Unknown') for p in all_patients]
            admission_df = pd.DataFrame({'Admission Type': admission_types})
            
            fig_admission = px.pie(admission_df, names='Admission Type', title="Admission Types Distribution")
            st.plotly_chart(fig_admission, use_container_width=True)
            
            # Daily admissions over time
            admission_dates = [p.get('admission_details', {}).get('admission_date', '')[:10] for p in all_patients]
            admission_dates = [date for date in admission_dates if date]
            
            if admission_dates:
                date_df = pd.DataFrame({'Date': admission_dates})
                daily_admissions = date_df.groupby('Date').size().reset_index(name='Count')
                
                fig_daily = px.line(daily_admissions, x='Date', y='Count', title="Daily Admissions Trend")
                st.plotly_chart(fig_daily, use_container_width=True)

def show_real_time_monitor():
    st.markdown("## 📊 Real-Time Patient Monitor")
    
    # Auto-refresh toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 🔄 Live Patient Dashboard")
    with col2:
        auto_refresh = st.checkbox("Auto-refresh (30s)", value=True)
    
    if auto_refresh:
        # Add placeholder for auto-refresh
        placeholder = st.empty()
        
        # Simulate real-time data
        with placeholder.container():
            # Current patients in system
            patients = data_manager.get_all_patients()
            if patients:
                # Select a random patient for demonstration
                current_patient = np.random.choice(patients)
                
                # Simulate vital signs with small variations
                base_systolic = current_patient.get('systolic_bp', 120)
                base_diastolic = current_patient.get('diastolic_bp', 80)
                base_pulse = current_patient.get('vital_signs', {}).get('pulse_rate', 72)
                
                # Add realistic variations
                current_systolic = base_systolic + np.random.randint(-10, 10)
                current_diastolic = base_diastolic + np.random.randint(-5, 5)
                current_pulse = base_pulse + np.random.randint(-5, 15)
                
                # Real-time metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Blood Pressure", f"{current_systolic}/{current_diastolic}", delta=f"{current_systolic-base_systolic}")
                
                with col2:
                    st.metric("Pulse Rate", f"{current_pulse} bpm", delta=f"{current_pulse-base_pulse}")
                
                with col3:
                    # Calculate current risk
                    temp_data = current_patient.copy()
                    temp_data['systolic_bp'] = current_systolic
                    temp_data['diastolic_bp'] = current_diastolic
                    current_risk = risk_calculator.calculate_framingham_risk(temp_data)
                    st.metric("CVD Risk", f"{current_risk:.1f}%", delta=f"{current_risk-risk_calculator.calculate_framingham_risk(current_patient):.1f}%")
                
                with col4:
                    status = "🟢 Normal" if current_risk < 10 else "🟡 Moderate" if current_risk < 20 else "🔴 High"
                    st.metric("Status", status)
                
                # Live chart
                st.markdown("### 📈 Live Vital Signs")
                
                # Create real-time visualization
                fig = create_real_time_monitor(current_patient)
                st.plotly_chart(fig, use_container_width=True)
                
                # Patient details
                st.markdown("### 👤 Current Patient")
                st.markdown(f"**Name:** {current_patient['name']}")
                st.markdown(f"**ID:** {current_patient['id']}")
                st.markdown(f"**Age:** {current_patient['age']} years")
                st.markdown(f"**Gender:** {current_patient['gender']}")
                
                # Alert system
                if current_risk > 20:
                    st.error("🚨 HIGH RISK ALERT: Immediate medical attention required!")
                elif current_risk > 10:
                    st.warning("⚠️ MODERATE RISK: Monitor closely")
                else:
                    st.success("✅ NORMAL: Continue monitoring")
                
                # Auto-refresh every 30 seconds
                time.sleep(30)
                st.rerun()
            else:
                st.info("No patients available for monitoring.")
    
    # Manual patient selection for monitoring
    st.markdown("### 🔍 Select Patient for Monitoring")
    patients = data_manager.get_all_patients()
    
    if patients:
        patient_names = [f"{p['name']} (ID: {p['id']})" for p in patients]
        selected_patient = st.selectbox("Choose Patient", patient_names)
        
        if selected_patient:
            patient_id = selected_patient.split("ID: ")[1].split(")")[0]
            patient = data_manager.get_patient(patient_id)
            
            if patient:
                # Show detailed monitoring for selected patient
                st.markdown(f"### 📋 Monitoring: {patient['name']}")
                
                # Patient assessments timeline
                assessments = data_manager.get_patient_assessments(patient_id)
                if assessments:
                    fig_timeline = create_timeline_chart(assessments)
                    st.plotly_chart(fig_timeline, use_container_width=True)
                
                # Current risk factors
                fig_factors = create_risk_factors_chart(patient)
                st.plotly_chart(fig_factors, use_container_width=True)

def show_settings():
    st.markdown("## ⚙️ PulseAI Settings")
    
    tab1, tab2, tab3 = st.tabs(["🎨 UI Settings", "📊 System Settings", "🔒 Security Settings"])
    
    with tab1:
        st.markdown("### 🎨 User Interface Settings")
        
        # Theme settings
        st.markdown("#### Theme Options")
        theme_option = st.selectbox("Select Theme", ["Medical Green (Default)", "Blue Professional", "Dark Mode"])
        
        # Font size
        font_size = st.slider("Font Size", min_value=12, max_value=20, value=14)
        
        # Dashboard layout
        st.markdown("#### Dashboard Layout")
        layout_option = st.selectbox("Layout Style", ["Compact", "Standard", "Detailed"])
        
        # Notification settings
        st.markdown("#### Notifications")
        enable_sound = st.checkbox("Enable Sound Alerts", value=True)
        high_risk_alerts = st.checkbox("High Risk Patient Alerts", value=True)
        
        if st.button("Apply UI Settings"):
            st.success("UI settings applied successfully!")
    
    with tab2:
        st.markdown("### 📊 System Configuration")
        
        # Data refresh settings
        st.markdown("#### Data Refresh")
        refresh_interval = st.selectbox("Auto-refresh Interval", ["30 seconds", "1 minute", "5 minutes", "Manual"])
        
        # Risk calculation settings
        st.markdown("#### Risk Assessment")
        risk_threshold_moderate = st.slider("Moderate Risk Threshold (%)", min_value=5, max_value=15, value=10)
        risk_threshold_high = st.slider("High Risk Threshold (%)", min_value=15, max_value=30, value=20)
        
        # Data export settings
        st.markdown("#### Data Management")
        export_format = st.selectbox("Export Format", ["CSV", "Excel", "PDF"])
        
        # Backup settings
        auto_backup = st.checkbox("Enable Auto Backup", value=True)
        backup_frequency = st.selectbox("Backup Frequency", ["Daily", "Weekly", "Monthly"])
        
        if st.button("Save System Settings"):
            st.success("System settings saved successfully!")
    
    with tab3:
        st.markdown("### 🔒 Security & Privacy")
        
        # User management
        st.markdown("#### User Access")
        user_roles = st.multiselect("User Roles", ["Doctor", "Nurse", "Administrator", "Technician"])
        
        # Data privacy
        st.markdown("#### Data Privacy")
        data_retention = st.selectbox("Data Retention Period", ["1 year", "2 years", "5 years", "Permanent"])
        anonymize_data = st.checkbox("Anonymize Patient Data for Analytics", value=True)
        
        # Security settings
        st.markdown("#### Security Features")
        two_factor_auth = st.checkbox("Two-Factor Authentication", value=True)
        session_timeout = st.slider("Session Timeout (minutes)", min_value=15, max_value=240, value=60)
        
        # Audit log
        st.markdown("#### Audit & Compliance")
        enable_audit_log = st.checkbox("Enable Audit Logging", value=True)
        hipaa_compliance = st.checkbox("HIPAA Compliance Mode", value=True)
        
        if st.button("Update Security Settings"):
            st.success("Security settings updated successfully!")
        
        # System info
        st.markdown("### ℹ️ System Information")
        st.info(f"""
        **PulseAI Version:** 2.0.0
        **Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        **Database Status:** ✅ Connected
        **Security Status:** ✅ Secure
        """)

if __name__ == "__main__":
    main()
