import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid
from fpdf import FPDF
from io import BytesIO
import base64

class PatientManager:
    """Comprehensive Patient Management System"""
    
    def __init__(self, data_file: str = "data/patients_detailed.json"):
        self.data_file = data_file
        self.patients = self._load_patients()
        self.common_symptoms = [
            "Fever", "Headache", "Cough", "Sore Throat", "Nausea", "Vomiting",
            "Diarrhea", "Abdominal Pain", "Chest Pain", "Shortness of Breath",
            "Dizziness", "Fatigue", "Loss of Appetite", "Joint Pain", "Muscle Pain",
            "Skin Rash", "Swelling", "High Blood Pressure", "Diabetes", "Anxiety"
        ]
        
    def _load_patients(self) -> Dict:
        """Load patient data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {"patients": {}, "visits": {}}
        else:
            return {"patients": {}, "visits": {}}
    
    def _save_patients(self):
        """Save patients to file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.patients, f, indent=2)
    
    def generate_patient_id(self) -> str:
        """Generate unique patient ID"""
        return f"P{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
    
    def add_patient(self, patient_data: Dict) -> str:
        """Add new patient"""
        if patient_data["phone"] not in self.patients["patients"]:
            patient_id = self.generate_patient_id()
            patient_data["patient_id"] = patient_id
            patient_data["created_date"] = datetime.now().isoformat()
            self.patients["patients"][patient_data["phone"]] = patient_data
            self._save_patients()
            return patient_id
        else:
            return self.patients["patients"][patient_data["phone"]]["patient_id"]
    
    def add_visit(self, patient_phone: str, visit_data: Dict) -> str:
        """Add new visit for patient"""
        visit_id = f"V{datetime.now().strftime('%Y%m%d%H%M%S')}"
        visit_data["visit_id"] = visit_id
        visit_data["patient_phone"] = patient_phone
        visit_data["visit_date"] = datetime.now().isoformat()
        
        if patient_phone not in self.patients["visits"]:
            self.patients["visits"][patient_phone] = []
        
        self.patients["visits"][patient_phone].append(visit_data)
        self._save_patients()
        return visit_id
    
    def get_patient_history(self, patient_phone: str) -> List[Dict]:
        """Get patient visit history"""
        return self.patients["visits"].get(patient_phone, [])
    
    def search_patients(self, query: str) -> List[Dict]:
        """Search patients by name, phone, or ID"""
        results = []
        for phone, patient in self.patients["patients"].items():
            if (query.lower() in patient["name"].lower() or 
                query in phone or 
                query in patient.get("patient_id", "")):
                results.append(patient)
        return results
    
    def patient_registration_form(self):
        """Display patient registration form"""
        st.markdown("## 👤 Patient Registration & Visit Management")
        
        # Hospital branding header
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,204,255,0.1)); 
                    border-radius: 15px; margin-bottom: 30px;">
            <h2 style="color: #00ff88; margin: 0;">🏥 PulseAI Medical Center</h2>
            <p style="color: #00ccff; margin: 5px 0;">Advanced Healthcare Management System</p>
            <p style="color: #888; margin: 0; font-size: 14px;">Dr. Sarah Johnson | Chief Medical Officer</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Patient search section
        st.markdown("### 🔍 Search Patient")
        search_query = st.text_input("Search by Name, Phone, or Patient ID", placeholder="Enter search term...")
        
        if search_query:
            results = self.search_patients(search_query)
            if results:
                st.success(f"Found {len(results)} patient(s)")
                for patient in results:
                    with st.expander(f"📋 {patient['name']} (ID: {patient['patient_id']})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Phone:** {patient['phone']}")
                            st.write(f"**Age:** {patient['age']}")
                            st.write(f"**Gender:** {patient['gender']}")
                        with col2:
                            st.write(f"**Address:** {patient.get('address', 'Not provided')}")
                            st.write(f"**Created:** {patient['created_date'][:10]}")
                        
                        # Show visit history
                        history = self.get_patient_history(patient['phone'])
                        if history:
                            st.write(f"**Total Visits:** {len(history)}")
                            if st.button(f"View History - {patient['name']}", key=f"history_{patient['phone']}"):
                                st.session_state.show_history = patient['phone']
        
        # Show patient history if selected
        if hasattr(st.session_state, 'show_history') and st.session_state.show_history:
            self.show_patient_history(st.session_state.show_history)
        
        st.markdown("---")
        
        # New patient/visit form
        form_type = st.radio("Select Action", ["New Patient Registration", "Existing Patient Visit"])
        
        if form_type == "New Patient Registration":
            self.new_patient_form()
        else:
            self.existing_patient_visit_form()
    
    def new_patient_form(self):
        """Form for new patient registration"""
        st.markdown("### 📝 New Patient Registration")
        
        with st.form("new_patient_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Patient Name *", placeholder="Enter full name")
                phone = st.text_input("Phone Number *", placeholder="+1234567890")
                age = st.number_input("Age *", min_value=0, max_value=120, value=25)
                gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
                
            with col2:
                address = st.text_area("Address", placeholder="Enter address (optional)")
                appointment_date = st.date_input("Appointment Date", value=datetime.now().date())
                follow_up = st.selectbox("Follow-up Visit Required?", ["No", "Yes"])
                
            st.markdown("### 🩺 Symptoms")
            symptoms_method = st.radio("How would you like to add symptoms?", 
                                     ["Select from common symptoms", "Enter custom symptoms"])
            
            symptoms = []
            if symptoms_method == "Select from common symptoms":
                symptoms = st.multiselect("Select Symptoms", self.common_symptoms)
            else:
                custom_symptoms = st.text_area("Enter symptoms (one per line)", 
                                             placeholder="Fever\nHeadache\nCough")
                if custom_symptoms:
                    symptoms = [s.strip() for s in custom_symptoms.split('\n') if s.strip()]
            
            # Note about medications
            st.markdown("### 💊 Medications")
            st.info("💡 Medications will be managed separately after patient registration. Go to Medicine Management section to prescribe medicines.")
            
            st.markdown("### 📄 Upload Reports")
            uploaded_files = st.file_uploader("Upload medical reports", 
                                            accept_multiple_files=True,
                                            type=['png', 'jpg', 'jpeg', 'pdf'])
            
            st.markdown("### 📅 Next Visit")
            next_visit_date = st.date_input("Next Visit Date", value=datetime.now().date() + timedelta(days=7))
            next_visit_notes = st.text_area("Instructions for next visit", 
                                          placeholder="Follow-up instructions...")
            
            submitted = st.form_submit_button("Register Patient & Record Visit", use_container_width=True)
            
            if submitted:
                if name and phone and age and gender:
                    # Create patient data
                    patient_data = {
                        "name": name,
                        "phone": phone,
                        "age": age,
                        "gender": gender,
                        "address": address,
                        "follow_up_required": follow_up == "Yes"
                    }
                    
                    # Add patient
                    patient_id = self.add_patient(patient_data)
                    
                    # Create visit data
                    visit_data = {
                        "appointment_date": appointment_date.isoformat(),
                        "symptoms": symptoms,
                        "next_visit_date": next_visit_date.isoformat(),
                        "next_visit_notes": next_visit_notes,
                        "uploaded_files": self._process_uploaded_files(uploaded_files) if uploaded_files else []
                    }
                    
                    # Add visit
                    visit_id = self.add_visit(phone, visit_data)
                    
                    st.success(f"✅ Patient registered successfully!")
                    st.info(f"**Patient ID:** {patient_id}")
                    st.info(f"**Visit ID:** {visit_id}")
                    
                    # Generate PDF report
                    pdf_buffer = self.generate_patient_report(patient_data, visit_data)
                    st.download_button(
                        label="📄 Download Patient Report",
                        data=pdf_buffer,
                        file_name=f"patient_report_{patient_id}_{visit_id}.pdf",
                        mime="application/pdf"
                    )
                    
                else:
                    st.error("Please fill in all required fields marked with *")
    
    def existing_patient_visit_form(self):
        """Form for existing patient visit"""
        st.markdown("### 🔄 Existing Patient Visit")
        
        patient_phone = st.text_input("Enter Patient Phone Number", placeholder="+1234567890")
        
        if patient_phone and patient_phone in self.patients["patients"]:
            patient = self.patients["patients"][patient_phone]
            
            # Display patient info
            st.markdown(f"### 👤 Patient: {patient['name']}")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**ID:** {patient['patient_id']}")
                st.write(f"**Age:** {patient['age']}")
            with col2:
                st.write(f"**Gender:** {patient['gender']}")
                st.write(f"**Phone:** {patient['phone']}")
            
            # Visit form
            with st.form("existing_patient_visit"):
                appointment_date = st.date_input("Appointment Date", value=datetime.now().date())
                
                st.markdown("### 🩺 Symptoms")
                symptoms_method = st.radio("How would you like to add symptoms?", 
                                         ["Select from common symptoms", "Enter custom symptoms"], 
                                         key="existing_symptoms")
                
                symptoms = []
                if symptoms_method == "Select from common symptoms":
                    symptoms = st.multiselect("Select Symptoms", self.common_symptoms, key="existing_symptoms_select")
                else:
                    custom_symptoms = st.text_area("Enter symptoms (one per line)", 
                                                 placeholder="Fever\nHeadache\nCough", 
                                                 key="existing_symptoms_text")
                    if custom_symptoms:
                        symptoms = [s.strip() for s in custom_symptoms.split('\n') if s.strip()]
                
                st.markdown("### 💊 Medications")
                st.info("💡 Medications will be managed separately after visit recording. Go to Medicine Management section to prescribe medicines.")
                
                st.markdown("### 📄 Upload Reports")
                uploaded_files = st.file_uploader("Upload medical reports", 
                                                accept_multiple_files=True,
                                                type=['png', 'jpg', 'jpeg', 'pdf'],
                                                key="existing_files")
                
                st.markdown("### 📅 Next Visit")
                next_visit_date = st.date_input("Next Visit Date", 
                                              value=datetime.now().date() + timedelta(days=7),
                                              key="existing_next_visit")
                next_visit_notes = st.text_area("Instructions for next visit", 
                                              placeholder="Follow-up instructions...",
                                              key="existing_next_notes")
                
                submitted = st.form_submit_button("Record Visit", use_container_width=True)
                
                if submitted:
                    # Create visit data
                    visit_data = {
                        "appointment_date": appointment_date.isoformat(),
                        "symptoms": symptoms,
                        "next_visit_date": next_visit_date.isoformat(),
                        "next_visit_notes": next_visit_notes,
                        "uploaded_files": self._process_uploaded_files(uploaded_files) if uploaded_files else []
                    }
                    
                    # Add visit
                    visit_id = self.add_visit(patient_phone, visit_data)
                    
                    st.success(f"✅ Visit recorded successfully!")
                    st.info(f"**Visit ID:** {visit_id}")
                    
                    # Generate PDF report
                    pdf_buffer = self.generate_patient_report(patient, visit_data)
                    st.download_button(
                        label="📄 Download Visit Report",
                        data=pdf_buffer,
                        file_name=f"visit_report_{patient['patient_id']}_{visit_id}.pdf",
                        mime="application/pdf"
                    )
        
        elif patient_phone:
            st.warning("Patient not found. Please check the phone number or register as new patient.")
    
    def show_patient_history(self, patient_phone: str):
        """Show patient visit history"""
        if patient_phone in self.patients["patients"]:
            patient = self.patients["patients"][patient_phone]
            st.markdown(f"### 📋 Medical History - {patient['name']}")
            
            history = self.get_patient_history(patient_phone)
            if history:
                for i, visit in enumerate(reversed(history)):
                    with st.expander(f"Visit {len(history)-i} - {visit['appointment_date'][:10]}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Visit ID:** {visit['visit_id']}")
                            st.write(f"**Date:** {visit['appointment_date'][:10]}")
                            st.write(f"**Symptoms:** {', '.join(visit['symptoms'])}")
                        with col2:
                            st.write(f"**Medications:** {len(visit['medications'])} prescribed")
                            st.write(f"**Next Visit:** {visit['next_visit_date'][:10]}")
                            if visit['next_visit_notes']:
                                st.write(f"**Notes:** {visit['next_visit_notes']}")
                        
                        if visit['medications']:
                            st.write("**Prescribed Medications:**")
                            for med in visit['medications']:
                                st.write(f"• {med['name']} - {med['dosage']} for {med['duration']}")
            else:
                st.info("No visit history found for this patient.")
    
    def _process_uploaded_files(self, uploaded_files) -> List[Dict]:
        """Process uploaded files"""
        processed_files = []
        for file in uploaded_files:
            # In a real system, you'd save files to a proper storage
            # For now, we'll just store metadata
            processed_files.append({
                "filename": file.name,
                "size": file.size,
                "type": file.type,
                "upload_date": datetime.now().isoformat()
            })
        return processed_files
    
    def generate_patient_report(self, patient_data: Dict, visit_data: Dict) -> bytes:
        """Generate PDF report for patient"""
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'PULSEAI MEDICAL CENTER', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, 'Advanced Healthcare Management System', 0, 1, 'C')
        pdf.cell(0, 10, 'Dr. Sarah Johnson | Chief Medical Officer', 0, 1, 'C')
        pdf.ln(10)
        
        # Patient Info
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'PATIENT INFORMATION', 0, 1)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 8, f'Name: {patient_data["name"]}', 0, 1)
        pdf.cell(0, 8, f'Patient ID: {patient_data["patient_id"]}', 0, 1)
        pdf.cell(0, 8, f'Age: {patient_data["age"]} | Gender: {patient_data["gender"]}', 0, 1)
        pdf.cell(0, 8, f'Phone: {patient_data["phone"]}', 0, 1)
        pdf.ln(5)
        
        # Visit Info
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'VISIT DETAILS', 0, 1)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 8, f'Visit Date: {visit_data["appointment_date"][:10]}', 0, 1)
        pdf.cell(0, 8, f'Symptoms: {", ".join(visit_data["symptoms"])}', 0, 1)
        pdf.ln(5)
        
        # Note about medications
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'MEDICATIONS', 0, 1)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 8, 'Medications will be managed separately in the Medicine Management section.', 0, 1)
        
        # Next Visit
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'NEXT VISIT', 0, 1)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 8, f'Scheduled: {visit_data["next_visit_date"][:10]}', 0, 1)
        if visit_data["next_visit_notes"]:
            pdf.multi_cell(0, 8, f'Instructions: {visit_data["next_visit_notes"]}')
        
        # Footer
        pdf.ln(20)
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 10, 'Report generated by PulseAI Hospital Management System', 0, 1, 'C')
        pdf.cell(0, 10, 'Built on Replit | Crafted by Moeed ul Hassan @The legend', 0, 1, 'C')
        
        return pdf.output(dest='S').encode('latin-1')