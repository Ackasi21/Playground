# Hurricane Monitoring Application

This is a Streamlit application that monitors hurricanes using data from the National Hurricane Center (NHC).

## Features
- Displays general hurricane updates
- Provides state-specific hurricane updates
- Interactive map showing hurricane locations

## Usage
1. Enter the state you want to monitor for hurricanes. You can use either the state abbreviation (e.g., FL) or the full state name (e.g., Florida).
2. Click the "Show Country-Wide Updates" button to see all hurricane updates.
3. Click the "Show State-Specific Updates" button to see updates for the specified state.

## Installation
1. Clone the repository.
2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the application:
    ```bash
    streamlit run streamlit_app.py
    ```

## Deployment
This app can be deployed on Streamlit Cloud. Ensure the `requirements.txt` file is in the root directory of your repository.
