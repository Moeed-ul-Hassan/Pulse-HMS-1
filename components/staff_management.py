import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
import json
import os

class StaffManagementSystem:
    """Complete staff and human resources management"""
    
    def __init__(self):
        self.staff_file = "data/staff.json"
        self.shifts_file = "data/shifts.json"
        self.attendance_file = "data/attendance.json"
        self.payroll_file = "data/payroll.json"
    
    def display_staff_dashboard(self):
        """Main staff management dashboard"""
        st.markdown("## 👥 Staff Management System")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Dashboard", "👤 Staff Directory", "📅 Shift Scheduling", 
            "⏰ Attendance", "💰 Payroll"
        ])
        
        with tab1:
            self._display_staff_overview()
        
        with tab2:
            self._manage_staff_directory()
        
        with tab3:
            self._manage_shift_scheduling()
        
        with tab4:
            self._manage_attendance()
        
        with tab5:
            self._manage_payroll()
    
    def _display_staff_overview(self):
        """Display staff overview dashboard"""
        st.markdown("### 👥 Staff Overview")
        
        staff = self._load_data(self.staff_file)
        attendance = self._load_data(self.attendance_file)
        
        # Calculate metrics
        total_staff = len(staff)
        active_staff = sum(1 for s in staff.values() if s.get('status') == 'Active')
        doctors = sum(1 for s in staff.values() if s.get('role') == 'Doctor')
        nurses = sum(1 for s in staff.values() if s.get('role') == 'Nurse')
        
        # Today's attendance
        today = datetime.now().strftime("%Y-%m-%d")
        present_today = sum(
            1 for a in attendance.values() 
            if a.get('date') == today and a.get('status') == 'Present'
        )
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Staff", total_staff, delta="+5 this month")
        
        with col2:
            st.metric("Active Staff", active_staff, delta="0")
        
        with col3:
            st.metric("Present Today", present_today, delta=f"{present_today - 2}")
        
        with col4:
            attendance_rate = (present_today / active_staff * 100) if active_staff > 0 else 0
            st.metric("Attendance Rate", f"{attendance_rate:.1f}%", delta="+2.5%")
        
        # Department distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Staff by Department")
            departments = {}
            for staff_member in staff.values():
                dept = staff_member.get('department', 'Unknown')
                departments[dept] = departments.get(dept, 0) + 1
            
            if departments:
                import plotly.express as px
                fig = px.pie(values=list(departments.values()), names=list(departments.keys()))
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Staff by Role")
            roles = {}
            for staff_member in staff.values():
                role = staff_member.get('role', 'Unknown')
                roles[role] = roles.get(role, 0) + 1
            
            if roles:
                fig = px.bar(x=list(roles.keys()), y=list(roles.values()))
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def _manage_staff_directory(self):
        """Manage staff directory"""
        st.markdown("### 👤 Staff Directory")
        
        # Add new staff member
        with st.expander("➕ Add New Staff Member"):
            with st.form("add_staff"):
                col1, col2 = st.columns(2)
                
                with col1:
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    employee_id = st.text_input("Employee ID")
                    role = st.selectbox("Role", [
                        "Doctor", "Nurse", "Technician", "Administrator", 
                        "Pharmacist", "Therapist", "Security", "Maintenance"
                    ])
                    department = st.selectbox("Department", [
                        "Emergency", "ICU", "Surgery", "Cardiology", "Pediatrics",
                        "Radiology", "Laboratory", "Pharmacy", "Administration"
                    ])
                
                with col2:
                    phone = st.text_input("Phone Number")
                    email = st.text_input("Email")
                    address = st.text_area("Address")
                    hire_date = st.date_input("Hire Date")
                    salary = st.number_input("Monthly Salary ($)", min_value=0.0, value=0.0, format="%.2f")
                
                specialization = st.text_input("Specialization/Certification")
                emergency_contact = st.text_input("Emergency Contact")
                
                if st.form_submit_button("Add Staff Member"):
                    if first_name and last_name and employee_id:
                        staff_data = {
                            'first_name': first_name,
                            'last_name': last_name,
                            'full_name': f"{first_name} {last_name}",
                            'employee_id': employee_id,
                            'role': role,
                            'department': department,
                            'phone': phone,
                            'email': email,
                            'address': address,
                            'hire_date': str(hire_date),
                            'salary': salary,
                            'specialization': specialization,
                            'emergency_contact': emergency_contact,
                            'status': 'Active',
                            'created_date': datetime.now().strftime("%Y-%m-%d")
                        }
                        
                        staff = self._load_data(self.staff_file)
                        staff_id = f"STF_{len(staff) + 1:04d}"
                        staff[staff_id] = staff_data
                        self._save_data(self.staff_file, staff_data)
                        
                        st.success(f"Staff member {first_name} {last_name} added successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill in required fields.")
        
        # Display staff directory
        staff = self._load_data(self.staff_file)
        
        if staff:
            st.markdown("#### Staff Directory")
            
            # Search functionality
            search_term = st.text_input("🔍 Search staff members...")
            department_filter = st.selectbox("Filter by Department", 
                ["All"] + ["Emergency", "ICU", "Surgery", "Cardiology", "Pediatrics",
                          "Radiology", "Laboratory", "Pharmacy", "Administration"])
            
            # Filter staff
            filtered_staff = {}
            for staff_id, member in staff.items():
                name_match = (search_term.lower() in member.get('full_name', '').lower() or 
                            search_term.lower() in member.get('employee_id', '').lower())
                dept_match = (department_filter == "All" or 
                            member.get('department') == department_filter)
                
                if (not search_term or name_match) and dept_match:
                    filtered_staff[staff_id] = member
            
            # Display staff cards
            for staff_id, member in filtered_staff.items():
                status_color = '#00ff88' if member.get('status') == 'Active' else '#ff4444'
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.05); border-left: 4px solid {status_color}; 
                                padding: 15px; margin: 10px 0; border-radius: 5px;">
                        <strong>{member.get('full_name', 'N/A')}</strong> ({member.get('employee_id', 'N/A')})<br>
                        <strong>Role:</strong> {member.get('role', 'N/A')}<br>
                        <strong>Department:</strong> {member.get('department', 'N/A')}<br>
                        <strong>Phone:</strong> {member.get('phone', 'N/A')}<br>
                        <strong>Status:</strong> <span style="color: {status_color};">{member.get('status', 'Unknown')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("📝 Edit", key=f"edit_staff_{staff_id}"):
                        st.session_state[f"edit_staff_{staff_id}"] = True
                
                with col3:
                    if st.button("👁️ View", key=f"view_staff_{staff_id}"):
                        self._display_staff_details(member)
        else:
            st.info("No staff members in directory.")
    
    def _manage_shift_scheduling(self):
        """Manage shift scheduling"""
        st.markdown("### 📅 Shift Scheduling")
        
        # Create new shift
        with st.expander("➕ Schedule New Shift"):
            with st.form("schedule_shift"):
                col1, col2 = st.columns(2)
                
                with col1:
                    # Get staff list
                    staff = self._load_data(self.staff_file)
                    staff_options = [f"{s['full_name']} ({s['employee_id']})" 
                                   for s in staff.values() if s.get('status') == 'Active']
                    
                    selected_staff = st.selectbox("Select Staff Member", staff_options)
                    shift_date = st.date_input("Shift Date")
                    shift_type = st.selectbox("Shift Type", ["Day", "Evening", "Night", "On-Call"])
                
                with col2:
                    start_time = st.time_input("Start Time")
                    end_time = st.time_input("End Time")
                    department = st.selectbox("Department", [
                        "Emergency", "ICU", "Surgery", "General Ward", 
                        "Pharmacy", "Laboratory", "Administration"
                    ])
                
                notes = st.text_area("Shift Notes")
                
                if st.form_submit_button("Schedule Shift"):
                    if selected_staff:
                        employee_id = selected_staff.split('(')[1].split(')')[0]
                        
                        shift_data = {
                            'employee_id': employee_id,
                            'staff_name': selected_staff.split(' (')[0],
                            'shift_date': str(shift_date),
                            'shift_type': shift_type,
                            'start_time': str(start_time),
                            'end_time': str(end_time),
                            'department': department,
                            'notes': notes,
                            'status': 'Scheduled',
                            'created_at': datetime.now().isoformat()
                        }
                        
                        shifts = self._load_data(self.shifts_file)
                        shift_id = f"SHF_{len(shifts) + 1:04d}"
                        shifts[shift_id] = shift_data
                        self._save_data(self.shifts_file, shifts)
                        
                        st.success("Shift scheduled successfully!")
                        st.rerun()
        
        # Display upcoming shifts
        shifts = self._load_data(self.shifts_file)
        
        if shifts:
            st.markdown("#### Upcoming Shifts")
            
            # Filter shifts by date
            today = datetime.now().date()
            upcoming_shifts = {
                shift_id: shift for shift_id, shift in shifts.items()
                if datetime.strptime(shift['shift_date'], "%Y-%m-%d").date() >= today
            }
            
            # Sort by date
            sorted_shifts = sorted(upcoming_shifts.items(), 
                                 key=lambda x: x[1]['shift_date'])
            
            for shift_id, shift in sorted_shifts[:10]:  # Show next 10 shifts
                shift_color = {
                    'Day': '#00ff88',
                    'Evening': '#ffa500',
                    'Night': '#8A2BE2',
                    'On-Call': '#00ccff'
                }.get(shift['shift_type'], '#ffffff')
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); border-left: 4px solid {shift_color}; 
                            padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <strong>{shift['staff_name']}</strong> - {shift['shift_type']} Shift<br>
                    <strong>Date:</strong> {shift['shift_date']}<br>
                    <strong>Time:</strong> {shift['start_time']} - {shift['end_time']}<br>
                    <strong>Department:</strong> {shift['department']}<br>
                    {f"<strong>Notes:</strong> {shift['notes']}" if shift.get('notes') else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No shifts scheduled.")
    
    def _manage_attendance(self):
        """Manage staff attendance"""
        st.markdown("### ⏰ Attendance Management")
        
        # Mark attendance
        with st.expander("✅ Mark Attendance"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Get staff list
                staff = self._load_data(self.staff_file)
                staff_options = [f"{s['full_name']} ({s['employee_id']})" 
                               for s in staff.values() if s.get('status') == 'Active']
                
                selected_staff = st.selectbox("Select Staff Member", staff_options, key="attendance_staff")
                attendance_date = st.date_input("Date", datetime.now().date())
                status = st.selectbox("Status", ["Present", "Absent", "Late", "Half Day", "Leave"])
            
            with col2:
                check_in_time = st.time_input("Check-in Time", datetime.now().time())
                check_out_time = st.time_input("Check-out Time")
                notes = st.text_area("Notes")
            
            if st.button("Mark Attendance"):
                if selected_staff:
                    employee_id = selected_staff.split('(')[1].split(')')[0]
                    
                    attendance_data = {
                        'employee_id': employee_id,
                        'staff_name': selected_staff.split(' (')[0],
                        'date': str(attendance_date),
                        'status': status,
                        'check_in_time': str(check_in_time),
                        'check_out_time': str(check_out_time),
                        'notes': notes,
                        'marked_at': datetime.now().isoformat()
                    }
                    
                    attendance = self._load_data(self.attendance_file)
                    attendance_id = f"ATT_{len(attendance) + 1:04d}"
                    attendance[attendance_id] = attendance_data
                    self._save_data(self.attendance_file, attendance)
                    
                    st.success("Attendance marked successfully!")
                    st.rerun()
        
        # Display today's attendance
        st.markdown("#### Today's Attendance")
        
        attendance = self._load_data(self.attendance_file)
        today = datetime.now().strftime("%Y-%m-%d")
        
        today_attendance = {
            att_id: att for att_id, att in attendance.items()
            if att.get('date') == today
        }
        
        if today_attendance:
            for att_id, att in today_attendance.items():
                status_color = {
                    'Present': '#00ff88',
                    'Late': '#ffa500',
                    'Absent': '#ff4444',
                    'Half Day': '#00ccff',
                    'Leave': '#8A2BE2'
                }.get(att['status'], '#ffffff')
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); border-left: 4px solid {status_color}; 
                            padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <strong>{att['staff_name']}</strong><br>
                    <strong>Status:</strong> <span style="color: {status_color};">{att['status']}</span><br>
                    <strong>Check-in:</strong> {att.get('check_in_time', 'N/A')}<br>
                    <strong>Check-out:</strong> {att.get('check_out_time', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No attendance marked for today.")
    
    def _manage_payroll(self):
        """Manage staff payroll"""
        st.markdown("### 💰 Payroll Management")
        
        # Generate payroll
        with st.expander("💰 Generate Payroll"):
            col1, col2 = st.columns(2)
            
            with col1:
                payroll_month = st.selectbox("Month", [
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ])
                payroll_year = st.number_input("Year", min_value=2020, max_value=2030, 
                                             value=datetime.now().year)
            
            with col2:
                overtime_rate = st.number_input("Overtime Rate Multiplier", min_value=1.0, 
                                              max_value=3.0, value=1.5)
                deduction_rate = st.number_input("Deduction Rate (%)", min_value=0.0, 
                                               max_value=50.0, value=10.0)
            
            if st.button("Generate Monthly Payroll"):
                self._generate_monthly_payroll(payroll_month, payroll_year, 
                                             overtime_rate, deduction_rate)
        
        # Display recent payroll
        payroll = self._load_data(self.payroll_file)
        
        if payroll:
            st.markdown("#### Recent Payroll Records")
            
            for payroll_id, record in list(payroll.items())[-5:]:  # Last 5 records
                st.markdown(f"""
                <div style="background: rgba(0, 255, 136, 0.1); border: 2px solid rgba(0, 255, 136, 0.3); 
                            border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <strong>{record['staff_name']}</strong> - {record['month']} {record['year']}<br>
                    <strong>Basic Salary:</strong> ${record['basic_salary']:.2f}<br>
                    <strong>Overtime:</strong> ${record.get('overtime_pay', 0):.2f}<br>
                    <strong>Deductions:</strong> ${record.get('deductions', 0):.2f}<br>
                    <strong>Net Pay:</strong> ${record['net_pay']:.2f}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No payroll records found.")
    
    def _display_staff_details(self, staff_member: Dict):
        """Display detailed staff information"""
        st.markdown(f"#### Staff Details: {staff_member.get('full_name', 'N/A')}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Employee ID:** {staff_member.get('employee_id', 'N/A')}")
            st.write(f"**Role:** {staff_member.get('role', 'N/A')}")
            st.write(f"**Department:** {staff_member.get('department', 'N/A')}")
            st.write(f"**Phone:** {staff_member.get('phone', 'N/A')}")
            st.write(f"**Email:** {staff_member.get('email', 'N/A')}")
        
        with col2:
            st.write(f"**Hire Date:** {staff_member.get('hire_date', 'N/A')}")
            st.write(f"**Salary:** ${staff_member.get('salary', 0):.2f}")
            st.write(f"**Specialization:** {staff_member.get('specialization', 'N/A')}")
            st.write(f"**Status:** {staff_member.get('status', 'N/A')}")
            st.write(f"**Emergency Contact:** {staff_member.get('emergency_contact', 'N/A')}")
    
    def _generate_monthly_payroll(self, month: str, year: int, overtime_rate: float, deduction_rate: float):
        """Generate monthly payroll for all staff"""
        staff = self._load_data(self.staff_file)
        payroll = self._load_data(self.payroll_file)
        
        for staff_id, member in staff.items():
            if member.get('status') == 'Active':
                basic_salary = member.get('salary', 0)
                overtime_pay = 0  # Would be calculated based on shifts and hours
                deductions = basic_salary * (deduction_rate / 100)
                net_pay = basic_salary + overtime_pay - deductions
                
                payroll_data = {
                    'employee_id': member.get('employee_id'),
                    'staff_name': member.get('full_name'),
                    'month': month,
                    'year': year,
                    'basic_salary': basic_salary,
                    'overtime_pay': overtime_pay,
                    'deductions': deductions,
                    'net_pay': net_pay,
                    'generated_date': datetime.now().strftime("%Y-%m-%d")
                }
                
                payroll_id = f"PAY_{member.get('employee_id')}_{month}_{year}"
                payroll[payroll_id] = payroll_data
        
        self._save_data(self.payroll_file, payroll)
        st.success(f"Payroll generated for {month} {year}")
    
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