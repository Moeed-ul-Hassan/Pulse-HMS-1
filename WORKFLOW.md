# Project Workflow

This section outlines the typical development and deployment workflow for the Pulse-HMS application.

## Development Cycle

1.  **Feature Branching**: All new features or bug fixes start with a new branch from `main` (e.g., `feature/new-dashboard`, `bugfix/login-issue`).
2.  **Local Development**: Code changes are made and tested locally.
3.  **Code Review**: Pull requests are opened for review by at least one other developer.
4.  **Testing**: Automated tests (unit, integration) are run. Manual testing is performed if necessary.
5.  **Merge**: Once approved and all checks pass, the branch is merged into `main`.

## Deployment Process

1.  **CI/CD Trigger**: Merges to `main` automatically trigger the CI/CD pipeline.
2.  **Build**: The application is built and dependencies are installed.
3.  **Testing**: Automated tests are re-run in the CI environment.
4.  **Deployment to Staging**: The application is deployed to a staging environment for final testing and UAT.
5.  **Deployment to Production**: After successful staging tests, the application is manually or automatically deployed to production.