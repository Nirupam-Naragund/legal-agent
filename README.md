# Legal Analysis Application

This project is a web-based application that allows users (e.g., police or general users) to input a crime description. Based on the input, the application generates relevant **IPC (Indian Penal Code) sections**, **landmark judgments**, and a **legal summary**. The application is built using a combination of backend logic (Python) and a frontend interface (React or similar framework).

---

## Features

- **Crime Input**: Users can type or describe the crime that has occurred.
- **IPC Sections**: The application generates relevant IPC sections based on the crime description.
- **Landmark Judgments**: Provides landmark court judgments related to the crime.
- **Legal Summary**: A concise legal summary of the crime and its implications.

---

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8 or higher
- Node.js (for the frontend)
- npm (Node Package Manager)

---

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd <project-folder>
```

### Step 2: Set Up Environment Variables

Create a .env file in the root directory of the project.

```bash
GEMINI_API_KEY=""
```

Step 3: Create a Virtual Environment
Navigate to the project directory.

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

Step 4: Install Python Dependencies
Install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

Step 5: Run the Backend Server
Start the backend server by running:

```bash
python main.py
```

The backend server will start running on http://localhost:8000 

Step 6: Set Up and Run the Frontend
Open a new terminal window.

Navigate to the legal-analysis-app directory:

```bash
cd legal-analysis-app
```

Install the required npm packages:

```bash
npm install
```

Start the frontend development server:

```bash
npm run dev
```

The frontend will be available at http://localhost:3000 (or another port if specified).

Usage
Open your browser and navigate to http://localhost:3000.

Enter the crime description in the input field.

Click the "Analyze" button to view the relevant IPC sections, landmark judgments, and legal summary.

[Demo Video](./Legal-analysis.mp4)


