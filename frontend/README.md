# BikeShareWebApp – Frontend

This repository contains the **frontend** of the BikeShareWebApp.

It is developed using:

* **Next.js**
* **React.js**
* **Tailwind CSS**
* Leaflet (for map rendering)

By default, the frontend runs locally at:

```
http://127.0.0.1:3000
```

It fetches data from the backend running at:

```
http://127.0.0.1:5000
```

---

## ⚠ Backend Dependency Notice

If the backend is **not running**, the following features will NOT work:

* Weather information
* User interface data
* Bike station distribution and availability
* Navigation functionality

In this case, only the base map page will be visible.

---

# Deployment & Local Setup Guide

---

## STEP 1 — Clone the Repository

Open a Bash terminal and navigate to your desired working directory (for example, your User home directory).

Example (Windows):

```
C:\Users\YourName\
```

Then clone the repository:

```bash
git clone https://github.com/HazelY90/COMP30830SE.git
cd COMP30830SE
```

---

## STEP 2 — Install Frontend Environment

Navigate to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

### Note:

If `npm` is not available, please install **Node.js** (which includes npm) first.

---

## STEP 3 — Run the Frontend

Start the development server:

```bash
npm run dev
```

### Verification:

Open your browser and visit:

```
http://localhost:3000/
```

If the frontend starts successfully, you should see the map page.

---

## STEP 4 — Install Backend Environment

⚠ Open a **NEW** Bash terminal window.
⚠ Do NOT close the frontend terminal.

Navigate to the backend folder:

```bash
cd COMP30830SE/backend
```

Create a virtual environment:

```bash
python -m venv venv
```

---

### Activate the Virtual Environment

**Windows (Git Bash):**

```bash
source venv/Scripts/activate
```

**MacOS / Linux:**

```bash
source venv/bin/activate
```

---

Install backend dependencies:

```bash
pip install -r requirements.txt
```

---

## STEP 5 — Start the Backend

Run:

```bash
python app.py
```

---

### Verification

Refresh the browser page opened earlier.

If the backend starts successfully, **Bike Station Markers** should appear on the map.

---

# Daily Startup (After First Setup)

Every time you want to run the project:

* Open **TWO** Bash windows.

---

## Frontend Terminal

```bash
cd COMP30830SE/frontend
npm run dev
```

---

## Backend Terminal

### Windows (Git Bash)

```bash
cd COMP30830SE/backend
source venv/Scripts/activate
python app.py
```

### MacOS / Linux

```bash
cd COMP30830SE/backend
source venv/bin/activate
python app.py
```

---

## Open in Browser

```
http://localhost:3000
```
