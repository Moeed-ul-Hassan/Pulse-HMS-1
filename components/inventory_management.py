import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
import json
import os

class InventoryManager:
    """Complete inventory management for hospital supplies and equipment"""
    
    def __init__(self):
        self.inventory_file = "data/inventory.json"
        self.equipment_file = "data/equipment.json"
        self.suppliers_file = "data/suppliers.json"
        self.orders_file = "data/purchase_orders.json"
    
    def display_inventory_dashboard(self):
        """Main inventory management dashboard"""
        st.markdown("## 📦 Inventory Management System")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Dashboard", "💊 Medical Supplies", "🏥 Equipment", 
            "📋 Purchase Orders", "👥 Suppliers"
        ])
        
        with tab1:
            self._display_inventory_dashboard()
        
        with tab2:
            self._manage_medical_supplies()
        
        with tab3:
            self._manage_equipment()
        
        with tab4:
            self._manage_purchase_orders()
        
        with tab5:
            self._manage_suppliers()
    
    def _display_inventory_dashboard(self):
        """Display inventory overview dashboard"""
        st.markdown("### 📊 Inventory Overview")
        
        # Load inventory data
        inventory = self._load_data(self.inventory_file)
        equipment = self._load_data(self.equipment_file)
        
        # Calculate metrics
        total_items = len(inventory)
        low_stock_items = sum(1 for item in inventory.values() if item.get('quantity', 0) < item.get('min_threshold', 10))
        expired_items = sum(1 for item in inventory.values() if self._is_expired(item.get('expiry_date')))
        equipment_count = len(equipment)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Items", total_items, delta="+15 this month")
        
        with col2:
            st.metric("Low Stock Alerts", low_stock_items, delta="-3")
        
        with col3:
            st.metric("Expired Items", expired_items, delta="0")
        
        with col4:
            st.metric("Equipment Units", equipment_count, delta="+2")
        
        # Low stock alerts
        if low_stock_items > 0:
            st.markdown("### 🚨 Low Stock Alerts")
            for item_id, item in inventory.items():
                if item.get('quantity', 0) < item.get('min_threshold', 10):
                    st.warning(f"⚠️ {item['name']}: {item['quantity']} units remaining (Min: {item['min_threshold']})")
        
        # Expiry alerts
        if expired_items > 0:
            st.markdown("### ⏰ Expiry Alerts")
            for item_id, item in inventory.items():
                if self._is_expired(item.get('expiry_date')):
                    st.error(f"❌ {item['name']}: Expired on {item['expiry_date']}")
    
    def _manage_medical_supplies(self):
        """Manage medical supplies inventory"""
        st.markdown("### 💊 Medical Supplies")
        
        # Add new supply form
        with st.expander("➕ Add New Medical Supply"):
            with st.form("add_supply"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Supply Name")
                    category = st.selectbox("Category", [
                        "Medications", "Surgical Supplies", "Laboratory", 
                        "Diagnostic", "Personal Protective Equipment", "Consumables"
                    ])
                    quantity = st.number_input("Quantity", min_value=0, value=0)
                    unit = st.selectbox("Unit", ["pieces", "boxes", "bottles", "vials", "kg", "liters"])
                
                with col2:
                    min_threshold = st.number_input("Minimum Threshold", min_value=1, value=10)
                    max_threshold = st.number_input("Maximum Threshold", min_value=1, value=100)
                    cost_per_unit = st.number_input("Cost per Unit ($)", min_value=0.0, value=0.0, format="%.2f")
                    expiry_date = st.date_input("Expiry Date")
                
                location = st.text_input("Storage Location")
                supplier = st.text_input("Supplier")
                notes = st.text_area("Notes")
                
                if st.form_submit_button("Add Supply"):
                    supply_data = {
                        'name': name,
                        'category': category,
                        'quantity': quantity,
                        'unit': unit,
                        'min_threshold': min_threshold,
                        'max_threshold': max_threshold,
                        'cost_per_unit': cost_per_unit,
                        'expiry_date': str(expiry_date),
                        'location': location,
                        'supplier': supplier,
                        'notes': notes,
                        'added_date': datetime.now().strftime("%Y-%m-%d"),
                        'last_updated': datetime.now().isoformat()
                    }
                    
                    inventory = self._load_data(self.inventory_file)
                    supply_id = f"SUP_{len(inventory) + 1:04d}"
                    inventory[supply_id] = supply_data
                    self._save_data(self.inventory_file, inventory)
                    
                    st.success("Medical supply added successfully!")
                    st.rerun()
        
        # Display existing supplies
        inventory = self._load_data(self.inventory_file)
        
        if inventory:
            st.markdown("#### Current Medical Supplies")
            
            # Search and filter
            search_term = st.text_input("🔍 Search supplies...")
            category_filter = st.selectbox("Filter by Category", 
                ["All"] + ["Medications", "Surgical Supplies", "Laboratory", 
                          "Diagnostic", "Personal Protective Equipment", "Consumables"])
            
            # Filter supplies
            filtered_supplies = {}
            for supply_id, supply in inventory.items():
                if search_term.lower() in supply['name'].lower() or not search_term:
                    if category_filter == "All" or supply['category'] == category_filter:
                        filtered_supplies[supply_id] = supply
            
            # Display supplies in cards
            for supply_id, supply in filtered_supplies.items():
                status_color = self._get_status_color(supply)
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.05); border-left: 4px solid {status_color}; 
                                padding: 15px; margin: 10px 0; border-radius: 5px;">
                        <strong>{supply['name']}</strong> ({supply['category']})<br>
                        <strong>Quantity:</strong> {supply['quantity']} {supply['unit']}<br>
                        <strong>Location:</strong> {supply.get('location', 'N/A')}<br>
                        <strong>Expiry:</strong> {supply.get('expiry_date', 'N/A')}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("📝 Edit", key=f"edit_{supply_id}"):
                        st.session_state[f"edit_supply_{supply_id}"] = True
                
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_{supply_id}"):
                        del inventory[supply_id]
                        self._save_data(self.inventory_file, inventory)
                        st.rerun()
        else:
            st.info("No medical supplies in inventory.")
    
    def _manage_equipment(self):
        """Manage medical equipment"""
        st.markdown("### 🏥 Medical Equipment")
        
        # Add new equipment form
        with st.expander("➕ Add New Equipment"):
            with st.form("add_equipment"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Equipment Name")
                    model = st.text_input("Model/Serial Number")
                    manufacturer = st.text_input("Manufacturer")
                    category = st.selectbox("Category", [
                        "Diagnostic", "Surgical", "Monitoring", "Laboratory", 
                        "Life Support", "Imaging", "Rehabilitation"
                    ])
                
                with col2:
                    purchase_date = st.date_input("Purchase Date")
                    warranty_expiry = st.date_input("Warranty Expiry")
                    cost = st.number_input("Purchase Cost ($)", min_value=0.0, value=0.0, format="%.2f")
                    status = st.selectbox("Status", ["Active", "Maintenance", "Out of Service", "Retired"])
                
                location = st.text_input("Current Location")
                maintenance_schedule = st.selectbox("Maintenance Schedule", 
                    ["Monthly", "Quarterly", "Semi-Annual", "Annual", "As Needed"])
                notes = st.text_area("Notes")
                
                if st.form_submit_button("Add Equipment"):
                    equipment_data = {
                        'name': name,
                        'model': model,
                        'manufacturer': manufacturer,
                        'category': category,
                        'purchase_date': str(purchase_date),
                        'warranty_expiry': str(warranty_expiry),
                        'cost': cost,
                        'status': status,
                        'location': location,
                        'maintenance_schedule': maintenance_schedule,
                        'notes': notes,
                        'added_date': datetime.now().strftime("%Y-%m-%d"),
                        'last_maintenance': None,
                        'next_maintenance': self._calculate_next_maintenance(maintenance_schedule)
                    }
                    
                    equipment = self._load_data(self.equipment_file)
                    equipment_id = f"EQP_{len(equipment) + 1:04d}"
                    equipment[equipment_id] = equipment_data
                    self._save_data(self.equipment_file, equipment)
                    
                    st.success("Equipment added successfully!")
                    st.rerun()
        
        # Display equipment
        equipment = self._load_data(self.equipment_file)
        
        if equipment:
            st.markdown("#### Medical Equipment Inventory")
            
            for equipment_id, item in equipment.items():
                status_color = {
                    'Active': '#00ff88',
                    'Maintenance': '#ffa500',
                    'Out of Service': '#ff4444',
                    'Retired': '#666666'
                }.get(item['status'], '#ffffff')
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); border-left: 4px solid {status_color}; 
                            padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <strong>{item['name']}</strong> ({item['model']})<br>
                    <strong>Manufacturer:</strong> {item['manufacturer']}<br>
                    <strong>Status:</strong> <span style="color: {status_color};">{item['status']}</span><br>
                    <strong>Location:</strong> {item.get('location', 'N/A')}<br>
                    <strong>Next Maintenance:</strong> {item.get('next_maintenance', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No equipment in inventory.")
    
    def _manage_purchase_orders(self):
        """Manage purchase orders"""
        st.markdown("### 📋 Purchase Orders")
        
        # Create new purchase order
        with st.expander("➕ Create New Purchase Order"):
            with st.form("create_po"):
                col1, col2 = st.columns(2)
                
                with col1:
                    supplier = st.text_input("Supplier")
                    order_date = st.date_input("Order Date", datetime.now().date())
                    expected_delivery = st.date_input("Expected Delivery")
                    priority = st.selectbox("Priority", ["Low", "Normal", "High", "Urgent"])
                
                with col2:
                    department = st.text_input("Requesting Department")
                    requested_by = st.text_input("Requested By")
                    approved_by = st.text_input("Approved By")
                    budget_code = st.text_input("Budget Code")
                
                # Order items
                st.markdown("#### Order Items")
                items = []
                
                # Simple item entry (in real system, this would be more sophisticated)
                item_name = st.text_input("Item Name")
                quantity = st.number_input("Quantity", min_value=1, value=1)
                unit_cost = st.number_input("Unit Cost ($)", min_value=0.0, value=0.0, format="%.2f")
                
                if st.form_submit_button("Create Purchase Order"):
                    if item_name and supplier:
                        po_data = {
                            'supplier': supplier,
                            'order_date': str(order_date),
                            'expected_delivery': str(expected_delivery),
                            'priority': priority,
                            'department': department,
                            'requested_by': requested_by,
                            'approved_by': approved_by,
                            'budget_code': budget_code,
                            'items': [{
                                'name': item_name,
                                'quantity': quantity,
                                'unit_cost': unit_cost,
                                'total_cost': quantity * unit_cost
                            }],
                            'total_amount': quantity * unit_cost,
                            'status': 'Pending',
                            'created_date': datetime.now().isoformat()
                        }
                        
                        orders = self._load_data(self.orders_file)
                        po_id = f"PO_{len(orders) + 1:04d}"
                        orders[po_id] = po_data
                        self._save_data(self.orders_file, orders)
                        
                        st.success(f"Purchase Order {po_id} created successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill in required fields.")
        
        # Display existing purchase orders
        orders = self._load_data(self.orders_file)
        
        if orders:
            st.markdown("#### Recent Purchase Orders")
            
            for po_id, order in orders.items():
                status_color = {
                    'Pending': '#ffa500',
                    'Approved': '#00ccff',
                    'Ordered': '#00ff88',
                    'Delivered': '#00ff88',
                    'Cancelled': '#ff4444'
                }.get(order['status'], '#ffffff')
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); border-left: 4px solid {status_color}; 
                            padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <strong>PO {po_id}</strong> - {order['supplier']}<br>
                    <strong>Amount:</strong> ${order['total_amount']:.2f}<br>
                    <strong>Status:</strong> <span style="color: {status_color};">{order['status']}</span><br>
                    <strong>Expected Delivery:</strong> {order['expected_delivery']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No purchase orders found.")
    
    def _manage_suppliers(self):
        """Manage supplier information"""
        st.markdown("### 👥 Supplier Management")
        
        # Add new supplier
        with st.expander("➕ Add New Supplier"):
            with st.form("add_supplier"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Supplier Name")
                    contact_person = st.text_input("Contact Person")
                    phone = st.text_input("Phone Number")
                    email = st.text_input("Email")
                
                with col2:
                    address = st.text_area("Address")
                    products = st.text_area("Products/Services")
                    payment_terms = st.text_input("Payment Terms")
                    rating = st.selectbox("Rating", ["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"])
                
                if st.form_submit_button("Add Supplier"):
                    supplier_data = {
                        'name': name,
                        'contact_person': contact_person,
                        'phone': phone,
                        'email': email,
                        'address': address,
                        'products': products,
                        'payment_terms': payment_terms,
                        'rating': rating,
                        'added_date': datetime.now().strftime("%Y-%m-%d"),
                        'status': 'Active'
                    }
                    
                    suppliers = self._load_data(self.suppliers_file)
                    supplier_id = f"SUP_{len(suppliers) + 1:04d}"
                    suppliers[supplier_id] = supplier_data
                    self._save_data(self.suppliers_file, suppliers)
                    
                    st.success("Supplier added successfully!")
                    st.rerun()
        
        # Display suppliers
        suppliers = self._load_data(self.suppliers_file)
        
        if suppliers:
            st.markdown("#### Registered Suppliers")
            
            for supplier_id, supplier in suppliers.items():
                st.markdown(f"""
                <div style="background: rgba(0, 255, 136, 0.1); border: 2px solid rgba(0, 255, 136, 0.3); 
                            border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <strong>{supplier['name']}</strong><br>
                    <strong>Contact:</strong> {supplier['contact_person']} ({supplier['phone']})<br>
                    <strong>Email:</strong> {supplier['email']}<br>
                    <strong>Products:</strong> {supplier.get('products', 'N/A')}<br>
                    <strong>Rating:</strong> {supplier.get('rating', 'Not Rated')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No suppliers registered.")
    
    def _is_expired(self, expiry_date_str: str) -> bool:
        """Check if item is expired"""
        if not expiry_date_str:
            return False
        try:
            expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
            return expiry_date < datetime.now().date()
        except:
            return False
    
    def _get_status_color(self, supply: Dict) -> str:
        """Get color based on supply status"""
        quantity = supply.get('quantity', 0)
        min_threshold = supply.get('min_threshold', 10)
        
        if self._is_expired(supply.get('expiry_date')):
            return '#ff4444'  # Red for expired
        elif quantity < min_threshold:
            return '#ffa500'  # Orange for low stock
        else:
            return '#00ff88'  # Green for normal
    
    def _calculate_next_maintenance(self, schedule: str) -> str:
        """Calculate next maintenance date"""
        now = datetime.now()
        
        if schedule == "Monthly":
            next_date = now + timedelta(days=30)
        elif schedule == "Quarterly":
            next_date = now + timedelta(days=90)
        elif schedule == "Semi-Annual":
            next_date = now + timedelta(days=180)
        elif schedule == "Annual":
            next_date = now + timedelta(days=365)
        else:
            return "As Needed"
        
        return next_date.strftime("%Y-%m-%d")
    
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