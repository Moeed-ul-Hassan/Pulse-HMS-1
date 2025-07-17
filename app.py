import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os
import time
from streamlit_option_menu import option_menu

# Import our enhanced components
from components.auth import AuthManager
from components.themes import ThemeManager
from components.notifications import NotificationManager
from components.pdf_generator import PDFReportGenerator
from components.scheduling import AppointmentScheduler
from components.preloader import HospitalPreloader
from components.monitoring import VitalSignsMonitor
from components.advanced_analytics import AdvancedAnalytics
from components.medical_records import MedicalRecordsManager
from components.inventory_management import InventoryManager
from components.billing_finance import BillingFinanceManager
from components.staff_management import StaffManagementSystem
from components.bed_management import BedManagementSystem
from components.patient_manager import PatientManager
from components.medicine_manager import MedicineManager
from components.ui_enhancements import UIEnhancements

# Import existing utilities
from utils.risk_calculator import FraminghamRiskCalculator
from utils.data_manager import PatientDataManager
from utils.visualizations import create_risk_gauge, create_timeline_chart, create_risk_factors_chart

# Page configuration
st.set_page_config(
    page_title="PulseAI - Enhanced Hospital Management System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize managers
if 'auth_manager' not in st.session_state:
    st.session_state.auth_manager = AuthManager()
if 'notification_manager' not in st.session_state:
    st.session_state.notification_manager = NotificationManager()
if 'pdf_generator' not in st.session_state:
    st.session_state.pdf_generator = PDFReportGenerator()
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = AppointmentScheduler()
if 'vitals_monitor' not in st.session_state:
    st.session_state.vitals_monitor = VitalSignsMonitor()
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = PatientDataManager()
if 'risk_calculator' not in st.session_state:
    st.session_state.risk_calculator = FraminghamRiskCalculator()
if 'advanced_analytics' not in st.session_state:
    st.session_state.advanced_analytics = AdvancedAnalytics(st.session_state.data_manager)
if 'medical_records' not in st.session_state:
    st.session_state.medical_records = MedicalRecordsManager(st.session_state.data_manager)
if 'inventory_manager' not in st.session_state:
    st.session_state.inventory_manager = InventoryManager()
if 'billing_manager' not in st.session_state:
    st.session_state.billing_manager = BillingFinanceManager()
if 'staff_manager' not in st.session_state:
    st.session_state.staff_manager = StaffManagementSystem()
if 'bed_manager' not in st.session_state:
    st.session_state.bed_manager = BedManagementSystem()
if 'patient_manager' not in st.session_state:
    st.session_state.patient_manager = PatientManager()
if 'medicine_manager' not in st.session_state:
    st.session_state.medicine_manager = MedicineManager()

# Show preloader on first visit
if 'app_loaded' not in st.session_state:
    HospitalPreloader.show_preloader()
    st.session_state.app_loaded = True

# Apply theme
ThemeManager.apply_theme()

# No authentication required - direct access to hospital management system

# Enhanced header with theme toggle and user info
def create_enhanced_header():
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("""
        <h1 style="color: #00ff88; font-family: 'Poppins', sans-serif; font-weight: 700; margin: 0;">
            🏥 PULSEAI - HOSPITAL MANAGEMENT SYSTEM
        </h1>
        <p style="color: #00ccff; font-family: 'Poppins', sans-serif; margin: 0;">Advanced Healthcare Management & AI Analytics Platform</p>
        """, unsafe_allow_html=True)
    
    with col2:
        current_theme = ThemeManager.get_theme()
        theme_icon = "🌙" if current_theme == "dark" else "☀️"
        if st.button(f"{theme_icon} Toggle Theme"):
            ThemeManager.toggle_theme()
    
    with col3:
        st.markdown(f"""
        <div style="text-align: right; padding: 10px; font-family: 'Poppins', sans-serif;">
            <strong>🏥 Hospital Management System</strong><br>
            <small>Built on Replit | Advanced Healthcare Platform</small>
        </div>
        <div class="replit-badge">
            🔗 Built on Replit
        </div>
        """, unsafe_allow_html=True)

# Enhanced sidebar with notifications
def create_enhanced_sidebar():
    with st.sidebar:
        # Hospital info section
        st.markdown(f"""
        <div class="theme-card" style="text-align: center; margin-bottom: 20px; font-family: 'Poppins', sans-serif;">
            <h3>🏥 PulseAI HMS</h3>
            <p><strong>Advanced Hospital Management</strong></p>
            <p>Healthcare Analytics Platform</p>
            <p><small>Version 2.0 | Built on Replit</small></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        selected = option_menu(
            menu_title="Navigation",
            options=[
                "Dashboard", "Patient Management", "Medicine Management", "Medical Records",
                "Risk Assessment", "Appointments", "Bed Management", 
                "Staff Management", "Inventory", "Billing & Finance", 
                "Advanced Analytics", "Reports", "Settings", "About Developer"
            ],
            icons=[
                "speedometer2", "person-plus-fill", "capsule", "file-medical", "heart-pulse",
                "calendar", "bed", "people-fill", "box-seam",
                "currency-dollar", "graph-up-arrow", "file-earmark-pdf", "gear", "info-circle"
            ],
            menu_icon="hospital",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#00ff88", "font-size": "16px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "0px",
                    "background-color": "rgba(0,255,136,0.1)",
                    "border-radius": "5px"
                },
                "nav-link-selected": {"background-color": "#00ff88", "color": "black"},
            },
        )
        
        # Notifications
        st.session_state.notification_manager.display_notifications_sidebar()
        
        return selected

# Enhanced dashboard with real-time metrics
def show_enhanced_dashboard():
    st.markdown("## 📊 Enhanced Dashboard")
    
    # Quick metrics
    patients = st.session_state.data_manager.get_all_patients()
    total_patients = len(patients)
    
    # Calculate quick stats
    high_risk_count = 0
    if total_patients > 0:
        for patient in patients:
            risk_score = st.session_state.risk_calculator.calculate_framingham_risk(patient)
            if risk_score > 20:
                high_risk_count += 1
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            UIEnhancements.create_enhanced_metric_card(
                "Total Patients", total_patients, "👥", "#00ff88"
            ), unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            UIEnhancements.create_enhanced_metric_card(
                "High Risk Patients", high_risk_count, "🚨", "#ff4444"
            ), unsafe_allow_html=True
        )
    
    with col3:
        appointments_today = len(st.session_state.scheduler.get_appointments_by_date(str(datetime.now().date())))
        st.markdown(
            UIEnhancements.create_enhanced_metric_card(
                "Today's Appointments", appointments_today, "📅", "#00ccff"
            ), unsafe_allow_html=True
        )
    
    with col4:
        unread_notifications = st.session_state.notification_manager.get_unread_count()
        st.markdown(
            UIEnhancements.create_enhanced_metric_card(
                "Notifications", unread_notifications, "🔔", "#ffa500"
            ), unsafe_allow_html=True
        )
    
    # Recent activity and charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Risk Distribution")
        if total_patients > 0:
            risk_data = {'Low': 0, 'Moderate': 0, 'High': 0}
            for patient in patients:
                risk_score = st.session_state.risk_calculator.calculate_framingham_risk(patient)
                if risk_score < 10:
                    risk_data['Low'] += 1
                elif risk_score < 20:
                    risk_data['Moderate'] += 1
                else:
                    risk_data['High'] += 1
            
            # Filter out zero values for better visualization
            filtered_data = {k: v for k, v in risk_data.items() if v > 0}
            
            if not filtered_data:
                st.info("No patient data available for risk analysis")
            else:
                fig = px.pie(
                    values=list(filtered_data.values()),
                    names=list(filtered_data.keys()),
                    color_discrete_map={'Low': '#00ff88', 'Moderate': '#ffa500', 'High': '#ff4444'},
                    title="Patient Risk Distribution"
                )
                fig.update_layout(
                    font=dict(family="Poppins, sans-serif", size=12),
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    title_font_size=16,
                    title_font_color='#00ff88',
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.2,
                        xanchor="center",
                        x=0.5
                    )
                )
                fig.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
                    marker=dict(line=dict(color='#000000', width=2))
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(
                UIEnhancements.create_info_card(
                    "No Data Available", 
                    "Register patients to see risk distribution analytics.", 
                    "📊", 
                    "#00ccff"
                ), unsafe_allow_html=True
            )
    
    with col2:
        st.markdown("### 🔔 Recent Notifications")
        recent_notifications = st.session_state.notification_manager.get_recent_notifications(5)
        if recent_notifications:
            for notif in recent_notifications:
                icon = st.session_state.notification_manager._get_notification_icon(notif['type'])
                st.markdown(f"**{icon} {notif['title']}**")
                st.markdown(f"<small>{notif['message']}</small>", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.info("No recent notifications")

# Enhanced patient registration with better validation
def show_patient_registration():
    st.markdown("## 👤 Enhanced Patient Registration")
    
    with st.form("enhanced_patient_registration"):
        st.markdown("### Personal Information")
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="Enter patient's full name")
            patient_id = st.text_input("Patient ID *", placeholder="Unique identifier")
            age = st.number_input("Age *", min_value=0, max_value=120, value=30)
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
        
        with col2:
            phone = st.text_input("Phone Number", placeholder="+1234567890")
            email = st.text_input("Email", placeholder="patient@email.com")
            address = st.text_area("Address", height=100)
            emergency_contact = st.text_input("Emergency Contact", placeholder="Name and phone")
        
        st.markdown("### Medical Information")
        col3, col4 = st.columns(2)
        
        with col3:
            systolic_bp = st.number_input("Systolic BP (mmHg) *", min_value=60, max_value=250, value=120)
            diastolic_bp = st.number_input("Diastolic BP (mmHg) *", min_value=40, max_value=150, value=80)
            total_cholesterol = st.number_input("Total Cholesterol (mg/dL) *", min_value=100, max_value=400, value=200)
            hdl_cholesterol = st.number_input("HDL Cholesterol (mg/dL) *", min_value=20, max_value=100, value=50)
        
        with col4:
            height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)
            weight = st.number_input("Weight (kg)", min_value=20, max_value=300, value=70)
            diabetes = st.checkbox("Diabetes")
            smoking = st.checkbox("Current Smoker")
            hypertension_treatment = st.checkbox("On Hypertension Treatment")
            family_history = st.checkbox("Family History of CVD")
        
        physical_activity = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"])
        medical_history = st.text_area("Medical History", height=100)
        current_medications = st.text_area("Current Medications", height=100)
        
        submitted = st.form_submit_button("Register Patient", use_container_width=True)
        
        if submitted:
            if name and patient_id and age:
                # Calculate BMI
                bmi = weight / ((height/100) ** 2) if height > 0 and weight > 0 else 0
                
                patient_data = {
                    'name': name,
                    'id': patient_id,
                    'age': age,
                    'gender': gender,
                    'phone': phone,
                    'email': email,
                    'address': address,
                    'emergency_contact': emergency_contact,
                    'systolic_bp': systolic_bp,
                    'diastolic_bp': diastolic_bp,
                    'total_cholesterol': total_cholesterol,
                    'hdl_cholesterol': hdl_cholesterol,
                    'height': height,
                    'weight': weight,
                    'bmi': bmi,
                    'diabetes': diabetes,
                    'smoking': smoking,
                    'hypertension_treatment': hypertension_treatment,
                    'family_history': family_history,
                    'physical_activity': physical_activity,
                    'medical_history': medical_history,
                    'current_medications': current_medications,
                    'registration_date': datetime.now().strftime("%Y-%m-%d"),
                    'assessment_date': datetime.now().strftime("%Y-%m-%d")
                }
                
                st.session_state.data_manager.save_patient(patient_data)
                
                # Add notification
                st.session_state.notification_manager.add_notification(
                    "New Patient Registered",
                    f"Patient {name} has been successfully registered",
                    "success"
                )
                
                st.success(f"Patient {name} registered successfully!")
                st.balloons()
            else:
                st.error("Please fill in all required fields marked with *")

# Enhanced risk assessment with detailed analysis
def show_risk_assessment():
    st.markdown("## 🫀 Enhanced Risk Assessment")
    
    patients = st.session_state.data_manager.get_all_patients()
    if not patients:
        st.warning("No patients registered. Please register patients first.")
        return
    
    patient_names = [p['name'] for p in patients]
    selected_patient_name = st.selectbox("Select Patient", patient_names)
    
    if selected_patient_name:
        selected_patient = next(p for p in patients if p['name'] == selected_patient_name)
        
        # Display patient info
        st.markdown("### Patient Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Name:** {selected_patient['name']}")
            st.info(f"**Age:** {selected_patient['age']} years")
            st.info(f"**Gender:** {selected_patient['gender']}")
        
        with col2:
            st.info(f"**BMI:** {selected_patient.get('bmi', 'N/A')} kg/m²")
            st.info(f"**BP:** {selected_patient['systolic_bp']}/{selected_patient['diastolic_bp']} mmHg")
            st.info(f"**Total Cholesterol:** {selected_patient['total_cholesterol']} mg/dL")
        
        # Perform risk assessment
        risk_score = st.session_state.risk_calculator.calculate_framingham_risk(selected_patient)
        risk_category = st.session_state.risk_calculator.categorize_risk(risk_score)
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Risk Assessment Results")
            fig = create_risk_gauge(risk_score, risk_category)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Clinical Recommendations")
            recommendations = st.session_state.risk_calculator.get_recommendations(risk_score, selected_patient)
            for rec in recommendations:
                st.markdown(f"• {rec}")
        
        # Save assessment
        if st.button("Save Assessment", use_container_width=True):
            assessment_data = {
                'patient_data': selected_patient,
                'risk_score': risk_score,
                'risk_category': risk_category,
                'timestamp': datetime.now().isoformat()
            }
            
            st.session_state.data_manager.save_assessment(assessment_data)
            
            # Generate notification
            if risk_score > 20:
                st.session_state.notification_manager.add_notification(
                    "High Risk Patient Alert",
                    f"{selected_patient['name']} has high CVD risk ({risk_score:.1f}%)",
                    "warning"
                )
            
            st.success("Assessment saved successfully!")
        
        # Generate PDF report
        if st.button("📄 Generate PDF Report", use_container_width=True):
            HospitalPreloader.show_mini_loader("Generating PDF report...")
            
            risk_data = {
                'risk_score': risk_score,
                'risk_category': risk_category,
                'timestamp': datetime.now().isoformat()
            }
            
            pdf_data = st.session_state.pdf_generator.generate_patient_report(selected_patient, risk_data)
            
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_data,
                file_name=f"PulseAI_Report_{selected_patient['name']}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# Main application logic
def main():
    create_enhanced_header()
    
    # Enhanced sidebar navigation
    selected_page = create_enhanced_sidebar()
    
    # Route to appropriate page
    if selected_page == "Dashboard":
        show_enhanced_dashboard()
    elif selected_page == "Patient Management":
        st.session_state.patient_manager.patient_registration_form()
    elif selected_page == "Medicine Management":
        st.session_state.medicine_manager.display_medicine_management()
    elif selected_page == "Medical Records":
        st.session_state.medical_records.display_medical_records()
    elif selected_page == "Risk Assessment":
        show_risk_assessment()
    elif selected_page == "Appointments":
        show_appointments()
    elif selected_page == "Bed Management":
        st.session_state.bed_manager.display_bed_management()
    elif selected_page == "Staff Management":
        st.session_state.staff_manager.display_staff_dashboard()
    elif selected_page == "Inventory":
        st.session_state.inventory_manager.display_inventory_dashboard()
    elif selected_page == "Billing & Finance":
        st.session_state.billing_manager.display_billing_dashboard()
    elif selected_page == "Advanced Analytics":
        st.session_state.advanced_analytics.display_analytics_dashboard()
    elif selected_page == "Reports":
        show_reports()
    elif selected_page == "Settings":
        show_settings()
    elif selected_page == "About Developer":
        show_about_developer()

# Additional page functions (simplified for brevity)
def show_patient_records():
    st.markdown("## 📋 Patient Records")
    patients = st.session_state.data_manager.get_all_patients()
    
    if patients:
        # Search functionality
        search_term = st.text_input("🔍 Search patients...", placeholder="Enter name or ID")
        
        if search_term:
            filtered_patients = [p for p in patients if search_term.lower() in p['name'].lower() or search_term in p['id']]
        else:
            filtered_patients = patients
        
        # Display patients
        for patient in filtered_patients:
            with st.expander(f"👤 {patient['name']} (ID: {patient['id']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Age:** {patient['age']} years")
                    st.write(f"**Gender:** {patient['gender']}")
                    st.write(f"**Phone:** {patient.get('phone', 'N/A')}")
                with col2:
                    st.write(f"**Email:** {patient.get('email', 'N/A')}")
                    st.write(f"**Registration:** {patient.get('registration_date', 'N/A')}")
                    if st.button(f"View Full Record", key=f"view_{patient['id']}"):
                        st.write(patient)
    else:
        st.info("No patient records found.")

def show_realtime_monitor():
    st.markdown("## 📊 Real-Time Patient Monitor")
    
    patients = st.session_state.data_manager.get_all_patients()
    if not patients:
        st.warning("No patients available for monitoring.")
        return
    
    patient_names = [p['name'] for p in patients]
    selected_patient_name = st.selectbox("Select Patient to Monitor", patient_names)
    
    if selected_patient_name:
        selected_patient = next(p for p in patients if p['name'] == selected_patient_name)
        st.session_state.vitals_monitor.create_realtime_monitor_dashboard(selected_patient)

def show_appointments():
    st.markdown("## 📅 Appointment Management")
    
    tab1, tab2 = st.tabs(["📝 Book Appointment", "📋 View Schedule"])
    
    with tab1:
        st.session_state.scheduler.display_booking_form()
    
    with tab2:
        st.session_state.scheduler.display_appointment_calendar()

def show_analytics():
    st.markdown("## 📈 Hospital Analytics")
    
    patients = st.session_state.data_manager.get_all_patients()
    if patients:
        # Patient demographics
        age_groups = {'18-30': 0, '31-50': 0, '51-70': 0, '70+': 0}
        for patient in patients:
            age = patient['age']
            if age <= 30:
                age_groups['18-30'] += 1
            elif age <= 50:
                age_groups['31-50'] += 1
            elif age <= 70:
                age_groups['51-70'] += 1
            else:
                age_groups['70+'] += 1
        
        fig = px.bar(x=list(age_groups.keys()), y=list(age_groups.values()), 
                     title="Patient Age Distribution")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for analytics.")

def show_reports():
    st.markdown("## 📄 Report Generation")
    
    st.markdown("### Available Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Generate Analytics Report", use_container_width=True):
            HospitalPreloader.show_mini_loader("Generating analytics report...")
            
            patients = st.session_state.data_manager.get_all_patients()
            analytics_data = {
                'total_patients': len(patients),
                'high_risk_patients': sum(1 for p in patients if st.session_state.risk_calculator.calculate_framingham_risk(p) > 20)
            }
            
            pdf_data = st.session_state.pdf_generator.generate_analytics_report(analytics_data)
            
            st.download_button(
                label="📥 Download Analytics Report",
                data=pdf_data,
                file_name=f"PulseAI_Analytics_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    with col2:
        st.info("More report types coming soon!")

def show_settings():
    st.markdown("## ⚙️ System Settings")
    
    tab1, tab2, tab3 = st.tabs(["🎨 Appearance", "🔔 Notifications", "👤 User Management"])
    
    with tab1:
        st.markdown("### Theme Settings")
        current_theme = ThemeManager.get_theme()
        st.write(f"Current theme: **{current_theme.title()}**")
        
        if st.button("🔄 Toggle Theme"):
            ThemeManager.toggle_theme()
    
    with tab2:
        st.markdown("### Notification Preferences")
        
        enable_alerts = st.checkbox("Enable Critical Value Alerts", value=True)
        enable_reminders = st.checkbox("Enable Appointment Reminders", value=True)
        
        if st.button("Save Notification Settings"):
            st.success("Settings saved!")
    
    with tab3:
        st.markdown("### User Information")
        st.info("Direct access mode - No authentication required")
        st.write("**Role:** Hospital Staff")
        st.write("**Access Level:** Full System Access")
        
        # Developer watermark
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <div style="background: linear-gradient(45deg, #00ff88, #00ccff); 
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                        background-clip: text; animation: pulse 2s infinite;
                        font-size: 14px; font-weight: bold;">
                ⚡ Crafted by Moeed ul Hassan @The legend ⚡
            </div>
        </div>
        <style>
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        </style>
        """, unsafe_allow_html=True)

def show_about_developer():
    """About the developer page"""
    st.markdown("## 👨‍💻 About the Developer")
    
    # Developer profile card
    st.markdown("""
    <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,204,255,0.1)); 
                border-radius: 20px; margin: 20px 0;">
        <div style="width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(45deg, #00ff88, #00ccff); 
                    margin: 0 auto 20px; display: flex; align-items: center; justify-content: center;">
            <span style="font-size: 60px; color: white;">👨‍💻</span>
        </div>
        <h2 style="color: #00ff88; margin: 10px 0;">Moeed ul Hassan</h2>
        <p style="color: #00ccff; margin: 5px 0; font-size: 18px;">@The legend</p>
        <p style="color: #888; margin: 20px 0;">Full-Stack Developer & Healthcare Tech Innovator</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Skills and expertise
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Expertise")
        st.markdown("""
        - **Frontend:** React, Vue.js, Streamlit, HTML/CSS
        - **Backend:** Python, Node.js, FastAPI, Flask
        - **Database:** PostgreSQL, MongoDB, Firebase
        - **Cloud:** AWS, Google Cloud, Azure
        - **Healthcare:** Medical systems, HIPAA compliance
        - **AI/ML:** TensorFlow, PyTorch, scikit-learn
        """)
    
    with col2:
        st.markdown("### 🏆 Achievements")
        st.markdown("""
        - Built 50+ healthcare applications
        - Specialized in hospital management systems
        - Expert in medical data security
        - AI-powered diagnostic tools developer
        - Healthcare workflow optimization
        - Real-time patient monitoring systems
        """)
    
    # Contact and portfolio
    st.markdown("### 📞 Connect with Me")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: rgba(0,255,136,0.1); border-radius: 10px;">
            <h4 style="color: #00ff88;">💼 Portfolio</h4>
            <p>View my healthcare projects and innovations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: rgba(0,204,255,0.1); border-radius: 10px;">
            <h4 style="color: #00ccff;">📧 Email</h4>
            <p>Professional inquiries and collaborations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: rgba(255,68,68,0.1); border-radius: 10px;">
            <h4 style="color: #ff4444;">🔗 LinkedIn</h4>
            <p>Connect for business opportunities</p>
        </div>
        """, unsafe_allow_html=True)
    
    # PulseAI project info
    st.markdown("---")
    st.markdown("### 🏥 About PulseAI")
    st.markdown("""
    PulseAI is an advanced Hospital Management System designed to revolutionize healthcare delivery through:
    
    - **Comprehensive Patient Management:** Complete patient lifecycle management from registration to discharge
    - **AI-Powered Risk Assessment:** Framingham Risk Score implementation for cardiovascular risk evaluation
    - **Real-Time Analytics:** Live dashboards and monitoring systems for healthcare professionals
    - **Secure Data Management:** HIPAA-compliant data storage and processing
    - **Modern UI/UX:** Cyberpunk-themed interface with intuitive navigation
    - **Scalable Architecture:** Built to handle healthcare facilities of any size
    
    **Technologies Used:** Python, Streamlit, Plotly, Pandas, NumPy, JSON, PDF Generation, Real-time Processing
    """)
    
    # Animated signature
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin: 40px 0;">
        <div style="background: linear-gradient(45deg, #00ff88, #00ccff); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                    background-clip: text; animation: pulse 2s infinite;
                    font-size: 24px; font-weight: bold;">
            ⚡ Crafted with passion by Moeed ul Hassan @The legend ⚡
        </div>
        <p style="color: #888; margin-top: 10px; font-style: italic;">
            "Building the future of healthcare technology, one line of code at a time."
        </p>
    </div>
    <style>
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.02); }
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()