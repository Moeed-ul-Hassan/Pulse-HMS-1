# MediCore HMS - Hospital Management System

## Overview

MediCore HMS is a futuristic, cyberpunk-themed Hospital Management System built with Streamlit. It empowers healthcare professionals with advanced patient data management, AI-powered cardiovascular risk assessment (Framingham Risk Score), and real-time analytics. All patient data is stored in JSON format for easy management and portability.

## Features

- **Patient Registration:** Comprehensive forms for personal, medical, emergency, insurance, and hospital information.
- **Patient Records:** Search, view, and manage patient data with assessment history.
- **Risk Assessment:** AI-powered Framingham Risk Score calculation with explainable results and clinical recommendations.
- **Admissions:** Patient admission workflow with queue and analytics.
- **Analytics Dashboard:** Visualize risk distributions, trends, and summary statistics.
- **Real-Time Monitor:** Live patient monitoring with simulated vital signs and risk updates.
- **Custom UI:** Futuristic cyberpunk design, Roblox-style cursor, animated watermark, and creative CSS effects.
- **About Creator:** Professional profile of Moeed ul Hassan @The Legend.

## System Architecture

- **Frontend:** Streamlit with custom CSS and Plotly for interactive charts.
- **Backend:** Python 3.x, Pandas, NumPy for data processing.
- **Data Storage:** JSON file-based ([data/patient_data.json](data/patient_data.json)).
- **Key Modules:**
  - [`utils/risk_calculator.py`](utils/risk_calculator.py): Framingham Risk Score logic.
  - [`utils/data_manager.py`](utils/data_manager.py): Patient data persistence.
  - [`utils/visualizations.py`](utils/visualizations.py): Plotly chart generation.

## Getting Started

### Prerequisites

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- pandas, numpy, plotly

### Installation

1. Clone this repository.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   Or manually:
   ```sh
   pip install streamlit pandas numpy plotly
   ```

### Running the App

```sh
streamlit run app.py
```

The app will open in your browser.

## File Structure

- [app.py](app.py): Main Streamlit application.
- [assets/style.css](assets/style.css): Custom CSS for UI.
- [assets/logo.svg](assets/logo.svg): App logo.
- [data/patient_data.json](data/patient_data.json): Patient data storage.
- [utils/data_manager.py](utils/data_manager.py): Data management logic.
- [utils/risk_calculator.py](utils/risk_calculator.py): Risk calculation logic.
- [utils/visualizations.py](utils/visualizations.py): Chart and visualization logic.

## Customization

- **Theme & UI:** Edit [assets/style.css](assets/style.css) and the `load_css()` function in [app.py](app.py).
- **Risk Algorithm:** Modify [`FraminghamRiskCalculator`](utils/risk_calculator.py).
- **Data Model:** Update [`PatientDataManager`](utils/data_manager.py) for new fields or storage changes.

## Disclaimer

> ⚠️ This tool is for clinical decision support only. All diagnostic and treatment decisions must be made by qualified healthcare professionals.

## Credits

Crafted by **Moeed ul Hassan @The Legend**  
Futuristic UI, creative coding, and healthcare innovation.

---

**Made with