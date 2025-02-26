# Sahayak: Your Grocery Store AI Assistant

Sahayak is an AI-powered chatbot designed to assist grocery store owners with sales analysis, invoice processing, and customer insights. The project includes a React frontend and a FastAPI backend.

## Project Structure
```
.
├── ui/                # Frontend (React)
│   ├── src/
│   ├── public/
│   ├── .env.example  # Sample environment variables for frontend
│   ├── Dockerfile    # Docker configuration for frontend
│   └── package.json
│
├── backend/           # Backend (FastAPI)
│   ├── app/
│   ├── models/
│   ├── .env.example  # Sample environment variables for backend
│   ├── Dockerfile    # Docker configuration for backend
│   ├── requirements.txt
│   └── main.py
│
├── docker-compose.yml  # Docker configuration to run the full project
└── README.md           # Project documentation
```

## Prerequisites
Ensure you have the following installed:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/sahayak.git
cd sahayak
```

### 2. Set Up Environment Variables

Copy the example environment files and configure them:
```sh
cp ui/.env.example ui/.env
cp backend/.env.example backend/.env
```
Edit `.env` files as needed with your API keys and configurations.

### 3. Build and Start the Application

Run the following command to build and start the containers:
```sh
docker-compose up --build
```
This will start both the frontend and backend services. Please be patient, it might take some time. :)

### 4. Access the Application
- **Frontend (React UI):** `http://localhost:3039`
- **Backend (FastAPI API):** `http://localhost:8000/docs`

## Common Issues & Fixes
- **Permission Denied (Docker):** Run `sudo usermod -aG docker $USER` and restart your system.
- **Missing `.env` Files:** Ensure you copied the `.env.example` files as described in step 2.
- **Port Conflicts:** Ensure ports `3039` (frontend) and `8000` (backend) are not in use.



