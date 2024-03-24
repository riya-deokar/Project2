# Smart Document Analyzer / Document Sentiment Analyzer

A full-stack application that analyzes sentiment in uploaded documents, built with a React frontend and Flask backend. This README details the project setup, functionalities, and usage.

## Overview

The Document Sentiment Analyzer offers:

- Secure user authentication and registration.
- File uploading capabilities for PDFs, images, text files, etc.
- Asynchronous text extraction and sentiment analysis.
- A queue system for background processing of tasks.
- A frontend interface for file uploading and viewing results.

## Project Summary

### APIs Development

**Client/Server Architecture**:
- Implemented RESTful APIs in a Flask backend to handle user authentication, file uploads, and sentiment analysis.
- Utilized React for the frontend to create interactive UIs, making API requests to the backend for processing and displaying results.

**Frontend/Backend Interaction**:
- **Authentication API**: Allows users to register and login, maintaining secure sessions with JWTs.
- **File Upload API**: Users can upload documents (PDFs, images, text files), which are then queued for asynchronous processing.
- **Sentiment Analysis API**: Extracted text from documents is analyzed for sentiment, providing users with insights into their content.

### Queue System Implementation

To enhance application scalability and responsiveness, a queuing system was integrated:
- **Asynchronous Processing**: Offloads heavy lifting from the web request-response cycle, placing tasks in queues for background processing.
- **PDF and NLP Analysis Queues**: Separately handle file processing and sentiment analysis, improving efficiency and manageability.
- **Worker Threads**: Continuously monitor queues and process tasks, ensuring timely task completion without blocking user interactions.

### Frontend and Backend Details

**Frontend**:
- Built with React, offering a dynamic and responsive user interface.
- Handles user inputs, file uploads, and displays sentiment analysis results interactively.
- Implements client-side routing and state management for a seamless user experience.

**Backend**:
- Developed with Flask, serving as a robust and scalable API server.
- Manages user authentication, file storage, and invokes the queuing system for file and text processing.
- Integrates with SQLAlchemy for database operations and JWT for secure authentication.

## Setup

### Backend (Flask)

1. **Pre-requisites**: Ensure Python 3.8+ and pip are installed.

2. **Install Dependencies**:
    ```bash
    pip install -r r.txt
    ```

3. **Set Environment Variables**:
    ```bash
    export FLASK_APP=main.py
    export FLASK_ENV=development
    ```

4. **Initialize Database**:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. **Run the Application**:
    ```bash
    flask run
    ```

### Frontend (React)

1. **Pre-requisites**: Ensure Node.js and npm are installed.

2. **Install Dependencies**:
    ```bash
    npm install
    ```

3. **Start the Application**:
    ```bash
    npm start
    ```

## APIs

- **Auth**: 
    - Register: `POST /auth/register`
    - Login: `POST /auth/login`
    - Protected: `GET /auth/protected` (requires JWT)

- **File Processing**: 
    - Upload: `POST /api/upload/` (asynchronously processes files)

- **Sentiment Analysis**: 
    - Analyze: `POST /api/analyze/` (returns sentiment of submitted text)

## Queuing System

Implemented in `queue_utils.py`, the queuing system manages background processing, enhancing performance under load:

- **PDF Analysis Queue**: Handles asynchronous processing of uploaded documents.
- **NLP Analysis Queue**: Manages background sentiment analysis of texts.

Workers continuously process tasks from these queues independently of the main application flow.