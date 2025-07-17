# PulseAI - Hospital Management System

## Project Overview
PulseAI (formerly MediCore HMS) is a futuristic, cyberpunk-themed Hospital Management System built with Streamlit. It provides healthcare professionals with advanced patient data management, AI-powered cardiovascular risk assessment using the Framingham Risk Score, and real-time analytics.

## Project Architecture
- **Frontend**: Streamlit with custom CSS and animated UI elements
- **Backend**: Python with pandas, numpy for data processing
- **Data Storage**: JSON file-based storage (data/patient_data.json)
- **Visualization**: Plotly for interactive charts and real-time monitoring
- **Risk Assessment**: Framingham Risk Score calculator

### Key Components
- `app.py`: Main Streamlit application with comprehensive patient management
- `components/patient_manager.py`: Advanced patient registration and visit management
- `components/`: Modular components for different hospital functions
- `utils/risk_calculator.py`: Framingham Risk Score implementation
- `utils/data_manager.py`: Patient data persistence layer
- `utils/visualizations.py`: Plotly chart generation
- `assets/style.css`: Custom cyberpunk styling
- `data/patient_data.json`: Legacy patient data storage
- `data/patients_detailed.json`: Comprehensive patient management data

## Features
- **Comprehensive Patient Management**: Full patient registration with detailed visit tracking
- **Advanced Patient Forms**: Symptoms selection, medication management, report uploads
- **Patient Search & History**: Searchable patient database with complete visit history
- **AI-Powered Risk Assessment**: Framingham Risk Score implementation
- **PDF Report Generation**: Downloadable patient reports with hospital branding
- **Appointment Scheduling**: Future visit planning and management
- **Medical Records**: Complete patient lifecycle management
- **Analytics and Reporting**: Hospital performance dashboards
- **Developer Recognition**: Animated watermark and about page
- **Custom Cyberpunk UI**: Modern, healthcare-focused interface

## Recent Changes
- **2025-07-17**: Migrated from Replit Agent to standard Replit environment
- **2025-07-17**: Added comprehensive patient management system
- **2025-07-17**: Removed Real-Time Monitor as requested
- **2025-07-17**: Added detailed patient registration with symptoms, medications, and reports
- **2025-07-17**: Implemented patient search and history tracking
- **2025-07-17**: Added PDF report generation for patient visits
- **2025-07-17**: Created "About Developer" page with animated watermark
- **2025-07-17**: Cleaned up project structure (removed old app.py, renamed app_enhanced.py to app.py)
- **2025-07-17**: Fixed settings page TypeError issue

## User Preferences
- Modern, clean design with Poppins font family
- No login/logout system required (direct access)
- Comprehensive hospital management features
- Real-time monitoring capabilities
- Professional healthcare-focused UI

## Deployment Configuration
- Streamlit server configured for 0.0.0.0:5000
- Dependencies managed via pyproject.toml and uv
- Ready for Replit deployment