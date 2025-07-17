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
- `app.py`: Main Streamlit application with cyberpunk UI
- `utils/risk_calculator.py`: Framingham Risk Score implementation
- `utils/data_manager.py`: Patient data persistence layer
- `utils/visualizations.py`: Plotly chart generation
- `assets/style.css`: Custom cyberpunk styling
- `data/patient_data.json`: Patient data storage

## Features
- Patient registration and records management
- AI-powered cardiovascular risk assessment
- Real-time patient monitoring dashboard
- Analytics and reporting
- Custom cyberpunk UI with animations

## Recent Changes
- **2025-07-17**: Migrated from Replit Agent to standard Replit environment
- **2025-07-17**: Added Streamlit configuration for proper deployment
- **2025-07-17**: Verified all dependencies and project structure

## User Preferences
- Cyberpunk/futuristic UI theme with animations
- Comprehensive patient management features
- Real-time monitoring capabilities

## Deployment Configuration
- Streamlit server configured for 0.0.0.0:5000
- Dependencies managed via pyproject.toml and uv
- Ready for Replit deployment