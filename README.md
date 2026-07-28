<div align="center">
  <h1>🏔️ TrekTour</h1>
  <p><b>An Advanced Online Trek Management System</b></p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version" />
    <img src="https://img.shields.io/badge/Flask-3.1.1-lightgrey.svg" alt="Flask Version" />
    <img src="https://img.shields.io/badge/Database-SQLite-green.svg" alt="Database" />
    <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status" />
  </p>
</div>

> TrekTour leverages **Role-Based Access Control (RBAC)** to provide a seamless, secure, and streamlined experience for managing treks, staff assignments, and customer bookings.

---

## ✨ Key Features

TrekTour is designed with three distinct user roles, each offering a tailored experience:

### 🛡️ Administrator
- **Comprehensive Dashboard:** Oversee total treks, bookings, and system users at a glance.
- **Trek Management:** Full CRUD (Create, Read, Update, Delete) capabilities for trekking routes.
- **Staff Assignment:** Seamlessly assign staff members to specific treks.
- **User Management:** Monitor, approve, or suspend user and staff accounts.

### 👥 Staff
- **Assigned Treks View:** Easily access all treks assigned by the administration.
- **Participant Tracking:** View the list of participants and bookings for assigned treks.
- **Status Updates:** Update trek progress and statuses.

### 🧗‍♂️ User (Customer)
- **Explore Treks:** Browse through a rich catalog of available treks including difficulty, duration, and remaining slots.
- **Booking Engine:** Book treks and manage reservations through a personalized dashboard.
- **History:** View past and upcoming trek bookings.

---

## 🛠️ Technology Stack

| Component         | Technology | Description |
|-------------------|------------|-------------|
| **Backend**       | Flask      | Core web framework for routing and logic. |
| **Database**      | SQLite     | Lightweight database used for storage. |
| **ORM**           | SQLAlchemy | Object-Relational Mapping (Flask-SQLAlchemy). |
| **Authentication**| Flask-Login| Handles user sessions and login state. |
| **Security**      | Werkzeug   | Password hashing and verification. |

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### 1️⃣ Prerequisites

Ensure you have **Python 3.8+** installed. You can check your version by running:
```sh
python --version
```

### 2️⃣ Installation

Clone the repository and navigate into the project directory:
```sh
git clone <your-repository-url>
cd Trektour
```

Set up a virtual environment to isolate dependencies:
```sh
python -m venv venv
```

Activate the virtual environment:
- **Windows:** `.\venv\Scripts\activate`
- **macOS / Linux:** `source venv/bin/activate`

Install the required Python packages:
```sh
pip install -r requirements.txt
```

### 3️⃣ Running the Application

Initialize the database and start the Flask development server:
```sh
flask run
```
*The application will be accessible at `http://127.0.0.1:5000/`.*

---

## 🏗️ Project Architecture

```text
Trektour/
├── app.py                 # Application factory and initialization
├── config.py              # App configuration (database URI, secret keys)
├── models.py              # Database schema (User, Trek, Booking)
├── requirements.txt       # Python dependencies
├── routes/                # Blueprint modules for modular routing
│   ├── auth.py            # Authentication routes (Login/Register)
│   ├── admin.py           # Administrator dashboard routes
│   ├── staff.py           # Staff-specific routes
│   ├── user.py            # Customer-facing routes
│   └── api.py             # RESTful API endpoints
├── static/                # CSS, JS, and image assets
└── templates/             # Jinja2 HTML templates
```

---

## 🔑 Default Admin Credentials

Upon launching the app for the first time, the database is automatically created along with a default administrator account.

- **Username:** `admin`
- **Email:** `admin@trek.com`
- **Password:** `admin123`


---

<div align="center">
  <i>Built with ❤️ for adventurers everywhere.</i>
</div>