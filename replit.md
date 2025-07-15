# MediCore HMS - Hospital Management System

## Overview

MediCore HMS is a comprehensive Hospital Management System built with Streamlit that provides healthcare professionals with advanced patient data management, cardiovascular risk assessment, and real-time analytics. The system features a futuristic cyberpunk interface with custom cursor implementation and stores all patient data in JSON format for easy management and portability.

## User Preferences

Preferred communication style: Simple, everyday language.
UI Design: Futuristic cyberpunk theme with custom Roblox-style cursor
Data Storage: JSON-based patient information storage
Watermark: "Made by Moeed ul Hassan @The Legend"

## Recent Changes (July 2025)

✓ Transformed from PulseAI to MediCore HMS - complete Hospital Management System
✓ Implemented comprehensive patient registration with JSON storage
✓ Added Patient Records module with search functionality
✓ Created Roblox-style custom cursor with hover effects
✓ Applied futuristic cyberpunk theme with neon colors and hologram effects
✓ Added neural network background animations and particle effects
✓ Integrated Orbitron font for sci-fi aesthetic
✓ Enhanced navigation with Hospital Management System modules
✓ Implemented comprehensive patient data structure with medical history, insurance, and emergency contacts
✓ Major UI/UX improvements with enhanced creativity and animations
✓ Added comprehensive About Creator section showcasing Moeed ul Hassan @The Legend
✓ Enhanced form styling with futuristic design elements
✓ Improved dashboard with enhanced metrics and creative visualizations
✓ Added progress indicators and validation checks
✓ Enhanced watermark with glowing animations

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - chosen for rapid prototyping and medical dashboard development
- **UI Components**: Custom CSS styling with medical-themed color scheme (green gradients)
- **Layout**: Wide layout with expandable sidebar for navigation
- **Visualizations**: Plotly for interactive charts and gauges

### Backend Architecture
- **Language**: Python 3.x
- **Data Processing**: Pandas and NumPy for numerical computations
- **Risk Calculation**: Custom Framingham Risk Score implementation
- **Session Management**: Streamlit session state for user data persistence

### Data Storage
- **Primary Storage**: JSON file-based system (`data/patient_data.json`)
- **Structure**: Patients and assessments stored separately
- **Rationale**: Lightweight solution for prototype/demo purposes, easily migrated to database later

## Key Components

### Risk Calculator (`utils/risk_calculator.py`)
- Implements Framingham Risk Score algorithm
- Separate coefficient sets for male and female patients
- Calculates 10-year cardiovascular disease risk percentage
- Supports risk factors: age, cholesterol levels, blood pressure, smoking, diabetes

### Data Manager (`utils/data_manager.py`)
- Handles patient data persistence
- JSON-based storage with auto-creation of data directory
- Functions for saving/retrieving patient information and assessment history
- Error handling for file operations

### Visualizations (`utils/visualizations.py`)
- Risk gauge charts with color-coded risk categories
- Timeline charts for assessment history
- Risk factors breakdown charts
- Uses Plotly for interactive visualizations

### Main Application (`app.py`)
- Streamlit-based user interface
- Patient input forms and assessment workflows
- Integration of all components
- Session state management

## Data Flow

1. **Patient Input**: Users enter patient data through Streamlit forms
2. **Risk Calculation**: Data passed to FraminghamRiskCalculator
3. **Risk Assessment**: Algorithm processes patient data and returns risk score
4. **Data Storage**: PatientDataManager saves patient and assessment data
5. **Visualization**: Risk scores and trends displayed through Plotly charts
6. **History Tracking**: Assessment history stored for longitudinal analysis

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive visualizations

### File Dependencies
- **assets/style.css**: Custom styling for medical theme
- **assets/logo.svg**: Application logo
- **data/patient_data.json**: Patient data storage

## Deployment Strategy

### Current Setup
- Local development with Streamlit server
- File-based data storage for simplicity
- No external database requirements

### Production Considerations
- Database migration path available (JSON structure easily convertible)
- Environment variables for configuration
- Healthcare data compliance requirements (HIPAA considerations)
- Scalability improvements needed for multi-user environments

### Security Notes
- Current implementation stores data locally
- No authentication/authorization implemented
- Designed for single-user or demonstration purposes
- Production deployment would require user management and data encryption

## Technical Decisions

### Why Streamlit?
- Rapid prototyping for medical applications
- Built-in components for forms and charts
- Easy deployment and sharing
- Python-native development

### Why JSON Storage?
- Lightweight for prototype phase
- Easy to inspect and debug
- Simple migration path to proper database
- No additional infrastructure requirements

### Why Framingham Risk Score?
- Clinically validated algorithm
- Widely accepted in medical practice
- Well-documented coefficients
- Suitable for general population screening