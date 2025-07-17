import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
import json
import os

class MedicalRecordsManager:
    """Complete medical records management system"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.records_file = "data/medical_records.json"
        self.visits_file = "data/patient_visits.json"
        self.prescriptions_file = "data/prescriptions.json"
        self.lab_results_file = "data/lab_results.json"
    
    def display_medical_records(self):
        """Main medical records dashboard"""
        st.markdown("## 📋 Medical Records Management")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "👤 Patient Records", "🏥 Visit History", "💊 Prescriptions", 
            "🧪 Lab Results", "📊 Medical Reports"
        ])
        
        with tab1:
            self._display_patient_records()
        
        with tab2:
            self._manage_visit_history()
        
        with tab3:
            self._manage_prescriptions()
        
        with tab4:
            self._manage_lab_results()
        
        with tab5:
            self._generate_medical_reports()
    
    def _display_patient_records(self):
        """Display and manage patient medical records"""
        st.markdown("### 👤 Patient Medical Records")
        
        patients = self.data_manager.get_all_patients()
        
        if not patients:
            st.warning("No patients registered. Please register patients first.")
            return
        
        # Patient selection
        patient_names = [p['name'] for p in patients]
        selected_patient_name = st.selectbox("Select Patient", patient_names)
        
        if selected_patient_name:
            selected_patient = next(p for p in patients if p['name'] == selected_patient_name)
            
            # Display patient basic info
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="background: rgba(0, 255, 136, 0.1); border: 2px solid rgba(0, 255, 136, 0.3); 
                            border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4>👤 Patient Information</h4>
                    <strong>Name:</strong> {selected_patient['name']}<br>
                    <strong>ID:</strong> {selected_patient['id']}<br>
                    <strong>Age:</strong> {selected_patient['age']} years<br>
                    <strong>Gender:</strong> {selected_patient['gender']}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: rgba(0, 204, 255, 0.1); border: 2px solid rgba(0, 204, 255, 0.3); 
                            border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4>📞 Contact Information</h4>
                    <strong>Phone:</strong> {selected_patient.get('phone', 'N/A')}<br>
                    <strong>Email:</strong> {selected_patient.get('email', 'N/A')}<br>
                    <strong>Address:</strong> {selected_patient.get('address', 'N/A')}<br>
                    <strong>Emergency:</strong> {selected_patient.get('emergency_contact', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="background: rgba(255, 165, 0, 0.1); border: 2px solid rgba(255, 165, 0, 0.3); 
                            border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4>🩺 Vital Signs</h4>
                    <strong>Blood Pressure:</strong> {selected_patient.get('systolic_bp', 'N/A')}/{selected_patient.get('diastolic_bp', 'N/A')} mmHg<br>
                    <strong>Cholesterol:</strong> {selected_patient.get('total_cholesterol', 'N/A')} mg/dL<br>
                    <strong>HDL:</strong> {selected_patient.get('hdl_cholesterol', 'N/A')} mg/dL<br>
                    <strong>BMI:</strong> {selected_patient.get('bmi', 'N/A')} kg/m²
                </div>
                """, unsafe_allow_html=True)
            
            # Medical history
            st.markdown("### 📜 Medical History")
            
            # Add new medical history entry
            with st.expander("➕ Add Medical History Entry"):
                with st.form("add_medical_history"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        condition = st.text_input("Medical Condition")
                        diagnosis_date = st.date_input("Diagnosis Date")
                        severity = st.selectbox("Severity", ["Mild", "Moderate", "Severe", "Critical"])
                        status = st.selectbox("Status", ["Active", "Resolved", "Chronic", "Under Treatment"])
                    
                    with col2:
                        treatment = st.text_area("Treatment/Medication")
                        doctor = st.text_input("Attending Doctor")
                        notes = st.text_area("Additional Notes")
                    
                    if st.form_submit_button("Add Medical History"):
                        history_entry = {
                            'condition': condition,
                            'diagnosis_date': str(diagnosis_date),
                            'severity': severity,
                            'status': status,
                            'treatment': treatment,
                            'doctor': doctor,
                            'notes': notes,
                            'added_date': datetime.now().isoformat()
                        }
                        
                        self._add_medical_history(selected_patient['id'], history_entry)
                        st.success("Medical history entry added successfully!")
                        st.rerun()
            
            # Display existing medical history
            medical_records = self._load_data(self.records_file)
            patient_records = medical_records.get(selected_patient['id'], [])
            
            if patient_records:
                st.markdown("#### Existing Medical History")
                
                for i, record in enumerate(patient_records):
                    status_color = {
                        'Active': '#ff4444',
                        'Resolved': '#00ff88',
                        'Chronic': '#ffa500',
                        'Under Treatment': '#00ccff'
                    }.get(record['status'], '#ffffff')
                    
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.05); border-left: 4px solid {status_color}; 
                                padding: 15px; margin: 10px 0; border-radius: 5px;">
                        <strong>{record['condition']}</strong> ({record['severity']})<br>
                        <strong>Diagnosed:</strong> {record['diagnosis_date']}<br>
                        <strong>Status:</strong> <span style="color: {status_color};">{record['status']}</span><br>
                        <strong>Doctor:</strong> {record.get('doctor', 'N/A')}<br>
                        <strong>Treatment:</strong> {record.get('treatment', 'N/A')}<br>
                        {f"<strong>Notes:</strong> {record.get('notes', '')}" if record.get('notes') else ""}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No medical history recorded for this patient.")
    
    def _manage_visit_history(self):
        """Manage patient visit history"""
        st.markdown("### 🏥 Patient Visit Management")
        
        # Record new visit
        with st.expander("➕ Record New Visit"):
            patients = self.data_manager.get_all_patients()
            if patients:
                patient_names = [p['name'] for p in patients]
                selected_patient = st.selectbox("Select Patient", patient_names, key="visit_patient")
                
                with st.form("record_visit"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        visit_date = st.date_input("Visit Date", datetime.now().date())
                        visit_time = st.time_input("Visit Time", datetime.now().time())
                        visit_type = st.selectbox("Visit Type", [
                            "Regular Checkup", "Emergency", "Follow-up", 
                            "Consultation", "Procedure", "Surgery"
                        ])
                        department = st.selectbox("Department", [
                            "General Medicine", "Emergency", "Cardiology", 
                            "Surgery", "Pediatrics", "Orthopedics"
                        ])
                    
                    with col2:
                        doctor = st.text_input("Attending Doctor")
                        chief_complaint = st.text_area("Chief Complaint")
                        diagnosis = st.text_area("Diagnosis")
                        treatment_plan = st.text_area("Treatment Plan")
                    
                    vital_signs = st.text_area("Vital Signs")
                    visit_notes = st.text_area("Visit Notes")
                    
                    if st.form_submit_button("Record Visit"):
                        if selected_patient:
                            patient = next(p for p in patients if p['name'] == selected_patient)
                            
                            visit_data = {
                                'patient_id': patient['id'],
                                'patient_name': patient['name'],
                                'visit_date': str(visit_date),
                                'visit_time': str(visit_time),
                                'visit_type': visit_type,
                                'department': department,
                                'doctor': doctor,
                                'chief_complaint': chief_complaint,
                                'diagnosis': diagnosis,
                                'treatment_plan': treatment_plan,
                                'vital_signs': vital_signs,
                                'visit_notes': visit_notes,
                                'recorded_at': datetime.now().isoformat()
                            }
                            
                            visits = self._load_data(self.visits_file)
                            visit_id = f"VISIT_{len(visits) + 1:04d}"
                            visits[visit_id] = visit_data
                            self._save_data(self.visits_file, visits)
                            
                            st.success("Visit recorded successfully!")
                            st.rerun()
        
        # Display recent visits
        visits = self._load_data(self.visits_file)
        
        if visits:
            st.markdown("#### Recent Visits")
            
            # Sort visits by date
            sorted_visits = sorted(visits.items(), 
                                 key=lambda x: x[1]['visit_date'], reverse=True)
            
            for visit_id, visit in sorted_visits[:10]:  # Show last 10 visits
                visit_type_color = {
                    'Emergency': '#ff4444',
                    'Regular Checkup': '#00ff88',
                    'Follow-up': '#00ccff',
                    'Consultation': '#ffa500',
                    'Procedure': '#8A2BE2',
                    'Surgery': '#ff69b4'
                }.get(visit['visit_type'], '#ffffff')
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); border-left: 4px solid {visit_type_color}; 
                            padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <strong>{visit['patient_name']}</strong> - {visit['visit_type']}<br>
                    <strong>Date:</strong> {visit['visit_date']} at {visit.get('visit_time', 'N/A')}<br>
                    <strong>Department:</strong> {visit['department']}<br>
                    <strong>Doctor:</strong> {visit.get('doctor', 'N/A')}<br>
                    <strong>Complaint:</strong> {visit.get('chief_complaint', 'N/A')}<br>
                    <strong>Diagnosis:</strong> {visit.get('diagnosis', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No visits recorded yet.")
    
    def _manage_prescriptions(self):
        """Manage patient prescriptions"""
        st.markdown("### 💊 Prescription Management")
        
        # Add new prescription
        with st.expander("➕ Create New Prescription"):
            patients = self.data_manager.get_all_patients()
            if patients:
                patient_names = [p['name'] for p in patients]
                selected_patient = st.selectbox("Select Patient", patient_names, key="prescription_patient")
                
                with st.form("create_prescription"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        medication_name = st.text_input("Medication Name")
                        dosage = st.text_input("Dosage (e.g., 500mg)")
                        frequency = st.selectbox("Frequency", [
                            "Once daily", "Twice daily", "Three times daily", 
                            "Four times daily", "As needed", "Before meals", "After meals"
                        ])
                        duration = st.text_input("Duration (e.g., 7 days)")
                    
                    with col2:
                        prescribed_date = st.date_input("Prescribed Date", datetime.now().date())
                        doctor = st.text_input("Prescribing Doctor")
                        pharmacy = st.text_input("Pharmacy")
                        refills = st.number_input("Number of Refills", min_value=0, max_value=10, value=0)
                    
                    instructions = st.text_area("Special Instructions")
                    indication = st.text_area("Indication/Reason")
                    
                    if st.form_submit_button("Create Prescription"):
                        if selected_patient and medication_name:
                            patient = next(p for p in patients if p['name'] == selected_patient)
                            
                            prescription_data = {
                                'patient_id': patient['id'],
                                'patient_name': patient['name'],
                                'medication_name': medication_name,
                                'dosage': dosage,
                                'frequency': frequency,
                                'duration': duration,
                                'prescribed_date': str(prescribed_date),
                                'doctor': doctor,
                                'pharmacy': pharmacy,
                                'refills': refills,
                                'instructions': instructions,
                                'indication': indication,
                                'status': 'Active',
                                'created_at': datetime.now().isoformat()
                            }
                            
                            prescriptions = self._load_data(self.prescriptions_file)
                            prescription_id = f"RX_{len(prescriptions) + 1:04d}"
                            prescriptions[prescription_id] = prescription_data
                            self._save_data(self.prescriptions_file, prescriptions)
                            
                            st.success("Prescription created successfully!")
                            st.rerun()
        
        # Display active prescriptions
        prescriptions = self._load_data(self.prescriptions_file)
        
        if prescriptions:
            st.markdown("#### Active Prescriptions")
            
            for prescription_id, prescription in prescriptions.items():
                if prescription.get('status') == 'Active':
                    st.markdown(f"""
                    <div style="background: rgba(0, 255, 136, 0.1); border: 2px solid rgba(0, 255, 136, 0.3); 
                                border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <strong>{prescription['medication_name']}</strong> - {prescription['dosage']}<br>
                        <strong>Patient:</strong> {prescription['patient_name']}<br>
                        <strong>Frequency:</strong> {prescription['frequency']}<br>
                        <strong>Duration:</strong> {prescription.get('duration', 'N/A')}<br>
                        <strong>Doctor:</strong> {prescription.get('doctor', 'N/A')}<br>
                        <strong>Prescribed:</strong> {prescription['prescribed_date']}<br>
                        {f"<strong>Instructions:</strong> {prescription.get('instructions', '')}" if prescription.get('instructions') else ""}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No prescriptions found.")
    
    def _manage_lab_results(self):
        """Manage laboratory test results"""
        st.markdown("### 🧪 Laboratory Results Management")
        
        # Add new lab result
        with st.expander("➕ Add Lab Result"):
            patients = self.data_manager.get_all_patients()
            if patients:
                patient_names = [p['name'] for p in patients]
                selected_patient = st.selectbox("Select Patient", patient_names, key="lab_patient")
                
                with st.form("add_lab_result"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        test_name = st.text_input("Test Name")
                        test_date = st.date_input("Test Date", datetime.now().date())
                        test_type = st.selectbox("Test Type", [
                            "Blood Test", "Urine Test", "X-Ray", "MRI", 
                            "CT Scan", "ECG", "Ultrasound", "Biopsy"
                        ])
                        lab_technician = st.text_input("Lab Technician")
                    
                    with col2:
                        result_value = st.text_input("Result Value")
                        reference_range = st.text_input("Reference Range")
                        unit = st.text_input("Unit")
                        status = st.selectbox("Status", ["Normal", "Abnormal", "Critical", "Pending"])
                    
                    interpretation = st.text_area("Interpretation")
                    notes = st.text_area("Additional Notes")
                    
                    if st.form_submit_button("Add Lab Result"):
                        if selected_patient and test_name:
                            patient = next(p for p in patients if p['name'] == selected_patient)
                            
                            lab_result = {
                                'patient_id': patient['id'],
                                'patient_name': patient['name'],
                                'test_name': test_name,
                                'test_date': str(test_date),
                                'test_type': test_type,
                                'lab_technician': lab_technician,
                                'result_value': result_value,
                                'reference_range': reference_range,
                                'unit': unit,
                                'status': status,
                                'interpretation': interpretation,
                                'notes': notes,
                                'created_at': datetime.now().isoformat()
                            }
                            
                            lab_results = self._load_data(self.lab_results_file)
                            result_id = f"LAB_{len(lab_results) + 1:04d}"
                            lab_results[result_id] = lab_result
                            self._save_data(self.lab_results_file, lab_results)
                            
                            st.success("Lab result added successfully!")
                            st.rerun()
        
        # Display recent lab results
        lab_results = self._load_data(self.lab_results_file)
        
        if lab_results:
            st.markdown("#### Recent Lab Results")
            
            for result_id, result in list(lab_results.items())[-10:]:  # Show last 10 results
                status_color = {
                    'Normal': '#00ff88',
                    'Abnormal': '#ffa500',
                    'Critical': '#ff4444',
                    'Pending': '#00ccff'
                }.get(result['status'], '#ffffff')
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); border-left: 4px solid {status_color}; 
                            padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <strong>{result['test_name']}</strong> ({result['test_type']})<br>
                    <strong>Patient:</strong> {result['patient_name']}<br>
                    <strong>Date:</strong> {result['test_date']}<br>
                    <strong>Result:</strong> {result.get('result_value', 'N/A')} {result.get('unit', '')}<br>
                    <strong>Reference:</strong> {result.get('reference_range', 'N/A')}<br>
                    <strong>Status:</strong> <span style="color: {status_color};">{result['status']}</span><br>
                    {f"<strong>Interpretation:</strong> {result.get('interpretation', '')}" if result.get('interpretation') else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No lab results recorded yet.")
    
    def _generate_medical_reports(self):
        """Generate comprehensive medical reports"""
        st.markdown("### 📊 Medical Reports & Analytics")
        
        patients = self.data_manager.get_all_patients()
        if not patients:
            st.warning("No patient data available for reports.")
            return
        
        # Patient medical summary report
        patient_names = [p['name'] for p in patients]
        selected_patient = st.selectbox("Select Patient for Report", patient_names)
        
        if selected_patient:
            patient = next(p for p in patients if p['name'] == selected_patient)
            
            if st.button("📄 Generate Complete Medical Report", use_container_width=True):
                st.markdown(f"### 📋 Complete Medical Report: {patient['name']}")
                
                # Patient summary
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Patient Demographics")
                    st.write(f"**Name:** {patient['name']}")
                    st.write(f"**Patient ID:** {patient['id']}")
                    st.write(f"**Age:** {patient['age']} years")
                    st.write(f"**Gender:** {patient['gender']}")
                    st.write(f"**Registration Date:** {patient.get('registration_date', 'N/A')}")
                
                with col2:
                    st.markdown("#### Current Vital Signs")
                    st.write(f"**Blood Pressure:** {patient.get('systolic_bp', 'N/A')}/{patient.get('diastolic_bp', 'N/A')} mmHg")
                    st.write(f"**Total Cholesterol:** {patient.get('total_cholesterol', 'N/A')} mg/dL")
                    st.write(f"**HDL Cholesterol:** {patient.get('hdl_cholesterol', 'N/A')} mg/dL")
                    st.write(f"**BMI:** {patient.get('bmi', 'N/A')} kg/m²")
                
                # Medical history
                medical_records = self._load_data(self.records_file)
                patient_records = medical_records.get(patient['id'], [])
                
                if patient_records:
                    st.markdown("#### Medical History")
                    for record in patient_records:
                        st.write(f"• **{record['condition']}** ({record['status']}) - Diagnosed: {record['diagnosis_date']}")
                
                # Recent visits
                visits = self._load_data(self.visits_file)
                patient_visits = [v for v in visits.values() if v['patient_id'] == patient['id']]
                
                if patient_visits:
                    st.markdown("#### Recent Visits")
                    for visit in patient_visits[-5:]:  # Last 5 visits
                        st.write(f"• **{visit['visit_date']}** - {visit['visit_type']} ({visit['department']})")
                
                # Active prescriptions
                prescriptions = self._load_data(self.prescriptions_file)
                patient_prescriptions = [p for p in prescriptions.values() 
                                       if p['patient_id'] == patient['id'] and p.get('status') == 'Active']
                
                if patient_prescriptions:
                    st.markdown("#### Active Prescriptions")
                    for prescription in patient_prescriptions:
                        st.write(f"• **{prescription['medication_name']}** - {prescription['dosage']} ({prescription['frequency']})")
                
                # Recent lab results
                lab_results = self._load_data(self.lab_results_file)
                patient_labs = [l for l in lab_results.values() if l['patient_id'] == patient['id']]
                
                if patient_labs:
                    st.markdown("#### Recent Lab Results")
                    for lab in patient_labs[-5:]:  # Last 5 lab results
                        st.write(f"• **{lab['test_name']}** ({lab['test_date']}): {lab.get('result_value', 'N/A')} - {lab['status']}")
    
    def _add_medical_history(self, patient_id: str, history_entry: dict):
        """Add medical history entry for a patient"""
        medical_records = self._load_data(self.records_file)
        
        if patient_id not in medical_records:
            medical_records[patient_id] = []
        
        medical_records[patient_id].append(history_entry)
        self._save_data(self.records_file, medical_records)
    
    def _load_data(self, filename: str) -> dict:
        """Load data from JSON file"""
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_data(self, filename: str, data: dict):
        """Save data to JSON file"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)