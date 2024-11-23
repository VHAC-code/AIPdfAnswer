# Backend

cd backend
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py runserver

# Frontend

cd frontend
npm install
npm start

# InternASSIGN Project

# Overview

This project is a full-stack application demonstrating the integration of a React-based frontend and a Python Django backend. The backend handles API requests and manages data, while the frontend provides a responsive user interface. It is designed for showcasing features such as authentication, CRUD operations, and seamless API integration.

# Features

Frontend: Built using React with responsive UI components.
Backend: Developed using Django (or Flask, update accordingly), with RESTful APIs.
Authentication: Secure user authentication (e.g., login, signup).
Environment Management: Secrets stored securely using .env.

# Technologies Used

# Frontend

React
HTML/CSS
Axios (for API requests)

# Backend

Django (or Flask)
Django REST Framework
SQLite (or other DB, specify)

# Additional Tools

Node.js and npm
Python virtual environment
Postman (for API testing)

# Folder Structure :

InternASSIGN/
├── backend/
│ ├── manage.py # Main backend script
│ ├── .env # Environment variables (excluded from Git)
│ ├── settings.py # Django settings
│ └── <other backend files>
├── frontend/
│ ├── src/
│ │ ├── App.js # Main React component
│ │ ├── components/ # Reusable components
│ │ ├── services/ # API integration
│ └── <other frontend files>
├── Venv/ # Python virtual environment
├── README.md # Project documentation
└── architecture.md # Design documentation

# Setup Instructions

# Backend Setup

Navigate to the backend folder:

cd backend
Activate the Python virtual environment:

# On Linux/Mac:

source ../Venv/bin/activate

# On Windows:

../Venv/Scripts/activate

# Install dependencies:

pip install -r requirements.txt

# Run the backend server:

uvicorn app:app --reload

# Frontend Setup

Navigate to the frontend folder:

cd ../frontend
Install dependencies:

npm install
Start the frontend development server:

npm start

# API Documentation

Base URL:

http://localhost:8000/api/

# Demo Links

Frontend Hosted Link: Frontend on Netlify
Backend Hosted Link: Backend on Render
Demo Video: Demo Video on Google Drive

Application Architecture
Refer to architecture.md for a detailed design document, including:

High-Level Design (HLD): Overall architecture and workflow.
Low-Level Design (LLD): Module interactions and key components.

# Future Enhancements

Add testing coverage for both frontend and backend.
Integrate CI/CD pipelines for smoother deployments.
Implement advanced features like real-time notifications.

# Contact

For any questions or feedback, please reach out to:

Name: Vachas Pati Pandey
Email: vachaspati1997@gmail.com
GitHub: VHAC-code
