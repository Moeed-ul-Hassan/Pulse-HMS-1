import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
from typing import Dict, List

def create_risk_gauge(risk_score: float, risk_category: str) -> go.Figure:
    """
    Create a risk gauge visualization.
    
    Args:
        risk_score: Risk score percentage
        risk_category: Risk category
        
    Returns:
        Plotly figure object
    """
    # Color mapping for risk categories
    color_map = {
        'Low': '#0B3D0B',
        'Moderate': '#FFA500',
        'High': '#FF4444'
    }
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "10-Year CVD Risk", 'font': {'size': 20}},
        delta = {'reference': 10, 'suffix': '%'},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color_map[risk_category]},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 10], 'color': '#C8E6C9'},
                {'range': [10, 20], 'color': '#FFE0B2'},
                {'range': [20, 100], 'color': '#FFCDD2'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': risk_score
            }
        }
    ))
    
    fig.update_layout(
        font = {'color': "#333333", 'family': "Arial"},
        height = 400,
        margin = dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_timeline_chart(assessments: List[Dict]) -> go.Figure:
    """
    Create a timeline chart showing risk score evolution.
    
    Args:
        assessments: List of assessment dictionaries
        
    Returns:
        Plotly figure object
    """
    # Sort assessments by date
    sorted_assessments = sorted(assessments, key=lambda x: x['timestamp'])
    
    dates = [datetime.fromisoformat(assessment['timestamp']).date() for assessment in sorted_assessments]
    risk_scores = [assessment['risk_score'] for assessment in sorted_assessments]
    risk_categories = [assessment['risk_category'] for assessment in sorted_assessments]
    
    # Color mapping
    color_map = {
        'Low': '#0B3D0B',
        'Moderate': '#FFA500',
        'High': '#FF4444'
    }
    
    colors = [color_map[category] for category in risk_categories]
    
    fig = go.Figure()
    
    # Add line plot
    fig.add_trace(go.Scatter(
        x=dates,
        y=risk_scores,
        mode='lines+markers',
        name='Risk Score',
        line=dict(color='#317873', width=3),
        marker=dict(color=colors, size=10, line=dict(width=2, color='white'))
    ))
    
    # Add risk zones
    fig.add_hline(y=10, line_dash="dash", line_color="orange", 
                  annotation_text="Moderate Risk Threshold")
    fig.add_hline(y=20, line_dash="dash", line_color="red", 
                  annotation_text="High Risk Threshold")
    
    fig.update_layout(
        title="Risk Score Timeline",
        xaxis_title="Assessment Date",
        yaxis_title="10-Year CVD Risk (%)",
        font=dict(family="Arial", size=12, color="#333333"),
        height=400,
        hovermode='x unified'
    )
    
    return fig

def create_risk_factors_chart(patient_data: Dict) -> go.Figure:
    """
    Create a chart showing risk factor contributions.
    
    Args:
        patient_data: Patient data dictionary
        
    Returns:
        Plotly figure object
    """
    # Calculate risk factor contributions
    factors = []
    values = []
    
    # Age factor
    if patient_data['age'] > 65:
        factors.append('Age')
        values.append(3)
    elif patient_data['age'] > 45:
        factors.append('Age')
        values.append(2)
    
    # Blood pressure
    if patient_data['systolic_bp'] > 140:
        factors.append('Hypertension')
        values.append(3)
    elif patient_data['systolic_bp'] > 130:
        factors.append('Elevated BP')
        values.append(2)
    
    # Cholesterol
    if patient_data['total_cholesterol'] > 240:
        factors.append('High Cholesterol')
        values.append(3)
    elif patient_data['total_cholesterol'] > 200:
        factors.append('Cholesterol')
        values.append(1)
    
    # HDL
    if patient_data['hdl_cholesterol'] < 40:
        factors.append('Low HDL')
        values.append(2)
    
    # Lifestyle factors
    if patient_data['smoking']:
        factors.append('Smoking')
        values.append(3)
    
    if patient_data['diabetes']:
        factors.append('Diabetes')
        values.append(3)
    
    # Additional factors
    if patient_data.get('family_history', False):
        factors.append('Family History')
        values.append(2)
    
    bmi = patient_data.get('bmi', 25)
    if bmi > 30:
        factors.append('Obesity')
        values.append(2)
    elif bmi > 25:
        factors.append('Overweight')
        values.append(1)
    
    if not factors:
        factors = ['No Major Risk Factors']
        values = [0]
    
    # Create color scale
    colors = ['#0B3D0B' if v == 0 else '#317873' if v == 1 else '#FFA500' if v == 2 else '#FF4444' for v in values]
    
    fig = go.Figure(data=[
        go.Bar(
            y=factors,
            x=values,
            orientation='h',
            marker_color=colors,
            text=[f'Impact: {v}' for v in values],
            textposition='inside'
        )
    ])
    
    fig.update_layout(
        title="Risk Factor Contributions",
        xaxis_title="Risk Impact Level",
        yaxis_title="Risk Factors",
        font=dict(family="Arial", size=12, color="#333333"),
        height=400,
        showlegend=False
    )
    
    return fig

def create_population_dashboard(assessments: List[Dict]) -> Dict:
    """
    Create population-level dashboard visualizations.
    
    Args:
        assessments: List of all assessments
        
    Returns:
        Dictionary containing multiple figures
    """
    if not assessments:
        return {}
    
    # Risk distribution pie chart
    risk_categories = [assessment['risk_category'] for assessment in assessments]
    risk_counts = pd.Series(risk_categories).value_counts()
    
    colors = ['#0B3D0B', '#FFA500', '#FF4444']
    
    fig_risk_dist = go.Figure(data=[go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        hole=0.3,
        marker_colors=colors
    )])
    
    fig_risk_dist.update_layout(
        title="Population Risk Distribution",
        font=dict(family="Arial", size=12, color="#333333"),
        height=400
    )
    
    # Age vs Risk scatter plot
    ages = [assessment['patient_data']['age'] for assessment in assessments]
    risk_scores = [assessment['risk_score'] for assessment in assessments]
    genders = [assessment['patient_data']['gender'] for assessment in assessments]
    
    fig_age_risk = px.scatter(
        x=ages,
        y=risk_scores,
        color=genders,
        title="Age vs Risk Score",
        labels={'x': 'Age (years)', 'y': '10-Year CVD Risk (%)'},
        color_discrete_map={'Male': '#317873', 'Female': '#0B3D0B'}
    )
    
    fig_age_risk.update_layout(
        font=dict(family="Arial", size=12, color="#333333"),
        height=400
    )
    
    return {
        'risk_distribution': fig_risk_dist,
        'age_risk_scatter': fig_age_risk
    }

