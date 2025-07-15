import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class PatientDataManager:
    """
    Manages patient data storage and retrieval.
    Handles patient information and assessment history.
    """
    
    def __init__(self, data_file: str = "data/patient_data.json"):
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load patient data from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {'patients': {}, 'assessments': []}
        else:
            return {'patients': {}, 'assessments': []}
    
    def _save_data(self) -> None:
        """Save patient data to JSON file."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
    
    def save_patient(self, patient_data: Dict) -> None:
        """
        Save patient information.
        
        Args:
            patient_data: Dictionary containing patient information
        """
        patient_id = patient_data['id']
        self.data['patients'][patient_id] = patient_data
        self._save_data()
    
    def get_patient(self, patient_id: str) -> Optional[Dict]:
        """
        Retrieve patient information by ID.
        
        Args:
            patient_id: Patient identifier
            
        Returns:
            Patient data dictionary or None if not found
        """
        return self.data['patients'].get(patient_id)
    
    def get_all_patients(self) -> List[Dict]:
        """
        Get all patients.
        
        Returns:
            List of patient dictionaries
        """
        return list(self.data['patients'].values())
    
    def save_assessment(self, assessment_data: Dict) -> None:
        """
        Save assessment data.
        
        Args:
            assessment_data: Dictionary containing assessment information
        """
        self.data['assessments'].append(assessment_data)
        self._save_data()
    
    def get_patient_assessments(self, patient_id: str) -> List[Dict]:
        """
        Get all assessments for a specific patient.
        
        Args:
            patient_id: Patient identifier
            
        Returns:
            List of assessment dictionaries
        """
        return [
            assessment for assessment in self.data['assessments']
            if assessment['patient_data']['id'] == patient_id
        ]
    
    def get_all_assessments(self) -> List[Dict]:
        """
        Get all assessments.
        
        Returns:
            List of assessment dictionaries
        """
        return self.data['assessments']
    
    def update_patient(self, patient_id: str, updated_data: Dict) -> bool:
        """
        Update patient information.
        
        Args:
            patient_id: Patient identifier
            updated_data: Updated patient data
            
        Returns:
            True if update successful, False otherwise
        """
        if patient_id in self.data['patients']:
            self.data['patients'][patient_id].update(updated_data)
            self._save_data()
            return True
        return False
    
    def delete_patient(self, patient_id: str) -> bool:
        """
        Delete patient and associated assessments.
        
        Args:
            patient_id: Patient identifier
            
        Returns:
            True if deletion successful, False otherwise
        """
        if patient_id in self.data['patients']:
            # Remove patient
            del self.data['patients'][patient_id]
            
            # Remove associated assessments
            self.data['assessments'] = [
                assessment for assessment in self.data['assessments']
                if assessment['patient_data']['id'] != patient_id
            ]
            
            self._save_data()
            return True
        return False
    
    def get_patient_statistics(self) -> Dict:
        """
        Get patient statistics.
        
        Returns:
            Dictionary containing patient statistics
        """
        total_patients = len(self.data['patients'])
        total_assessments = len(self.data['assessments'])
        
        if total_assessments == 0:
            return {
                'total_patients': total_patients,
                'total_assessments': total_assessments,
                'average_age': 0,
                'gender_distribution': {},
                'risk_distribution': {}
            }
        
        # Calculate statistics
        ages = [patient['age'] for patient in self.data['patients'].values()]
        genders = [patient['gender'] for patient in self.data['patients'].values()]
        risk_categories = [assessment['risk_category'] for assessment in self.data['assessments']]
        
        average_age = sum(ages) / len(ages) if ages else 0
        
        gender_distribution = {}
        for gender in genders:
            gender_distribution[gender] = gender_distribution.get(gender, 0) + 1
        
        risk_distribution = {}
        for risk in risk_categories:
            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1
        
        return {
            'total_patients': total_patients,
            'total_assessments': total_assessments,
            'average_age': average_age,
            'gender_distribution': gender_distribution,
            'risk_distribution': risk_distribution
        }
