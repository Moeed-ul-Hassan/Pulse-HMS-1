import streamlit as st
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from datetime import datetime
import io
import os
from typing import Dict, List

class PDFReportGenerator:
    """Generate branded PDF reports for PulseAI"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for branding"""
        # PulseAI Header Style
        self.header_style = ParagraphStyle(
            'PulseAIHeader',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#00ff88'),
            spaceAfter=20,
            alignment=1  # Center alignment
        )
        
        # Subheader Style
        self.subheader_style = ParagraphStyle(
            'PulseAISubheader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#00ccff'),
            spaceAfter=12
        )
        
        # Patient Info Style
        self.info_style = ParagraphStyle(
            'PatientInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=6
        )
    
    def generate_patient_report(self, patient_data: Dict, risk_data: Dict) -> bytes:
        """Generate comprehensive patient report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                              topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        story = []
        
        # Header with branding
        story.append(self._create_header())
        story.append(Spacer(1, 20))
        
        # Patient Information Section
        story.append(Paragraph("PATIENT INFORMATION", self.subheader_style))
        story.append(self._create_patient_info_table(patient_data))
        story.append(Spacer(1, 20))
        
        # Risk Assessment Section
        story.append(Paragraph("CARDIOVASCULAR RISK ASSESSMENT", self.subheader_style))
        story.append(self._create_risk_assessment_table(risk_data))
        story.append(Spacer(1, 20))
        
        # Clinical Recommendations
        story.append(Paragraph("CLINICAL RECOMMENDATIONS", self.subheader_style))
        story.append(self._create_recommendations(risk_data))
        story.append(Spacer(1, 20))
        
        # Footer with branding
        story.append(self._create_footer())
        
        doc.build(story)
        pdf_data = buffer.getvalue()
        buffer.close()
        return pdf_data
    
    def _create_header(self):
        """Create branded header"""
        header_text = """
        <para align="center">
        <font color="#00ff88" size="24"><b>⚡ PULSEAI HOSPITAL MANAGEMENT SYSTEM ⚡</b></font><br/>
        <font color="#00ccff" size="12">Advanced Healthcare Analytics & Risk Assessment</font><br/>
        <font color="#666666" size="10">Generated on: {}</font>
        </para>
        """.format(datetime.now().strftime("%B %d, %Y at %I:%M %p"))
        
        return Paragraph(header_text, self.styles['Normal'])
    
    def _create_patient_info_table(self, patient_data: Dict):
        """Create patient information table"""
        data = [
            ['Patient Name', patient_data.get('name', 'N/A')],
            ['Patient ID', patient_data.get('id', 'N/A')],
            ['Age', f"{patient_data.get('age', 'N/A')} years"],
            ['Gender', patient_data.get('gender', 'N/A')],
            ['Assessment Date', patient_data.get('assessment_date', 'N/A')],
            ['Blood Pressure', f"{patient_data.get('systolic_bp', 'N/A')}/{patient_data.get('diastolic_bp', 'N/A')} mmHg"],
            ['Total Cholesterol', f"{patient_data.get('total_cholesterol', 'N/A')} mg/dL"],
            ['HDL Cholesterol', f"{patient_data.get('hdl_cholesterol', 'N/A')} mg/dL"],
            ['BMI', f"{patient_data.get('bmi', 'N/A')} kg/m²"],
            ['Smoking Status', 'Yes' if patient_data.get('smoking') else 'No'],
            ['Diabetes', 'Yes' if patient_data.get('diabetes') else 'No'],
            ['Physical Activity', patient_data.get('physical_activity', 'N/A')]
        ]
        
        table = Table(data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        return table
    
    def _create_risk_assessment_table(self, risk_data: Dict):
        """Create risk assessment results table"""
        risk_score = risk_data.get('risk_score', 0)
        risk_category = risk_data.get('risk_category', 'Unknown')
        
        # Risk level color coding
        risk_color = colors.green
        if risk_score > 20:
            risk_color = colors.red
        elif risk_score > 10:
            risk_color = colors.orange
        
        data = [
            ['Risk Assessment Method', 'Framingham Risk Score'],
            ['10-Year CVD Risk', f"{risk_score:.1f}%"],
            ['Risk Category', risk_category],
            ['Assessment Timestamp', risk_data.get('timestamp', 'N/A')],
            ['Risk Interpretation', self._get_risk_interpretation(risk_score)]
        ]
        
        table = Table(data, colWidths=[2.5*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (1, 1), (1, 1), risk_color),
            ('TEXTCOLOR', (1, 1), (1, 1), colors.white),
            ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
        ]))
        
        return table
    
    def _create_recommendations(self, risk_data: Dict):
        """Create clinical recommendations based on risk"""
        risk_score = risk_data.get('risk_score', 0)
        
        if risk_score < 10:
            recommendations = [
                "• Continue current lifestyle modifications",
                "• Annual cardiovascular risk reassessment",
                "• Maintain healthy diet and regular exercise",
                "• Monitor blood pressure and cholesterol levels"
            ]
        elif risk_score < 20:
            recommendations = [
                "• Consider statin therapy (discuss with physician)",
                "• Blood pressure control if hypertensive",
                "• Smoking cessation if applicable",
                "• Weight management and increased physical activity",
                "• Consider aspirin therapy (physician consultation required)"
            ]
        else:
            recommendations = [
                "• HIGH PRIORITY: Immediate physician consultation required",
                "• Strong consideration for statin therapy",
                "• Aggressive blood pressure management",
                "• Comprehensive lifestyle intervention",
                "• Consider cardiology referral",
                "• Frequent monitoring and follow-up required"
            ]
        
        rec_text = "<br/>".join(recommendations)
        return Paragraph(rec_text, self.info_style)
    
    def _create_footer(self):
        """Create branded footer"""
        footer_text = """
        <para align="center">
        <font color="#666666" size="8">
        ────────────────────────────────────────────────────────────────<br/>
        <b>⚡ Crafted by Moeed ul Hassan @The Legend ⚡</b><br/>
        PulseAI Hospital Management System - Advanced Healthcare Technology<br/>
        This report is for clinical decision support only. All diagnostic and treatment decisions must be made by qualified healthcare professionals.<br/>
        ────────────────────────────────────────────────────────────────
        </font>
        </para>
        """
        return Paragraph(footer_text, self.styles['Normal'])
    
    def _get_risk_interpretation(self, risk_score: float) -> str:
        """Get risk interpretation text"""
        if risk_score < 10:
            return "Low risk - Continue preventive measures"
        elif risk_score < 20:
            return "Moderate risk - Consider intervention"
        else:
            return "High risk - Requires immediate attention"
    
    def generate_analytics_report(self, analytics_data: Dict) -> bytes:
        """Generate hospital analytics report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        story = []
        
        # Header
        story.append(self._create_header())
        story.append(Spacer(1, 20))
        
        # Analytics Title
        story.append(Paragraph("HOSPITAL ANALYTICS DASHBOARD REPORT", self.subheader_style))
        story.append(Spacer(1, 20))
        
        # Summary Statistics
        total_patients = analytics_data.get('total_patients', 0)
        high_risk_patients = analytics_data.get('high_risk_patients', 0)
        
        summary_data = [
            ['Total Patients', str(total_patients)],
            ['High Risk Patients', str(high_risk_patients)],
            ['Risk Assessment Rate', f"{(high_risk_patients/total_patients*100):.1f}%" if total_patients > 0 else "0%"],
            ['Report Generated', datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        story.append(self._create_footer())
        
        doc.build(story)
        pdf_data = buffer.getvalue()
        buffer.close()
        return pdf_data