def create_real_time_monitor(patient_data: Dict) -> go.Figure:
    """
    Create a real-time monitoring visualization for patient vitals.
    
    Args:
        patient_data: Patient data dictionary
        
    Returns:
        Plotly figure object
    """
    import numpy as np
    from datetime import datetime, timedelta
    
    # Generate simulated real-time data for demonstration
    time_points = []
    heart_rate = []
    blood_pressure_sys = []
    blood_pressure_dia = []
    
    base_time = datetime.now() - timedelta(minutes=10)
    base_hr = patient_data.get('vital_signs', {}).get('pulse_rate', 72)
    base_sys = patient_data.get('systolic_bp', 120)
    base_dia = patient_data.get('diastolic_bp', 80)
    
    for i in range(20):
        time_points.append(base_time + timedelta(seconds=30*i))
        # Add realistic variations
        heart_rate.append(base_hr + np.random.randint(-5, 15))
        blood_pressure_sys.append(base_sys + np.random.randint(-10, 10))
        blood_pressure_dia.append(base_dia + np.random.randint(-5, 5))
    
    # Create subplot with secondary y-axis
    fig = go.Figure()
    
    # Heart rate line
    fig.add_trace(go.Scatter(
        x=time_points,
        y=heart_rate,
        mode='lines+markers',
        name='Heart Rate (bpm)',
        line=dict(color='#FF4444', width=3),
        marker=dict(size=6)
    ))
    
    # Blood pressure lines
    fig.add_trace(go.Scatter(
        x=time_points,
        y=blood_pressure_sys,
        mode='lines+markers',
        name='Systolic BP (mmHg)',
        line=dict(color='#0B3D0B', width=2),
        marker=dict(size=4)
    ))
    
    fig.add_trace(go.Scatter(
        x=time_points,
        y=blood_pressure_dia,
        mode='lines+markers',
        name='Diastolic BP (mmHg)',
        line=dict(color='#317873', width=2),
        marker=dict(size=4)
    ))
    
    # Add reference lines for normal ranges
    fig.add_hline(y=60, line_dash="dash", line_color="gray", opacity=0.5, 
                  annotation_text="HR Lower Normal")
    fig.add_hline(y=100, line_dash="dash", line_color="gray", opacity=0.5, 
                  annotation_text="HR Upper Normal")
    
    fig.update_layout(
        title=f"Real-Time Vital Signs Monitor - {patient_data.get('name', 'Patient')}",
        xaxis_title="Time",
        yaxis_title="Value",
        font=dict(family="Arial", size=12, color="#333333"),
        height=400,
        hovermode='x unified',
        showlegend=True,
        legend=dict(x=0, y=1)
    )
    
    return fig
