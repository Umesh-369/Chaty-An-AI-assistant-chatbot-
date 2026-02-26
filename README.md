# Final Chaty

## Overview
Final Chaty is a web application built using Python and Flask. It provides a complete user authentication flow, a personalized dashboard, and an integrated AI chatbot powered by the Google Gemini model (`gemini-2.5-flash`). All user data is securely managed and stored using Firebase Firestore.

## Features
- **Secure Authentication:** Custom sign-up, log-in, and log-out functionality with password hashing using Werkzeug.
- **Firebase Firestore Database:** Stores user records securely with the Firebase Admin SDK.
- **AI-Powered Chatbot:** A chat application interface integrated with the `google-genai` client for responsive AI conversations.
- **Protected Routes:** Both the dashboard and the chat application require users to be authenticated to access them.

## Prerequisites
Ensure you have the following installed and configured before running the application:
- Python 3.7 or higher
- A Google Gemini API Key
- A Firebase Project with Firestore enabled
- A Firebase Service Account Private Key

## Installation and Setup

1. **Clone or Download the Repository**
   Navigate to the project folder (`Final Chaty`).

2. **Set Up a Virtual Environment** (Recommended)
   ```bash
   python -m venv .venv
   # Activate on Windows:
   .\.venv\Scripts\activate
   # Activate on macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   Install the necessary Python packages:
   ```bash
   pip install flask google-genai firebase-admin werkzeug
   ```

4. **Add Firebase Credentials**
   - Go to your [Firebase Console](https://console.firebase.google.com/).
   - Open **Project Settings** > **Service Accounts**.
   - Click **Generate new private key** and download the JSON file.
   - Move this file to the root directory of the project and rename it to exactly `firebase-key.json`.

5. **Configure API Keys**
   - Currently, the Google Gemini API key is initialized in `main.py`. Ensure your API key is active. (It is highly recommended to use environment variables for API keys in production).

## Running the Application

1. Start the Flask server from the root directory:
   ```bash
   python main.py
   ```
2. Open your web browser and navigate to the application:
   ```
   http://localhost:8080
   ```

## Project Structure

```
Final Chaty/
│
├── .venv/                  # Python virtual environment (if created)
├── firebase-key.json       # Firebase service account credentials (must be provided)
├── main.py                 # The main Flask application and backend logic
└── templates/              # HTML frontend templates
    ├── index.html          # Chatbot application UI
    ├── dashboard.html      # Authenticated user dashboard
    ├── login.html          # Login page
    └── signup.html         # Registration page
```

## Technologies Used
- **Backend:** Python, Flask
- **AI Model:** Google Gemini (`gemini-2.5-flash`) via `google-genai`
- **Database:** Firebase Firestore (`firebase-admin`)
- **Security:** Werkzeug (Password Hashing)
- **Frontend:** HTML/CSS/JavaScript (via Flask templates)
