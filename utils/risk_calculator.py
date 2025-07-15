import numpy as np
import math
from typing import Dict, List, Tuple

class FraminghamRiskCalculator:
    """
    Cardiovascular risk calculator based on Framingham Risk Score
    and other validated clinical algorithms.
    """
    
    def __init__(self):
        # Framingham risk coefficients
        self.male_coefficients = {
            'age': 0.04826,
            'total_cholesterol': 0.00340,
            'hdl_cholesterol': -0.00832,
            'systolic_bp_treated': 0.00764,
            'systolic_bp_untreated': 0.00889,
            'smoking': 0.5180,
            'diabetes': 0.4555
        }
        
        self.female_coefficients = {
            'age': 0.07689,
            'total_cholesterol': 0.00268,
            'hdl_cholesterol': -0.00818,
            'systolic_bp_treated': 0.00481,
            'systolic_bp_untreated': 0.00645,
            'smoking': 0.5865,
            'diabetes': 0.3842
        }
    
    def calculate_framingham_risk(self, patient_data: Dict) -> float:
        """
        Calculate 10-year cardiovascular risk using Framingham Risk Score.
        
        Args:
            patient_data: Dictionary containing patient information
            
        Returns:
            10-year CVD risk percentage
        """
        coefficients = self.male_coefficients if patient_data['gender'] == 'Male' else self.female_coefficients
        
        # Calculate risk score
        risk_score = 0
        
        # Age contribution
        risk_score += coefficients['age'] * patient_data['age']
        
        # Cholesterol contribution
        risk_score += coefficients['total_cholesterol'] * patient_data['total_cholesterol']
        risk_score += coefficients['hdl_cholesterol'] * patient_data['hdl_cholesterol']
        
        # Blood pressure contribution
        if patient_data['hypertension_treatment']:
            risk_score += coefficients['systolic_bp_treated'] * patient_data['systolic_bp']
        else:
            risk_score += coefficients['systolic_bp_untreated'] * patient_data['systolic_bp']
        
        # Smoking contribution
        if patient_data['smoking']:
            risk_score += coefficients['smoking']
        
        # Diabetes contribution
        if patient_data['diabetes']:
            risk_score += coefficients['diabetes']
        
        # Additional risk factors adjustments
        risk_score = self._apply_additional_risk_factors(risk_score, patient_data)
        
        # Convert to probability
        probability = 1 - math.exp(-math.exp(risk_score))
        
        # Convert to percentage and ensure reasonable bounds
        risk_percentage = min(max(probability * 100, 0), 100)
        
        return risk_percentage
    
    def _apply_additional_risk_factors(self, base_risk: float, patient_data: Dict) -> float:
        """Apply additional risk factor adjustments."""
        adjusted_risk = base_risk
        
        # Family history adjustment
        if patient_data.get('family_history', False):
            adjusted_risk *= 1.2
        
        # BMI adjustment
        bmi = patient_data.get('bmi', 25)
        if bmi > 30:
            adjusted_risk *= 1.15
        elif bmi > 25:
            adjusted_risk *= 1.05
        
        # Physical activity adjustment
        activity_level = patient_data.get('physical_activity', 'Moderate')
        if activity_level == 'Low':
            adjusted_risk *= 1.1
        elif activity_level == 'High':
            adjusted_risk *= 0.9
        
        return adjusted_risk
    
    def get_risk_category(self, risk_score: float) -> str:
        """
        Categorize risk score into clinical risk categories.
        
        Args:
            risk_score: 10-year CVD risk percentage
            
        Returns:
            Risk category string
        """
        if risk_score < 10:
            return 'Low'
        elif risk_score < 20:
            return 'Moderate'
        else:
            return 'High'
    
    def get_risk_explanations(self, patient_data: Dict, risk_score: float) -> List[Dict]:
        """
        Provide explanations for risk factors contributing to the score.
        
        Args:
            patient_data: Patient information
            risk_score: Calculated risk score
            
        Returns:
            List of risk factor explanations
        """
        explanations = []
        
        # Age factor
        if patient_data['age'] > 65:
            explanations.append({
                'factor': 'Age',
                'impact': f'Advanced age ({patient_data["age"]} years) significantly increases cardiovascular risk.'
            })
        elif patient_data['age'] > 45:
            explanations.append({
                'factor': 'Age',
                'impact': f'Age ({patient_data["age"]} years) is a moderate risk factor.'
            })
        
        # Blood pressure
        if patient_data['systolic_bp'] > 140:
            explanations.append({
                'factor': 'Hypertension',
                'impact': f'Systolic BP ({patient_data["systolic_bp"]} mmHg) indicates hypertension, increasing risk.'
            })
        elif patient_data['systolic_bp'] > 130:
            explanations.append({
                'factor': 'Blood Pressure',
                'impact': f'Elevated systolic BP ({patient_data["systolic_bp"]} mmHg) contributes to increased risk.'
            })
        
        # Cholesterol
        if patient_data['total_cholesterol'] > 240:
            explanations.append({
                'factor': 'High Cholesterol',
                'impact': f'Total cholesterol ({patient_data["total_cholesterol"]} mg/dL) is significantly elevated.'
            })
        
        if patient_data['hdl_cholesterol'] < 40:
            explanations.append({
                'factor': 'Low HDL',
                'impact': f'Low HDL cholesterol ({patient_data["hdl_cholesterol"]} mg/dL) increases risk.'
            })
        
        # Lifestyle factors
        if patient_data['smoking']:
            explanations.append({
                'factor': 'Smoking',
                'impact': 'Current smoking significantly increases cardiovascular risk.'
            })
        
        if patient_data['diabetes']:
            explanations.append({
                'factor': 'Diabetes',
                'impact': 'Diabetes mellitus is a major cardiovascular risk factor.'
            })
        
        # Additional factors
        if patient_data.get('family_history', False):
            explanations.append({
                'factor': 'Family History',
                'impact': 'Family history of cardiovascular disease increases genetic predisposition.'
            })
        
        bmi = patient_data.get('bmi', 25)
        if bmi > 30:
            explanations.append({
                'factor': 'Obesity',
                'impact': f'BMI ({bmi:.1f}) indicates obesity, contributing to increased risk.'
            })
        
        return explanations
    
    def get_clinical_recommendations(self, risk_category: str, patient_data: Dict) -> List[str]:
        """
        Provide clinical recommendations based on risk category and patient data.
        
        Args:
            risk_category: Risk category (Low, Moderate, High)
            patient_data: Patient information
            
        Returns:
            List of clinical recommendations
        """
        recommendations = []
        
        if risk_category == 'High':
            recommendations.extend([
                "Immediate cardiology consultation recommended",
                "Consider statin therapy if not contraindicated",
                "Aggressive blood pressure management (target <130/80 mmHg)",
                "Smoking cessation counseling if applicable",
                "Diabetes management optimization",
                "Consider antiplatelet therapy (aspirin)",
                "Lifestyle modifications: diet, exercise, weight management"
            ])
        
        elif risk_category == 'Moderate':
            recommendations.extend([
                "Consider statin therapy based on clinical judgment",
                "Blood pressure monitoring and management",
                "Lifestyle modifications: Mediterranean diet, regular exercise",
                "Smoking cessation if applicable",
                "Annual cardiovascular risk reassessment",
                "Consider cardiology consultation"
            ])
        
        else:  # Low risk
            recommendations.extend([
                "Continue current preventive measures",
                "Regular blood pressure and cholesterol monitoring",
                "Maintain healthy lifestyle: diet and exercise",
                "Annual health screenings",
                "Smoking cessation if applicable"
            ])
        
        # Specific recommendations based on risk factors
        if patient_data['systolic_bp'] > 140:
            recommendations.append("Hypertension management: medication review and lifestyle modifications")
        
        if patient_data['total_cholesterol'] > 240:
            recommendations.append("Lipid management: dietary changes and possible statin therapy")
        
        if patient_data.get('bmi', 25) > 30:
            recommendations.append("Weight management: nutritional counseling and exercise program")
        
        return recommendations
