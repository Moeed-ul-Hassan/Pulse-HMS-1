import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
import json
import os

class BillingFinanceManager:
    """Complete billing and financial management system"""
    
    def __init__(self):
        self.bills_file = "data/bills.json"
        self.payments_file = "data/payments.json"
        self.insurance_file = "data/insurance.json"
        self.services_file = "data/services.json"
    
    def display_billing_dashboard(self):
        """Main billing and finance dashboard"""
        st.markdown("## 💰 Billing & Financial Management")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Dashboard", "🧾 Generate Bill", "💳 Payment Processing", 
            "🏥 Insurance Claims", "⚙️ Service Management"
        ])
        
        with tab1:
            self._display_financial_dashboard()
        
        with tab2:
            self._generate_patient_bill()
        
        with tab3:
            self._process_payments()
        
        with tab4:
            self._manage_insurance()
        
        with tab5:
            self._manage_services()
    
    def _display_financial_dashboard(self):
        """Display financial overview dashboard"""
        st.markdown("### 💰 Financial Overview")
        
        bills = self._load_data(self.bills_file)
        payments = self._load_data(self.payments_file)
        
        # Calculate financial metrics
        total_revenue = sum(bill.get('total_amount', 0) for bill in bills.values())
        total_paid = sum(payment.get('amount', 0) for payment in payments.values())
        outstanding = total_revenue - total_paid
        
        # This month's metrics
        current_month = datetime.now().strftime("%Y-%m")
        monthly_revenue = sum(
            bill.get('total_amount', 0) for bill in bills.values() 
            if bill.get('bill_date', '').startswith(current_month)
        )
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Revenue", f"${total_revenue:,.2f}", delta=f"+${monthly_revenue:,.2f} this month")
        
        with col2:
            st.metric("Payments Received", f"${total_paid:,.2f}", delta="+12.5%")
        
        with col3:
            st.metric("Outstanding Amount", f"${outstanding:,.2f}", delta="-8.3%")
        
        with col4:
            collection_rate = (total_paid / total_revenue * 100) if total_revenue > 0 else 0
            st.metric("Collection Rate", f"{collection_rate:.1f}%", delta="+2.1%")
        
        # Revenue trends
        st.markdown("### 📈 Revenue Trends")
        
        # Generate sample revenue data for last 6 months
        months = []
        revenues = []
        
        for i in range(6, 0, -1):
            month_date = datetime.now() - timedelta(days=i*30)
            months.append(month_date.strftime("%Y-%m"))
            # Calculate revenue for each month
            month_revenue = sum(
                bill.get('total_amount', 0) for bill in bills.values()
                if bill.get('bill_date', '').startswith(month_date.strftime("%Y-%m"))
            )
            revenues.append(month_revenue if month_revenue > 0 else 15000 + i * 2000)  # Sample data
        
        # Create revenue chart
        import plotly.express as px
        fig = px.line(x=months, y=revenues, title="Monthly Revenue Trend")
        fig.update_traces(line=dict(color='#00ff88', width=3), marker=dict(size=8))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Outstanding bills
        st.markdown("### 📋 Outstanding Bills")
        outstanding_bills = {
            bill_id: bill for bill_id, bill in bills.items() 
            if bill.get('status') in ['Pending', 'Partially Paid']
        }
        
        if outstanding_bills:
            for bill_id, bill in list(outstanding_bills.items())[:5]:  # Show first 5
                st.markdown(f"""
                <div style="background: rgba(255, 165, 0, 0.1); border: 2px solid rgba(255, 165, 0, 0.3); 
                            border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <strong>Bill #{bill_id}</strong> - {bill.get('patient_name', 'Unknown')}<br>
                    <strong>Amount:</strong> ${bill.get('total_amount', 0):.2f}<br>
                    <strong>Status:</strong> {bill.get('status', 'Unknown')}<br>
                    <strong>Due Date:</strong> {bill.get('due_date', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No outstanding bills!")
    
    def _generate_patient_bill(self):
        """Generate patient bills"""
        st.markdown("### 🧾 Generate Patient Bill")
        
        with st.form("generate_bill"):
            col1, col2 = st.columns(2)
            
            with col1:
                patient_id = st.text_input("Patient ID")
                patient_name = st.text_input("Patient Name")
                admission_date = st.date_input("Admission Date")
                discharge_date = st.date_input("Discharge Date")
            
            with col2:
                room_type = st.selectbox("Room Type", ["General Ward", "Private Room", "ICU", "Emergency"])
                doctor_name = st.text_input("Attending Doctor")
                insurance_provider = st.text_input("Insurance Provider (Optional)")
                insurance_id = st.text_input("Insurance ID (Optional)")
            
            st.markdown("#### Services & Charges")
            
            # Service selection
            services = self._load_data(self.services_file)
            if not services:
                # Initialize default services
                services = self._get_default_services()
                self._save_data(self.services_file, services)
            
            selected_services = []
            total_amount = 0
            
            # Room charges
            days_stayed = (discharge_date - admission_date).days
            room_charges = {
                "General Ward": 200,
                "Private Room": 400,
                "ICU": 800,
                "Emergency": 300
            }
            
            room_cost = room_charges.get(room_type, 200) * days_stayed
            total_amount += room_cost
            
            st.write(f"**Room Charges ({room_type}):** ${room_cost:.2f} ({days_stayed} days)")
            
            # Additional services
            st.markdown("**Additional Services:**")
            
            for service_id, service in services.items():
                if st.checkbox(f"{service['name']} - ${service['cost']:.2f}", key=f"service_{service_id}"):
                    quantity = st.number_input(f"Quantity for {service['name']}", 
                                             min_value=1, value=1, key=f"qty_{service_id}")
                    service_total = service['cost'] * quantity
                    selected_services.append({
                        'name': service['name'],
                        'cost': service['cost'],
                        'quantity': quantity,
                        'total': service_total
                    })
                    total_amount += service_total
            
            # Taxes and discounts
            tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, max_value=50.0, value=8.5) / 100
            discount = st.number_input("Discount ($)", min_value=0.0, value=0.0)
            
            tax_amount = total_amount * tax_rate
            final_amount = total_amount + tax_amount - discount
            
            st.markdown(f"**Subtotal:** ${total_amount:.2f}")
            st.markdown(f"**Tax:** ${tax_amount:.2f}")
            st.markdown(f"**Discount:** ${discount:.2f}")
            st.markdown(f"**Total Amount:** ${final_amount:.2f}")
            
            if st.form_submit_button("Generate Bill"):
                if patient_id and patient_name:
                    bill_data = {
                        'patient_id': patient_id,
                        'patient_name': patient_name,
                        'admission_date': str(admission_date),
                        'discharge_date': str(discharge_date),
                        'room_type': room_type,
                        'doctor_name': doctor_name,
                        'insurance_provider': insurance_provider,
                        'insurance_id': insurance_id,
                        'room_charges': room_cost,
                        'services': selected_services,
                        'subtotal': total_amount,
                        'tax_rate': tax_rate,
                        'tax_amount': tax_amount,
                        'discount': discount,
                        'total_amount': final_amount,
                        'bill_date': datetime.now().strftime("%Y-%m-%d"),
                        'due_date': (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                        'status': 'Pending',
                        'created_at': datetime.now().isoformat()
                    }
                    
                    bills = self._load_data(self.bills_file)
                    bill_id = f"BILL_{len(bills) + 1:04d}"
                    bills[bill_id] = bill_data
                    self._save_data(self.bills_file, bills)
                    
                    st.success(f"Bill {bill_id} generated successfully!")
                    
                    # Option to download bill
                    if st.button("📄 Download Bill PDF"):
                        self._generate_bill_pdf(bill_id, bill_data)
                else:
                    st.error("Please fill in patient ID and name.")
    
    def _process_payments(self):
        """Process patient payments"""
        st.markdown("### 💳 Payment Processing")
        
        # Payment form
        with st.expander("➕ Record New Payment"):
            with st.form("record_payment"):
                col1, col2 = st.columns(2)
                
                with col1:
                    # Get list of pending bills
                    bills = self._load_data(self.bills_file)
                    pending_bills = [
                        f"{bill_id} - {bill['patient_name']} (${bill['total_amount']:.2f})"
                        for bill_id, bill in bills.items()
                        if bill.get('status') in ['Pending', 'Partially Paid']
                    ]
                    
                    if pending_bills:
                        selected_bill = st.selectbox("Select Bill", pending_bills)
                        bill_id = selected_bill.split(' - ')[0]
                    else:
                        bill_id = st.text_input("Bill ID")
                    
                    payment_amount = st.number_input("Payment Amount ($)", min_value=0.0, value=0.0, format="%.2f")
                    payment_method = st.selectbox("Payment Method", [
                        "Cash", "Credit Card", "Debit Card", "Check", 
                        "Bank Transfer", "Insurance", "Online Payment"
                    ])
                
                with col2:
                    payment_date = st.date_input("Payment Date", datetime.now().date())
                    reference_number = st.text_input("Reference Number")
                    received_by = st.text_input("Received By")
                    notes = st.text_area("Notes")
                
                if st.form_submit_button("Record Payment"):
                    if bill_id and payment_amount > 0:
                        payment_data = {
                            'bill_id': bill_id,
                            'amount': payment_amount,
                            'payment_method': payment_method,
                            'payment_date': str(payment_date),
                            'reference_number': reference_number,
                            'received_by': received_by,
                            'notes': notes,
                            'recorded_at': datetime.now().isoformat()
                        }
                        
                        payments = self._load_data(self.payments_file)
                        payment_id = f"PAY_{len(payments) + 1:04d}"
                        payments[payment_id] = payment_data
                        self._save_data(self.payments_file, payments)
                        
                        # Update bill status
                        self._update_bill_status(bill_id, payment_amount)
                        
                        st.success(f"Payment {payment_id} recorded successfully!")
                        st.rerun()
                    else:
                        st.error("Please select a bill and enter payment amount.")
        
        # Recent payments
        payments = self._load_data(self.payments_file)
        
        if payments:
            st.markdown("#### Recent Payments")
            
            for payment_id, payment in list(payments.items())[-10:]:  # Last 10 payments
                st.markdown(f"""
                <div style="background: rgba(0, 255, 136, 0.1); border: 2px solid rgba(0, 255, 136, 0.3); 
                            border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <strong>Payment #{payment_id}</strong><br>
                    <strong>Bill:</strong> {payment['bill_id']}<br>
                    <strong>Amount:</strong> ${payment['amount']:.2f}<br>
                    <strong>Method:</strong> {payment['payment_method']}<br>
                    <strong>Date:</strong> {payment['payment_date']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No payments recorded yet.")
    
    def _manage_insurance(self):
        """Manage insurance claims"""
        st.markdown("### 🏥 Insurance Claims Management")
        
        # Create new insurance claim
        with st.expander("➕ Create New Insurance Claim"):
            with st.form("create_claim"):
                col1, col2 = st.columns(2)
                
                with col1:
                    patient_name = st.text_input("Patient Name")
                    insurance_provider = st.text_input("Insurance Provider")
                    policy_number = st.text_input("Policy Number")
                    claim_amount = st.number_input("Claim Amount ($)", min_value=0.0, value=0.0, format="%.2f")
                
                with col2:
                    treatment_date = st.date_input("Treatment Date")
                    diagnosis = st.text_input("Primary Diagnosis")
                    treatment_code = st.text_input("Treatment Code")
                    provider_id = st.text_input("Provider ID")
                
                claim_notes = st.text_area("Claim Notes")
                
                if st.form_submit_button("Submit Claim"):
                    claim_data = {
                        'patient_name': patient_name,
                        'insurance_provider': insurance_provider,
                        'policy_number': policy_number,
                        'claim_amount': claim_amount,
                        'treatment_date': str(treatment_date),
                        'diagnosis': diagnosis,
                        'treatment_code': treatment_code,
                        'provider_id': provider_id,
                        'notes': claim_notes,
                        'status': 'Submitted',
                        'submitted_date': datetime.now().strftime("%Y-%m-%d"),
                        'created_at': datetime.now().isoformat()
                    }
                    
                    claims = self._load_data(self.insurance_file)
                    claim_id = f"CLM_{len(claims) + 1:04d}"
                    claims[claim_id] = claim_data
                    self._save_data(self.insurance_file, claims)
                    
                    st.success(f"Insurance claim {claim_id} submitted successfully!")
                    st.rerun()
        
        # Display existing claims
        claims = self._load_data(self.insurance_file)
        
        if claims:
            st.markdown("#### Insurance Claims Status")
            
            for claim_id, claim in claims.items():
                status_color = {
                    'Submitted': '#00ccff',
                    'Under Review': '#ffa500',
                    'Approved': '#00ff88',
                    'Denied': '#ff4444',
                    'Paid': '#00ff88'
                }.get(claim['status'], '#ffffff')
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); border-left: 4px solid {status_color}; 
                            padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <strong>Claim #{claim_id}</strong> - {claim['patient_name']}<br>
                    <strong>Provider:</strong> {claim['insurance_provider']}<br>
                    <strong>Amount:</strong> ${claim['claim_amount']:.2f}<br>
                    <strong>Status:</strong> <span style="color: {status_color};">{claim['status']}</span><br>
                    <strong>Submitted:</strong> {claim['submitted_date']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No insurance claims submitted yet.")
    
    def _manage_services(self):
        """Manage hospital services and pricing"""
        st.markdown("### ⚙️ Service Management")
        
        # Add new service
        with st.expander("➕ Add New Service"):
            with st.form("add_service"):
                col1, col2 = st.columns(2)
                
                with col1:
                    service_name = st.text_input("Service Name")
                    service_code = st.text_input("Service Code")
                    category = st.selectbox("Category", [
                        "Consultation", "Diagnostic", "Laboratory", "Surgery", 
                        "Radiology", "Therapy", "Emergency", "Pharmacy"
                    ])
                    cost = st.number_input("Cost ($)", min_value=0.0, value=0.0, format="%.2f")
                
                with col2:
                    department = st.text_input("Department")
                    duration = st.text_input("Duration (minutes)")
                    description = st.text_area("Description")
                    active = st.checkbox("Active Service", value=True)
                
                if st.form_submit_button("Add Service"):
                    service_data = {
                        'name': service_name,
                        'code': service_code,
                        'category': category,
                        'cost': cost,
                        'department': department,
                        'duration': duration,
                        'description': description,
                        'active': active,
                        'created_date': datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    services = self._load_data(self.services_file)
                    service_id = f"SRV_{len(services) + 1:04d}"
                    services[service_id] = service_data
                    self._save_data(self.services_file, services)
                    
                    st.success("Service added successfully!")
                    st.rerun()
        
        # Display existing services
        services = self._load_data(self.services_file)
        
        if services:
            st.markdown("#### Hospital Services")
            
            # Filter by category
            categories = list(set(service['category'] for service in services.values()))
            selected_category = st.selectbox("Filter by Category", ["All"] + categories)
            
            filtered_services = {
                sid: service for sid, service in services.items()
                if selected_category == "All" or service['category'] == selected_category
            }
            
            for service_id, service in filtered_services.items():
                status_color = '#00ff88' if service.get('active', True) else '#666666'
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); border-left: 4px solid {status_color}; 
                            padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <strong>{service['name']}</strong> ({service.get('code', 'N/A')})<br>
                    <strong>Category:</strong> {service['category']}<br>
                    <strong>Cost:</strong> ${service['cost']:.2f}<br>
                    <strong>Department:</strong> {service.get('department', 'N/A')}<br>
                    <strong>Status:</strong> <span style="color: {status_color};">
                        {'Active' if service.get('active', True) else 'Inactive'}
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No services configured yet.")
    
    def _get_default_services(self) -> Dict:
        """Get default hospital services"""
        return {
            "SRV_0001": {
                "name": "General Consultation",
                "code": "CONS001",
                "category": "Consultation",
                "cost": 150.00,
                "department": "General Medicine",
                "duration": "30",
                "description": "General medical consultation",
                "active": True
            },
            "SRV_0002": {
                "name": "Blood Test - Complete",
                "code": "LAB001",
                "category": "Laboratory",
                "cost": 75.00,
                "department": "Laboratory",
                "duration": "15",
                "description": "Complete blood count and basic metabolic panel",
                "active": True
            },
            "SRV_0003": {
                "name": "X-Ray Chest",
                "code": "RAD001",
                "category": "Radiology",
                "cost": 200.00,
                "department": "Radiology",
                "duration": "20",
                "description": "Chest X-ray examination",
                "active": True
            },
            "SRV_0004": {
                "name": "ECG",
                "code": "DIAG001",
                "category": "Diagnostic",
                "cost": 100.00,
                "department": "Cardiology",
                "duration": "15",
                "description": "Electrocardiogram",
                "active": True
            }
        }
    
    def _update_bill_status(self, bill_id: str, payment_amount: float):
        """Update bill status based on payment"""
        bills = self._load_data(self.bills_file)
        
        if bill_id in bills:
            bill = bills[bill_id]
            current_paid = bill.get('paid_amount', 0)
            new_paid = current_paid + payment_amount
            total_amount = bill['total_amount']
            
            bill['paid_amount'] = new_paid
            
            if new_paid >= total_amount:
                bill['status'] = 'Paid'
            elif new_paid > 0:
                bill['status'] = 'Partially Paid'
            
            bills[bill_id] = bill
            self._save_data(self.bills_file, bills)
    
    def _generate_bill_pdf(self, bill_id: str, bill_data: Dict):
        """Generate PDF bill (placeholder)"""
        st.info("PDF generation feature would be implemented here using ReportLab")
    
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