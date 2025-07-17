import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
import json
import os

class BedManagementSystem:
    """Complete bed and room management system"""
    
    def __init__(self):
        self.beds_file = "data/beds.json"
        self.admissions_file = "data/admissions.json"
        self.transfers_file = "data/transfers.json"
        self.rooms_file = "data/rooms.json"
    
    def display_bed_management(self):
        """Main bed management dashboard"""
        st.markdown("## 🛏️ Bed & Room Management")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Bed Status", "🏥 Patient Admissions", "↔️ Transfers", "⚙️ Room Management"
        ])
        
        with tab1:
            self._display_bed_status()
        
        with tab2:
            self._manage_admissions()
        
        with tab3:
            self._manage_transfers()
        
        with tab4:
            self._manage_rooms()
    
    def _display_bed_status(self):
        """Display real-time bed status"""
        st.markdown("### 🛏️ Real-Time Bed Status")
        
        beds = self._load_data(self.beds_file)
        
        if not beds:
            beds = self._initialize_default_beds()
            self._save_data(self.beds_file, beds)
        
        # Calculate bed statistics
        total_beds = len(beds)
        occupied_beds = sum(1 for bed in beds.values() if bed.get('status') == 'Occupied')
        available_beds = sum(1 for bed in beds.values() if bed.get('status') == 'Available')
        maintenance_beds = sum(1 for bed in beds.values() if bed.get('status') == 'Maintenance')
        
        occupancy_rate = (occupied_beds / total_beds * 100) if total_beds > 0 else 0
        
        # Display metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Beds", total_beds)
        
        with col2:
            st.metric("Occupied", occupied_beds, delta=f"+{occupied_beds - 5}")
        
        with col3:
            st.metric("Available", available_beds, delta=f"-{5 - available_beds}")
        
        with col4:
            st.metric("Maintenance", maintenance_beds)
        
        with col5:
            st.metric("Occupancy Rate", f"{occupancy_rate:.1f}%", delta="+2.3%")
        
        # Bed status by department
        st.markdown("### 🏥 Bed Status by Department")
        
        departments = {}
        for bed in beds.values():
            dept = bed.get('department', 'Unknown')
            if dept not in departments:
                departments[dept] = {'total': 0, 'occupied': 0, 'available': 0, 'maintenance': 0}
            
            departments[dept]['total'] += 1
            status = bed.get('status', 'Unknown')
            if status == 'Occupied':
                departments[dept]['occupied'] += 1
            elif status == 'Available':
                departments[dept]['available'] += 1
            elif status == 'Maintenance':
                departments[dept]['maintenance'] += 1
        
        # Display department status
        for dept_name, dept_data in departments.items():
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"**{dept_name}**")
            
            with col2:
                st.markdown(f"Total: {dept_data['total']}")
            
            with col3:
                occupancy = (dept_data['occupied'] / dept_data['total'] * 100) if dept_data['total'] > 0 else 0
                st.markdown(f"Occupancy: {occupancy:.1f}%")
            
            with col4:
                st.markdown(f"Available: {dept_data['available']}")
        
        # Visual bed map
        st.markdown("### 🗺️ Bed Availability Map")
        
        # Group beds by department for visual display
        for dept_name, dept_data in departments.items():
            with st.expander(f"{dept_name} Department ({dept_data['available']} available)"):
                dept_beds = {bid: bed for bid, bed in beds.items() if bed.get('department') == dept_name}
                
                # Display beds in a grid
                cols = st.columns(5)
                for i, (bed_id, bed) in enumerate(dept_beds.items()):
                    col_idx = i % 5
                    
                    status_color = {
                        'Available': '#00ff88',
                        'Occupied': '#ff4444',
                        'Maintenance': '#ffa500',
                        'Reserved': '#00ccff'
                    }.get(bed.get('status'), '#666666')
                    
                    with cols[col_idx]:
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.05); border: 2px solid {status_color}; 
                                    border-radius: 8px; padding: 10px; margin: 5px; text-align: center;">
                            <strong>{bed.get('bed_number', 'N/A')}</strong><br>
                            <small style="color: {status_color};">{bed.get('status', 'Unknown')}</small><br>
                            {f"<small>{bed.get('patient_name', '')}</small>" if bed.get('patient_name') else ""}
                        </div>
                        """, unsafe_allow_html=True)
    
    def _manage_admissions(self):
        """Manage patient admissions"""
        st.markdown("### 🏥 Patient Admissions")
        
        # New admission form
        with st.expander("➕ New Patient Admission"):
            with st.form("new_admission"):
                col1, col2 = st.columns(2)
                
                with col1:
                    patient_id = st.text_input("Patient ID")
                    patient_name = st.text_input("Patient Name")
                    admission_date = st.date_input("Admission Date", datetime.now().date())
                    admission_time = st.time_input("Admission Time", datetime.now().time())
                    admission_type = st.selectbox("Admission Type", [
                        "Emergency", "Scheduled", "Transfer", "Outpatient"
                    ])
                
                with col2:
                    department = st.selectbox("Department", [
                        "Emergency", "ICU", "General Surgery", "Cardiology", 
                        "Pediatrics", "Maternity", "Orthopedics"
                    ])
                    
                    # Get available beds for selected department
                    beds = self._load_data(self.beds_file)
                    available_beds = [
                        f"{bed['bed_number']} ({bed['room_number']})"
                        for bed in beds.values()
                        if bed.get('department') == department and bed.get('status') == 'Available'
                    ]
                    
                    if available_beds:
                        selected_bed = st.selectbox("Assign Bed", available_beds)
                    else:
                        st.warning(f"No available beds in {department}")
                        selected_bed = None
                    
                    attending_doctor = st.text_input("Attending Doctor")
                    diagnosis = st.text_input("Primary Diagnosis")
                
                medical_history = st.text_area("Medical History")
                admission_notes = st.text_area("Admission Notes")
                
                if st.form_submit_button("Admit Patient"):
                    if patient_id and patient_name and selected_bed:
                        bed_number = selected_bed.split(' (')[0]
                        
                        admission_data = {
                            'patient_id': patient_id,
                            'patient_name': patient_name,
                            'admission_date': str(admission_date),
                            'admission_time': str(admission_time),
                            'admission_type': admission_type,
                            'department': department,
                            'bed_number': bed_number,
                            'attending_doctor': attending_doctor,
                            'diagnosis': diagnosis,
                            'medical_history': medical_history,
                            'admission_notes': admission_notes,
                            'status': 'Admitted',
                            'created_at': datetime.now().isoformat()
                        }
                        
                        # Save admission
                        admissions = self._load_data(self.admissions_file)
                        admission_id = f"ADM_{len(admissions) + 1:04d}"
                        admissions[admission_id] = admission_data
                        self._save_data(self.admissions_file, admissions)
                        
                        # Update bed status
                        self._update_bed_status(bed_number, 'Occupied', patient_name, patient_id)
                        
                        st.success(f"Patient {patient_name} admitted successfully! Admission ID: {admission_id}")
                        st.rerun()
                    else:
                        st.error("Please fill in all required fields and select an available bed.")
        
        # Current admissions
        admissions = self._load_data(self.admissions_file)
        current_admissions = {
            adm_id: adm for adm_id, adm in admissions.items()
            if adm.get('status') == 'Admitted'
        }
        
        if current_admissions:
            st.markdown("#### Current Admissions")
            
            for adm_id, admission in current_admissions.items():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="background: rgba(0, 255, 136, 0.1); border: 2px solid rgba(0, 255, 136, 0.3); 
                                border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <strong>{admission['patient_name']}</strong> (ID: {admission['patient_id']})<br>
                        <strong>Bed:</strong> {admission.get('bed_number', 'N/A')}<br>
                        <strong>Department:</strong> {admission['department']}<br>
                        <strong>Doctor:</strong> {admission.get('attending_doctor', 'N/A')}<br>
                        <strong>Admitted:</strong> {admission['admission_date']}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("🔄 Transfer", key=f"transfer_{adm_id}"):
                        st.session_state[f"transfer_{adm_id}"] = True
                
                with col3:
                    if st.button("📤 Discharge", key=f"discharge_{adm_id}"):
                        self._discharge_patient(adm_id, admission)
                        st.rerun()
        else:
            st.info("No current admissions.")
    
    def _manage_transfers(self):
        """Manage patient transfers"""
        st.markdown("### ↔️ Patient Transfers")
        
        # Transfer form
        with st.expander("↔️ Transfer Patient"):
            admissions = self._load_data(self.admissions_file)
            current_patients = [
                f"{adm['patient_name']} (ID: {adm['patient_id']}) - Bed {adm.get('bed_number', 'N/A')}"
                for adm in admissions.values()
                if adm.get('status') == 'Admitted'
            ]
            
            if current_patients:
                selected_patient = st.selectbox("Select Patient to Transfer", current_patients)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    new_department = st.selectbox("Transfer to Department", [
                        "Emergency", "ICU", "General Surgery", "Cardiology", 
                        "Pediatrics", "Maternity", "Orthopedics"
                    ])
                    
                    # Get available beds in new department
                    beds = self._load_data(self.beds_file)
                    available_beds = [
                        f"{bed['bed_number']} ({bed['room_number']})"
                        for bed in beds.values()
                        if bed.get('department') == new_department and bed.get('status') == 'Available'
                    ]
                    
                    if available_beds:
                        new_bed = st.selectbox("New Bed", available_beds)
                    else:
                        st.warning(f"No available beds in {new_department}")
                        new_bed = None
                
                with col2:
                    transfer_reason = st.text_area("Transfer Reason")
                    new_doctor = st.text_input("New Attending Doctor")
                    transfer_date = st.date_input("Transfer Date", datetime.now().date())
                
                if st.button("Transfer Patient") and new_bed:
                    patient_id = selected_patient.split('ID: ')[1].split(')')[0]
                    self._process_transfer(patient_id, new_department, new_bed.split(' (')[0], 
                                        transfer_reason, new_doctor, str(transfer_date))
                    st.success("Patient transferred successfully!")
                    st.rerun()
            else:
                st.info("No patients available for transfer.")
        
        # Transfer history
        transfers = self._load_data(self.transfers_file)
        
        if transfers:
            st.markdown("#### Recent Transfers")
            
            for transfer_id, transfer in list(transfers.items())[-5:]:
                st.markdown(f"""
                <div style="background: rgba(0, 204, 255, 0.1); border: 2px solid rgba(0, 204, 255, 0.3); 
                            border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <strong>{transfer['patient_name']}</strong><br>
                    <strong>From:</strong> {transfer['from_department']} (Bed {transfer['from_bed']})<br>
                    <strong>To:</strong> {transfer['to_department']} (Bed {transfer['to_bed']})<br>
                    <strong>Date:</strong> {transfer['transfer_date']}<br>
                    <strong>Reason:</strong> {transfer.get('reason', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No transfer history.")
    
    def _manage_rooms(self):
        """Manage rooms and bed configuration"""
        st.markdown("### ⚙️ Room Management")
        
        # Add new room
        with st.expander("➕ Add New Room"):
            with st.form("add_room"):
                col1, col2 = st.columns(2)
                
                with col1:
                    room_number = st.text_input("Room Number")
                    room_type = st.selectbox("Room Type", [
                        "General Ward", "Private Room", "ICU", "Emergency", 
                        "Operating Room", "Recovery Room"
                    ])
                    department = st.selectbox("Department", [
                        "Emergency", "ICU", "General Surgery", "Cardiology", 
                        "Pediatrics", "Maternity", "Orthopedics"
                    ])
                    bed_count = st.number_input("Number of Beds", min_value=1, max_value=10, value=1)
                
                with col2:
                    floor = st.number_input("Floor", min_value=1, max_value=20, value=1)
                    wing = st.text_input("Wing/Section")
                    equipment = st.text_area("Available Equipment")
                    notes = st.text_area("Room Notes")
                
                if st.form_submit_button("Add Room"):
                    if room_number:
                        # Create room
                        room_data = {
                            'room_number': room_number,
                            'room_type': room_type,
                            'department': department,
                            'bed_count': bed_count,
                            'floor': floor,
                            'wing': wing,
                            'equipment': equipment,
                            'notes': notes,
                            'status': 'Active',
                            'created_date': datetime.now().strftime("%Y-%m-%d")
                        }
                        
                        rooms = self._load_data(self.rooms_file)
                        rooms[room_number] = room_data
                        self._save_data(self.rooms_file, rooms)
                        
                        # Create beds for the room
                        self._create_beds_for_room(room_number, bed_count, department, room_type)
                        
                        st.success(f"Room {room_number} added with {bed_count} beds!")
                        st.rerun()
        
        # Display rooms
        rooms = self._load_data(self.rooms_file)
        
        if rooms:
            st.markdown("#### Room Directory")
            
            for room_number, room in rooms.items():
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); border: 2px solid rgba(0, 255, 136, 0.3); 
                            border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <strong>Room {room_number}</strong> ({room['room_type']})<br>
                    <strong>Department:</strong> {room['department']}<br>
                    <strong>Floor:</strong> {room.get('floor', 'N/A')} | <strong>Wing:</strong> {room.get('wing', 'N/A')}<br>
                    <strong>Beds:</strong> {room['bed_count']}<br>
                    {f"<strong>Equipment:</strong> {room.get('equipment', 'N/A')}" if room.get('equipment') else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No rooms configured.")
    
    def _initialize_default_beds(self) -> Dict:
        """Initialize default beds for demonstration"""
        default_beds = {}
        
        # Emergency Department
        for i in range(1, 11):
            bed_id = f"ER_{i:02d}"
            default_beds[bed_id] = {
                'bed_number': f"ER-{i:02d}",
                'room_number': f"ER-{i:02d}",
                'department': 'Emergency',
                'bed_type': 'Emergency',
                'status': 'Available',
                'patient_name': None,
                'patient_id': None
            }
        
        # ICU
        for i in range(1, 11):
            bed_id = f"ICU_{i:02d}"
            default_beds[bed_id] = {
                'bed_number': f"ICU-{i:02d}",
                'room_number': f"ICU-{i:02d}",
                'department': 'ICU',
                'bed_type': 'ICU',
                'status': 'Available',
                'patient_name': None,
                'patient_id': None
            }
        
        # General Ward
        for i in range(1, 21):
            bed_id = f"GW_{i:02d}"
            default_beds[bed_id] = {
                'bed_number': f"GW-{i:02d}",
                'room_number': f"GW-{(i-1)//2 + 1:02d}",
                'department': 'General Surgery',
                'bed_type': 'General',
                'status': 'Available',
                'patient_name': None,
                'patient_id': None
            }
        
        return default_beds
    
    def _create_beds_for_room(self, room_number: str, bed_count: int, department: str, room_type: str):
        """Create beds for a new room"""
        beds = self._load_data(self.beds_file)
        
        for i in range(1, bed_count + 1):
            bed_id = f"{room_number}_BED_{i}"
            bed_number = f"{room_number}-{i:02d}"
            
            beds[bed_id] = {
                'bed_number': bed_number,
                'room_number': room_number,
                'department': department,
                'bed_type': room_type,
                'status': 'Available',
                'patient_name': None,
                'patient_id': None,
                'created_date': datetime.now().strftime("%Y-%m-%d")
            }
        
        self._save_data(self.beds_file, beds)
    
    def _update_bed_status(self, bed_number: str, status: str, patient_name: str = None, patient_id: str = None):
        """Update bed status"""
        beds = self._load_data(self.beds_file)
        
        for bed_id, bed in beds.items():
            if bed['bed_number'] == bed_number:
                bed['status'] = status
                bed['patient_name'] = patient_name
                bed['patient_id'] = patient_id
                bed['last_updated'] = datetime.now().isoformat()
                break
        
        self._save_data(self.beds_file, beds)
    
    def _discharge_patient(self, admission_id: str, admission_data: Dict):
        """Discharge a patient"""
        # Update admission status
        admissions = self._load_data(self.admissions_file)
        admissions[admission_id]['status'] = 'Discharged'
        admissions[admission_id]['discharge_date'] = datetime.now().strftime("%Y-%m-%d")
        self._save_data(self.admissions_file, admissions)
        
        # Free up the bed
        bed_number = admission_data.get('bed_number')
        if bed_number:
            self._update_bed_status(bed_number, 'Available')
    
    def _process_transfer(self, patient_id: str, new_department: str, new_bed: str, 
                         reason: str, new_doctor: str, transfer_date: str):
        """Process patient transfer"""
        # Get current admission
        admissions = self._load_data(self.admissions_file)
        
        for adm_id, admission in admissions.items():
            if admission['patient_id'] == patient_id and admission['status'] == 'Admitted':
                old_bed = admission.get('bed_number')
                old_department = admission['department']
                
                # Update admission
                admission['department'] = new_department
                admission['bed_number'] = new_bed
                admission['attending_doctor'] = new_doctor
                
                # Free old bed
                if old_bed:
                    self._update_bed_status(old_bed, 'Available')
                
                # Occupy new bed
                self._update_bed_status(new_bed, 'Occupied', admission['patient_name'], patient_id)
                
                # Record transfer
                transfers = self._load_data(self.transfers_file)
                transfer_id = f"TRF_{len(transfers) + 1:04d}"
                
                transfer_data = {
                    'patient_id': patient_id,
                    'patient_name': admission['patient_name'],
                    'from_department': old_department,
                    'from_bed': old_bed,
                    'to_department': new_department,
                    'to_bed': new_bed,
                    'reason': reason,
                    'new_doctor': new_doctor,
                    'transfer_date': transfer_date,
                    'created_at': datetime.now().isoformat()
                }
                
                transfers[transfer_id] = transfer_data
                self._save_data(self.transfers_file, transfers)
                break
        
        self._save_data(self.admissions_file, admissions)
    
    def _load_data(self, filename: str) -> Dict:
        """Load data from JSON file"""
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_data(self, filename: str, data: Dict):
        """Save data to JSON file"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)