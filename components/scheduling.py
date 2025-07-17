import streamlit as st
from datetime import datetime, timedelta, time
import json
import os
from typing import Dict, List, Optional
import schedule

class AppointmentScheduler:
    """Advanced appointment scheduling system"""
    
    def __init__(self, appointments_file: str = "data/appointments.json"):
        self.appointments_file = appointments_file
        self.appointments = self._load_appointments()
    
    def _load_appointments(self) -> List[Dict]:
        """Load appointments from file"""
        if os.path.exists(self.appointments_file):
            try:
                with open(self.appointments_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def _save_appointments(self):
        """Save appointments to file"""
        os.makedirs(os.path.dirname(self.appointments_file), exist_ok=True)
        with open(self.appointments_file, 'w') as f:
            json.dump(self.appointments, f, indent=2, default=str)
    
    def book_appointment(self, patient_id: str, patient_name: str, 
                        doctor: str, department: str, date: str, 
                        time_slot: str, notes: str = ""):
        """Book a new appointment"""
        appointment = {
            "id": len(self.appointments) + 1,
            "patient_id": patient_id,
            "patient_name": patient_name,
            "doctor": doctor,
            "department": department,
            "date": date,
            "time": time_slot,
            "status": "scheduled",
            "notes": notes,
            "created_at": datetime.now().isoformat()
        }
        self.appointments.append(appointment)
        self._save_appointments()
        return appointment["id"]
    
    def get_available_slots(self, date: str, doctor: str = None) -> List[str]:
        """Get available time slots for a date"""
        # Define working hours (9 AM to 5 PM)
        time_slots = []
        start_hour = 9
        end_hour = 17
        
        for hour in range(start_hour, end_hour):
            for minute in [0, 30]:
                time_str = f"{hour:02d}:{minute:02d}"
                time_slots.append(time_str)
        
        # Filter out booked slots
        booked_slots = []
        for appointment in self.appointments:
            if appointment["date"] == date:
                if doctor is None or appointment["doctor"] == doctor:
                    booked_slots.append(appointment["time"])
        
        available_slots = [slot for slot in time_slots if slot not in booked_slots]
        return available_slots
    
    def get_appointments_by_date(self, date: str) -> List[Dict]:
        """Get all appointments for a specific date"""
        return [apt for apt in self.appointments if apt["date"] == date]
    
    def get_patient_appointments(self, patient_id: str) -> List[Dict]:
        """Get all appointments for a patient"""
        return [apt for apt in self.appointments if apt["patient_id"] == patient_id]
    
    def update_appointment_status(self, appointment_id: int, status: str):
        """Update appointment status"""
        for appointment in self.appointments:
            if appointment["id"] == appointment_id:
                appointment["status"] = status
                break
        self._save_appointments()
    
    def display_appointment_calendar(self):
        """Display interactive appointment calendar"""
        st.subheader("📅 Appointment Calendar")
        
        # Date selection
        selected_date = st.date_input("Select Date", datetime.now().date())
        
        # Get appointments for selected date
        daily_appointments = self.get_appointments_by_date(str(selected_date))
        
        if daily_appointments:
            st.markdown("### Scheduled Appointments")
            for apt in sorted(daily_appointments, key=lambda x: x["time"]):
                status_color = {
                    "scheduled": "#00ccff",
                    "completed": "#00ff88",
                    "cancelled": "#ff4444",
                    "no-show": "#ffa500"
                }.get(apt["status"], "#ffffff")
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); border-left: 4px solid {status_color}; 
                            padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <strong>🕐 {apt['time']} - Dr. {apt['doctor']}</strong><br>
                    <strong>Patient:</strong> {apt['patient_name']}<br>
                    <strong>Department:</strong> {apt['department']}<br>
                    <strong>Status:</strong> <span style="color: {status_color};">{apt['status'].title()}</span><br>
                    {f"<strong>Notes:</strong> {apt['notes']}" if apt['notes'] else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No appointments scheduled for this date.")
    
    def display_booking_form(self):
        """Display appointment booking form"""
        st.subheader("📝 Book New Appointment")
        
        with st.form("appointment_booking"):
            col1, col2 = st.columns(2)
            
            with col1:
                patient_id = st.text_input("Patient ID")
                patient_name = st.text_input("Patient Name")
                department = st.selectbox("Department", [
                    "Cardiology", "Internal Medicine", "Emergency", 
                    "Orthopedics", "Pediatrics", "Neurology", "Radiology"
                ])
            
            with col2:
                doctor = st.selectbox("Doctor", [
                    "Dr. Smith", "Dr. Johnson", "Dr. Williams", 
                    "Dr. Brown", "Dr. Davis", "Dr. Miller"
                ])
                apt_date = st.date_input("Appointment Date", min_value=datetime.now().date())
                time_slot = st.selectbox("Time Slot", self.get_available_slots(str(apt_date), doctor))
            
            notes = st.text_area("Additional Notes", height=100)
            
            if st.form_submit_button("Book Appointment", use_container_width=True):
                if patient_id and patient_name and time_slot:
                    apt_id = self.book_appointment(
                        patient_id, patient_name, doctor, 
                        department, str(apt_date), time_slot, notes
                    )
                    st.success(f"Appointment booked successfully! ID: {apt_id}")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")