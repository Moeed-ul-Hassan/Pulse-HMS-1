# Admin Only Readme

This document contains sensitive or internal project information not intended for public viewing.

## Important Project Data

*   **Sensitive API Keys/Credentials**: [Placeholder for sensitive keys]
*   **Internal Server Endpoints**: [Placeholder for internal endpoints]
*   **Database Connection Details**: [Placeholder for database connection details]
*   **Deployment Specifics**: [Placeholder for deployment-specific notes]

## Project Blueprint (Architecture Overview)

This section describes the high-level architecture and key components of the Pulse-HMS application.

*   **Frontend**: Streamlit-based web application for user interaction.
*   **Backend/Logic**: Python scripts and modules handling business logic, data processing, and integrations.
*   **Data Storage**: JSON files for patient data, appointments, users, etc. (Consider migrating to a proper database for scalability).
*   **PDF Generation**: `fpdf2` and `reportlab` for generating reports.
*   **Authentication**: Custom authentication module (`auth.py`).
*   **Modules**: Modular design with separate components for patient management, billing, scheduling, inventory, etc.

---

*This document is for internal use only. Do not share publicly.*