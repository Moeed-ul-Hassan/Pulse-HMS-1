import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import time
from typing import Dict, List

class VitalSignsMonitor:
    """Real-time vital signs monitoring system"""
    
    def __init__(self):
        self.vital_ranges = {
            'heart_rate': {'min': 60, 'max': 100, 'critical_low': 50, 'critical_high': 120},
            'blood_pressure_systolic': {'min': 90, 'max': 140, 'critical_low': 80, 'critical_high': 180},
            'blood_pressure_diastolic': {'min': 60, 'max': 90, 'critical_low': 50, 'critical_high': 110},
            'temperature': {'min': 36.1, 'max': 37.2, 'critical_low': 35.0, 'critical_high': 39.0},
            'oxygen_saturation': {'min': 95, 'max': 100, 'critical_low': 90, 'critical_high': 100},
            'respiratory_rate': {'min': 12, 'max': 20, 'critical_low': 8, 'critical_high': 30}
        }
    
    def generate_realistic_vitals(self, patient_risk_level: str = "normal") -> Dict:
        """Generate realistic vital signs based on patient risk level"""
        base_vitals = {
            'heart_rate': 75,
            'systolic_bp': 120,
            'diastolic_bp': 80,
            'temperature': 36.5,
            'oxygen_saturation': 98,
            'respiratory_rate': 16
        }
        
        # Adjust based on risk level
        if patient_risk_level == "high":
            variations = {
                'heart_rate': random.uniform(5, 15),
                'systolic_bp': random.uniform(10, 30),
                'diastolic_bp': random.uniform(5, 15),
                'temperature': random.uniform(0.2, 0.8),
                'oxygen_saturation': random.uniform(-3, 0),
                'respiratory_rate': random.uniform(2, 8)
            }
        elif patient_risk_level == "moderate":
            variations = {
                'heart_rate': random.uniform(3, 10),
                'systolic_bp': random.uniform(5, 20),
                'diastolic_bp': random.uniform(3, 10),
                'temperature': random.uniform(0.1, 0.4),
                'oxygen_saturation': random.uniform(-2, 0),
                'respiratory_rate': random.uniform(1, 4)
            }
        else:  # normal
            variations = {
                'heart_rate': random.uniform(-5, 5),
                'systolic_bp': random.uniform(-10, 10),
                'diastolic_bp': random.uniform(-5, 5),
                'temperature': random.uniform(-0.2, 0.2),
                'oxygen_saturation': random.uniform(-1, 2),
                'respiratory_rate': random.uniform(-2, 2)
            }
        
        # Apply variations
        current_vitals = {}
        for vital, base_value in base_vitals.items():
            current_vitals[vital] = base_value + variations.get(vital, 0)
        
        # Add timestamp
        current_vitals['timestamp'] = datetime.now()
        
        return current_vitals
    
    def create_realtime_monitor_dashboard(self, patient_data: Dict):
        """Create real-time monitoring dashboard"""
        st.markdown("### 📊 Real-Time Vital Signs Monitor")
        
        # Generate current vitals
        risk_level = self._determine_risk_level(patient_data)
        current_vitals = self.generate_realistic_vitals(risk_level)
        
        # Create metrics display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self._display_vital_metric("❤️ Heart Rate", 
                                     current_vitals['heart_rate'], 
                                     "bpm", 
                                     self.vital_ranges['heart_rate'])
            
            self._display_vital_metric("🌡️ Temperature", 
                                     current_vitals['temperature'], 
                                     "°C", 
                                     self.vital_ranges['temperature'])
        
        with col2:
            self._display_vital_metric("🩸 Blood Pressure", 
                                     f"{current_vitals['systolic_bp']:.0f}/{current_vitals['diastolic_bp']:.0f}", 
                                     "mmHg", 
                                     self.vital_ranges['blood_pressure_systolic'])
            
            self._display_vital_metric("💨 Respiratory Rate", 
                                     current_vitals['respiratory_rate'], 
                                     "breaths/min", 
                                     self.vital_ranges['respiratory_rate'])
        
        with col3:
            self._display_vital_metric("🫁 Oxygen Saturation", 
                                     current_vitals['oxygen_saturation'], 
                                     "%", 
                                     self.vital_ranges['oxygen_saturation'])
            
            # Overall status indicator
            overall_status = self._calculate_overall_status(current_vitals)
            status_color = {
                'Normal': '#00ff88',
                'Warning': '#ffa500', 
                'Critical': '#ff4444'
            }.get(overall_status, '#ffffff')
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); border: 2px solid {status_color}; 
                        border-radius: 10px; padding: 20px; text-align: center;">
                <h3 style="color: {status_color}; margin: 0;">Overall Status</h3>
                <h2 style="color: {status_color}; margin: 5px 0;">{overall_status}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Real-time charts
        st.markdown("### 📈 Vital Signs Trends")
        self._create_realtime_charts(current_vitals, patient_data)
        
        # Auto-refresh
        if st.button("🔄 Refresh Vitals", use_container_width=True):
            st.rerun()
        
        # Auto-refresh every 30 seconds
        st.markdown("""
        <script>
        setTimeout(function(){
            window.location.reload();
        }, 30000);
        </script>
        """, unsafe_allow_html=True)
    
    def _display_vital_metric(self, title: str, value, unit: str, normal_range: Dict):
        """Display individual vital sign metric"""
        # Determine status color
        if isinstance(value, str):  # For blood pressure display
            color = '#00ccff'
        else:
            if value < normal_range['critical_low'] or value > normal_range['critical_high']:
                color = '#ff4444'  # Critical
            elif value < normal_range['min'] or value > normal_range['max']:
                color = '#ffa500'  # Warning
            else:
                color = '#00ff88'  # Normal
        
        # Format value
        if isinstance(value, float):
            display_value = f"{value:.1f}"
        else:
            display_value = str(value)
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); border: 2px solid {color}; 
                    border-radius: 10px; padding: 15px; margin: 10px 0; text-align: center;">
            <h4 style="color: #ffffff; margin: 0; font-size: 14px;">{title}</h4>
            <h2 style="color: {color}; margin: 5px 0; font-size: 24px;">{display_value}</h2>
            <p style="color: #cccccc; margin: 0; font-size: 12px;">{unit}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def _create_realtime_charts(self, current_vitals: Dict, patient_data: Dict):
        """Create real-time trend charts"""
        # Generate historical data for demonstration
        times = [datetime.now() - timedelta(minutes=x*5) for x in range(12, 0, -1)]
        times.append(datetime.now())
        
        # Generate trending data
        hr_data = [75 + random.uniform(-8, 8) for _ in range(12)]
        hr_data.append(current_vitals['heart_rate'])
        
        bp_sys_data = [120 + random.uniform(-15, 15) for _ in range(12)]
        bp_sys_data.append(current_vitals['systolic_bp'])
        
        temp_data = [36.5 + random.uniform(-0.5, 0.5) for _ in range(12)]
        temp_data.append(current_vitals['temperature'])
        
        # Create charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Heart Rate Chart
            fig_hr = go.Figure()
            fig_hr.add_trace(go.Scatter(
                x=times, y=hr_data,
                mode='lines+markers',
                name='Heart Rate',
                line=dict(color='#ff6b6b', width=3),
                marker=dict(size=8)
            ))
            
            fig_hr.add_hline(y=60, line_dash="dash", line_color="green", annotation_text="Min Normal")
            fig_hr.add_hline(y=100, line_dash="dash", line_color="orange", annotation_text="Max Normal")
            
            fig_hr.update_layout(
                title="❤️ Heart Rate Trend",
                yaxis_title="BPM",
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_hr, use_container_width=True)
        
        with col2:
            # Blood Pressure Chart
            fig_bp = go.Figure()
            fig_bp.add_trace(go.Scatter(
                x=times, y=bp_sys_data,
                mode='lines+markers',
                name='Systolic BP',
                line=dict(color='#4ecdc4', width=3),
                marker=dict(size=8)
            ))
            
            fig_bp.add_hline(y=120, line_dash="dash", line_color="green", annotation_text="Normal")
            fig_bp.add_hline(y=140, line_dash="dash", line_color="orange", annotation_text="High")
            
            fig_bp.update_layout(
                title="🩸 Blood Pressure Trend",
                yaxis_title="mmHg",
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_bp, use_container_width=True)
    
    def _determine_risk_level(self, patient_data: Dict) -> str:
        """Determine patient risk level from their data"""
        age = patient_data.get('age', 30)
        has_diabetes = patient_data.get('diabetes', False)
        smoking = patient_data.get('smoking', False)
        
        risk_score = 0
        if age > 65:
            risk_score += 2
        elif age > 45:
            risk_score += 1
        
        if has_diabetes:
            risk_score += 2
        if smoking:
            risk_score += 1
        
        if risk_score >= 3:
            return "high"
        elif risk_score >= 1:
            return "moderate"
        else:
            return "normal"
    
    def _calculate_overall_status(self, vitals: Dict) -> str:
        """Calculate overall patient status"""
        critical_count = 0
        warning_count = 0
        
        checks = [
            ('heart_rate', vitals['heart_rate']),
            ('blood_pressure_systolic', vitals['systolic_bp']),
            ('temperature', vitals['temperature']),
            ('oxygen_saturation', vitals['oxygen_saturation']),
            ('respiratory_rate', vitals['respiratory_rate'])
        ]
        
        for vital_name, value in checks:
            ranges = self.vital_ranges[vital_name]
            if value < ranges['critical_low'] or value > ranges['critical_high']:
                critical_count += 1
            elif value < ranges['min'] or value > ranges['max']:
                warning_count += 1
        
        if critical_count > 0:
            return "Critical"
        elif warning_count > 1:
            return "Warning"
        else:
            return "Normal"