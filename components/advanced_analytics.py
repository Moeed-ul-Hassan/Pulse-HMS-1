import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List
import json

class AdvancedAnalytics:
    """Advanced analytics and reporting for hospital data"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def display_analytics_dashboard(self):
        """Main analytics dashboard"""
        st.markdown("## 📊 Advanced Analytics & Intelligence")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Patient Analytics", "🏥 Operational Insights", 
            "💰 Financial Analytics", "🔮 Predictive Models"
        ])
        
        with tab1:
            self._display_patient_analytics()
        
        with tab2:
            self._display_operational_insights()
        
        with tab3:
            self._display_financial_analytics()
        
        with tab4:
            self._display_predictive_models()
    
    def _display_patient_analytics(self):
        """Display comprehensive patient analytics"""
        st.markdown("### 👥 Patient Demographics & Health Analytics")
        
        patients = self.data_manager.get_all_patients()
        
        if not patients:
            st.warning("No patient data available for analytics.")
            return
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(patients)
        
        # Age distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Age Distribution")
            age_bins = pd.cut(df['age'], bins=[0, 18, 35, 50, 65, 100], labels=['0-18', '19-35', '36-50', '51-65', '65+'])
            age_counts = age_bins.value_counts()
            
            fig = px.bar(x=age_counts.index, y=age_counts.values, 
                        title="Patient Age Groups",
                        color=age_counts.values,
                        color_continuous_scale="viridis")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Gender Distribution")
            gender_counts = df['gender'].value_counts()
            
            fig = px.pie(values=gender_counts.values, names=gender_counts.index,
                        title="Gender Distribution",
                        color_discrete_map={'Male': '#4CAF50', 'Female': '#FF9800', 'Other': '#9C27B0'})
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Health metrics analysis
        st.markdown("#### Health Metrics Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Blood Pressure Distribution**")
            bp_systolic = [p.get('systolic_bp', 120) for p in patients]
            fig = px.histogram(x=bp_systolic, nbins=20, title="Systolic BP Distribution")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Cholesterol Levels**")
            cholesterol = [p.get('total_cholesterol', 200) for p in patients]
            fig = px.box(y=cholesterol, title="Cholesterol Distribution")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.markdown("**Risk Score Distribution**")
            # Calculate risk scores for all patients
            risk_scores = []
            for patient in patients:
                # Simplified risk calculation for demo
                age_factor = patient.get('age', 30) * 0.5
                bp_factor = (patient.get('systolic_bp', 120) - 120) * 0.2
                chol_factor = (patient.get('total_cholesterol', 200) - 200) * 0.1
                risk_score = max(0, age_factor + bp_factor + chol_factor)
                risk_scores.append(risk_score)
            
            fig = px.histogram(x=risk_scores, nbins=15, title="Risk Score Distribution")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def _display_operational_insights(self):
        """Display operational analytics"""
        st.markdown("### 🏥 Operational Performance Insights")
        
        # Sample operational data - in real system this would come from actual operations
        operational_data = self._generate_sample_operational_data()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Department Utilization")
            dept_utilization = {
                'Emergency': 85,
                'ICU': 92,
                'Surgery': 78,
                'General Ward': 65,
                'Pediatrics': 70,
                'Maternity': 55
            }
            
            fig = px.bar(x=list(dept_utilization.keys()), y=list(dept_utilization.values()),
                        title="Department Utilization (%)",
                        color=list(dept_utilization.values()),
                        color_continuous_scale="RdYlGn_r")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Average Wait Times")
            wait_times = {
                'Emergency': 15,
                'Consultation': 25,
                'Laboratory': 30,
                'Radiology': 45,
                'Pharmacy': 10
            }
            
            fig = px.bar(x=list(wait_times.keys()), y=list(wait_times.values()),
                        title="Average Wait Times (minutes)",
                        color=list(wait_times.values()),
                        color_continuous_scale="Reds")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Patient flow analysis
        st.markdown("#### Patient Flow Trends")
        
        # Generate sample patient flow data
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        admissions = np.random.poisson(15, 30)  # Average 15 admissions per day
        discharges = np.random.poisson(14, 30)  # Average 14 discharges per day
        
        flow_df = pd.DataFrame({
            'Date': dates,
            'Admissions': admissions,
            'Discharges': discharges
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=flow_df['Date'], y=flow_df['Admissions'], 
                                mode='lines+markers', name='Admissions', line=dict(color='#00ff88')))
        fig.add_trace(go.Scatter(x=flow_df['Date'], y=flow_df['Discharges'], 
                                mode='lines+markers', name='Discharges', line=dict(color='#ff4444')))
        
        fig.update_layout(
            title="Daily Patient Flow (Last 30 Days)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def _display_financial_analytics(self):
        """Display financial analytics"""
        st.markdown("### 💰 Financial Performance Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Revenue by Department")
            revenue_data = {
                'Surgery': 45000,
                'Emergency': 35000,
                'ICU': 25000,
                'Radiology': 15000,
                'Laboratory': 12000,
                'Pharmacy': 8000
            }
            
            fig = px.pie(values=list(revenue_data.values()), names=list(revenue_data.keys()),
                        title="Monthly Revenue Distribution")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Cost Analysis")
            cost_data = {
                'Staff Salaries': 80000,
                'Medical Supplies': 25000,
                'Equipment': 15000,
                'Utilities': 8000,
                'Maintenance': 5000,
                'Other': 7000
            }
            
            fig = px.bar(x=list(cost_data.keys()), y=list(cost_data.values()),
                        title="Monthly Cost Breakdown",
                        color=list(cost_data.values()),
                        color_continuous_scale="Reds")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Financial trends
        st.markdown("#### Financial Trends")
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        revenue = [120000, 135000, 128000, 142000, 138000, 145000]
        expenses = [95000, 102000, 98000, 108000, 105000, 110000]
        profit = [r - e for r, e in zip(revenue, expenses)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=revenue, mode='lines+markers', 
                                name='Revenue', line=dict(color='#00ff88')))
        fig.add_trace(go.Scatter(x=months, y=expenses, mode='lines+markers', 
                                name='Expenses', line=dict(color='#ff4444')))
        fig.add_trace(go.Scatter(x=months, y=profit, mode='lines+markers', 
                                name='Profit', line=dict(color='#00ccff')))
        
        fig.update_layout(
            title="Financial Trends (6 Months)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def _display_predictive_models(self):
        """Display predictive analytics"""
        st.markdown("### 🔮 Predictive Analytics & AI Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Predicted Patient Admissions")
            
            # Generate prediction data
            future_dates = [datetime.now() + timedelta(days=x) for x in range(1, 8)]
            predicted_admissions = np.random.poisson(16, 7)  # Predicted admissions
            confidence_upper = predicted_admissions + np.random.poisson(3, 7)
            confidence_lower = np.maximum(0, predicted_admissions - np.random.poisson(3, 7))
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=future_dates, y=predicted_admissions,
                                    mode='lines+markers', name='Predicted',
                                    line=dict(color='#00ff88')))
            fig.add_trace(go.Scatter(x=future_dates, y=confidence_upper,
                                    fill=None, mode='lines', line_color='rgba(0,0,0,0)',
                                    showlegend=False))
            fig.add_trace(go.Scatter(x=future_dates, y=confidence_lower,
                                    fill='tonexty', mode='lines', line_color='rgba(0,0,0,0)',
                                    name='Confidence Interval', fillcolor='rgba(0,255,136,0.2)'))
            
            fig.update_layout(
                title="7-Day Admission Forecast",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Risk Score Predictions")
            
            # Sample risk prediction data
            risk_categories = ['Low Risk', 'Medium Risk', 'High Risk', 'Critical']
            current_patients = [45, 25, 15, 5]
            predicted_patients = [42, 28, 18, 7]
            
            x = np.arange(len(risk_categories))
            width = 0.35
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=risk_categories, y=current_patients, 
                                name='Current', marker_color='#00ccff'))
            fig.add_trace(go.Bar(x=risk_categories, y=predicted_patients, 
                                name='Predicted Next Month', marker_color='#ffa500'))
            
            fig.update_layout(
                title="Risk Category Trends",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                barmode='group'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # AI Insights
        st.markdown("#### 🤖 AI-Generated Insights")
        
        insights = [
            "📈 Emergency department utilization is trending 15% higher than normal - consider additional staffing",
            "💊 Medication inventory for antibiotics is projected to run low in 5 days",
            "🔍 Pattern detected: Higher admission rates on Mondays and Fridays",
            "⚠️ 12 patients identified as high-risk for readmission within 30 days",
            "💰 Revenue optimization opportunity: Increase surgical scheduling by 8% to maximize capacity"
        ]
        
        for insight in insights:
            st.markdown(f"""
            <div style="background: rgba(0, 255, 136, 0.1); border-left: 4px solid #00ff88; 
                        padding: 15px; margin: 10px 0; border-radius: 5px;">
                {insight}
            </div>
            """, unsafe_allow_html=True)
    
    def _generate_sample_operational_data(self):
        """Generate sample operational data for demonstration"""
        # This would be replaced with real data in production
        return {
            'departments': ['Emergency', 'ICU', 'Surgery', 'General Ward'],
            'utilization': [85, 92, 78, 65],
            'wait_times': [15, 25, 30, 45],
            'patient_satisfaction': [4.2, 4.5, 4.7, 4.1]
        }