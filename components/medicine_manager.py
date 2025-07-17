import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class MedicineManager:
    """Medicine Management System for Patients"""
    
    def __init__(self, data_file: str = "data/medicines.json"):
        self.data_file = data_file
        self.medicines = self._load_medicines()
        self.timing_options = [
            "Morning", "Afternoon", "Evening", "Night",
            "Before Breakfast", "After Breakfast", "Before Lunch", "After Lunch",
            "Before Dinner", "After Dinner", "As Needed", "Every 4 Hours",
            "Every 6 Hours", "Every 8 Hours", "Every 12 Hours", "Once Daily"
        ]
        
    def _load_medicines(self) -> Dict:
        """Load medicine data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {"patient_medicines": {}}
        else:
            return {"patient_medicines": {}}
    
    def _save_medicines(self):
        """Save medicines to file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.medicines, f, indent=2)
    
    def add_medicine(self, patient_phone: str, medicine_data: Dict):
        """Add medicine for a patient"""
        if patient_phone not in self.medicines["patient_medicines"]:
            self.medicines["patient_medicines"][patient_phone] = []
        
        medicine_data["prescribed_date"] = datetime.now().isoformat()
        medicine_data["medicine_id"] = f"MED{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        self.medicines["patient_medicines"][patient_phone].append(medicine_data)
        self._save_medicines()
    
    def get_patient_medicines(self, patient_phone: str) -> List[Dict]:
        """Get all medicines for a patient"""
        return self.medicines["patient_medicines"].get(patient_phone, [])
    
    def update_medicine(self, patient_phone: str, medicine_id: str, updated_data: Dict):
        """Update medicine information"""
        if patient_phone in self.medicines["patient_medicines"]:
            for i, medicine in enumerate(self.medicines["patient_medicines"][patient_phone]):
                if medicine["medicine_id"] == medicine_id:
                    self.medicines["patient_medicines"][patient_phone][i].update(updated_data)
                    self._save_medicines()
                    return True
        return False
    
    def remove_medicine(self, patient_phone: str, medicine_id: str):
        """Remove a medicine from patient's prescription"""
        if patient_phone in self.medicines["patient_medicines"]:
            self.medicines["patient_medicines"][patient_phone] = [
                med for med in self.medicines["patient_medicines"][patient_phone] 
                if med["medicine_id"] != medicine_id
            ]
            self._save_medicines()
    
    def display_medicine_management(self):
        """Display medicine management interface"""
        st.markdown("""
        <div style="text-align: center; padding: 20px; font-family: 'Poppins', sans-serif;">
            <h1 style="color: #00ff88; margin-bottom: 10px;">💊 Medicine Management System</h1>
            <p style="color: #00ccff; margin: 0;">Manage patient prescriptions and dosage schedules</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Load patients from patient manager
        try:
            with open("data/patients_detailed.json", 'r') as f:
                patients_data = json.load(f)
            patients = patients_data.get("patients", {})
        except (FileNotFoundError, json.JSONDecodeError):
            st.error("No patient data found. Please register patients first.")
            return
        
        if not patients:
            st.info("No patients registered. Please register patients first in the Patient Management section.")
            return
        
        # Patient selection
        st.markdown("### 👥 Select Patient")
        patient_options = {f"{patient['name']} - {phone}": phone for phone, patient in patients.items()}
        selected_patient_display = st.selectbox("Choose patient:", list(patient_options.keys()))
        
        if selected_patient_display:
            selected_patient_phone = patient_options[selected_patient_display]
            selected_patient = patients[selected_patient_phone]
            
            # Display patient info
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,204,255,0.1)); 
                        border-radius: 15px; padding: 20px; margin: 20px 0; font-family: 'Poppins', sans-serif;">
                <h3 style="color: #00ff88; margin: 0 0 15px 0;">📋 Patient Information</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div>
                        <p style="margin: 5px 0; color: #fff;"><strong>Name:</strong> {selected_patient['name']}</p>
                        <p style="margin: 5px 0; color: #fff;"><strong>ID:</strong> {selected_patient['patient_id']}</p>
                    </div>
                    <div>
                        <p style="margin: 5px 0; color: #fff;"><strong>Age:</strong> {selected_patient['age']}</p>
                        <p style="margin: 5px 0; color: #fff;"><strong>Phone:</strong> {selected_patient['phone']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Medicine management tabs
            tab1, tab2, tab3 = st.tabs(["💊 Add Medicine", "📋 View Medicines", "📊 Medicine History"])
            
            with tab1:
                self._show_add_medicine_form(selected_patient_phone)
            
            with tab2:
                self._show_current_medicines(selected_patient_phone, selected_patient['name'])
            
            with tab3:
                self._show_medicine_history(selected_patient_phone, selected_patient['name'])
    
    def _show_add_medicine_form(self, patient_phone: str):
        """Show form to add new medicine"""
        st.markdown("### ➕ Add New Medicine")
        
        with st.form("add_medicine_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                medicine_name = st.text_input("Medicine Name *", placeholder="e.g., Paracetamol")
                dosage = st.text_input("Dosage *", placeholder="e.g., 500mg")
                frequency = st.selectbox("Frequency *", [
                    "Once daily", "Twice daily", "Three times daily", 
                    "Four times daily", "As needed", "Every 4 hours",
                    "Every 6 hours", "Every 8 hours", "Every 12 hours"
                ])
                
            with col2:
                timing = st.multiselect("Timing *", self.timing_options, default=["Morning"])
                duration = st.text_input("Duration *", placeholder="e.g., 7 days")
                instructions = st.text_area("Special Instructions", placeholder="Take with food, avoid alcohol, etc.")
            
            # Medicine details
            col1, col2 = st.columns(2)
            with col1:
                medicine_type = st.selectbox("Type", [
                    "Tablet", "Capsule", "Syrup", "Injection", "Drops", 
                    "Cream", "Ointment", "Spray", "Inhaler", "Other"
                ])
                
            with col2:
                purpose = st.text_input("Purpose/Condition", placeholder="e.g., Pain relief, Fever")
            
            submitted = st.form_submit_button("💊 Add Medicine", use_container_width=True)
            
            if submitted:
                if medicine_name and dosage and frequency and timing and duration:
                    medicine_data = {
                        "medicine_name": medicine_name,
                        "dosage": dosage,
                        "frequency": frequency,
                        "timing": timing,
                        "duration": duration,
                        "instructions": instructions,
                        "medicine_type": medicine_type,
                        "purpose": purpose,
                        "status": "Active"
                    }
                    
                    self.add_medicine(patient_phone, medicine_data)
                    st.success(f"✅ Medicine '{medicine_name}' added successfully!")
                else:
                    st.error("Please fill in all required fields marked with *")
    
    def _show_current_medicines(self, patient_phone: str, patient_name: str):
        """Show current medicines for patient"""
        st.markdown("### 📋 Current Medicines")
        
        medicines = self.get_patient_medicines(patient_phone)
        active_medicines = [med for med in medicines if med.get("status", "Active") == "Active"]
        
        if active_medicines:
            for medicine in active_medicines:
                with st.expander(f"💊 {medicine['medicine_name']} - {medicine['dosage']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Frequency:** {medicine['frequency']}")
                        st.write(f"**Timing:** {', '.join(medicine['timing'])}")
                        st.write(f"**Duration:** {medicine['duration']}")
                        st.write(f"**Type:** {medicine['medicine_type']}")
                        
                    with col2:
                        st.write(f"**Purpose:** {medicine.get('purpose', 'N/A')}")
                        st.write(f"**Prescribed:** {medicine['prescribed_date'][:10]}")
                        if medicine.get('instructions'):
                            st.write(f"**Instructions:** {medicine['instructions']}")
                    
                    # Action buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"🔄 Mark as Completed", key=f"complete_{medicine['medicine_id']}"):
                            self.update_medicine(patient_phone, medicine['medicine_id'], {"status": "Completed"})
                            st.success("Medicine marked as completed!")
                            st.rerun()
                    
                    with col2:
                        if st.button(f"❌ Remove", key=f"remove_{medicine['medicine_id']}"):
                            self.remove_medicine(patient_phone, medicine['medicine_id'])
                            st.success("Medicine removed!")
                            st.rerun()
        else:
            st.info("No active medicines prescribed for this patient.")
    
    def _show_medicine_history(self, patient_phone: str, patient_name: str):
        """Show medicine history for patient"""
        st.markdown("### 📊 Medicine History")
        
        medicines = self.get_patient_medicines(patient_phone)
        
        if medicines:
            # Statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_medicines = len(medicines)
                st.metric("Total Prescribed", total_medicines)
            
            with col2:
                active_count = len([med for med in medicines if med.get("status", "Active") == "Active"])
                st.metric("Currently Active", active_count)
            
            with col3:
                completed_count = len([med for med in medicines if med.get("status") == "Completed"])
                st.metric("Completed", completed_count)
            
            # History table
            st.markdown("#### 📋 Complete Medicine History")
            
            history_data = []
            for medicine in sorted(medicines, key=lambda x: x['prescribed_date'], reverse=True):
                history_data.append({
                    "Medicine": medicine['medicine_name'],
                    "Dosage": medicine['dosage'],
                    "Frequency": medicine['frequency'],
                    "Duration": medicine['duration'],
                    "Prescribed Date": medicine['prescribed_date'][:10],
                    "Status": medicine.get('status', 'Active'),
                    "Purpose": medicine.get('purpose', 'N/A')
                })
            
            if history_data:
                import pandas as pd
                df = pd.DataFrame(history_data)
                st.dataframe(df, use_container_width=True)
                
                # Download history as CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Medicine History",
                    data=csv,
                    file_name=f"medicine_history_{patient_name}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("No medicine history found for this patient.")