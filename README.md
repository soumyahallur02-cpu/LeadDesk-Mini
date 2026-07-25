# LeadDesk Mini

A lightweight CRM (Customer Relationship Management) web application built with Flask to manage customer leads securely.

## Features

- Lead Capture Form
- Admin Login Authentication
- Secure Session Management
- Dashboard with Statistics
- Search Leads by Name or Email
- Update Lead Status
- Delete Leads
- Export Leads to CSV
- Interactive Charts using Chart.js
- Responsive User Interface

---

## Technology Stack

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite
- HTML
- CSS
- JavaScript
- Chart.js

---

## Database Models

### Lead

| Field | Description |
|-------|-------------|
| id | Unique Lead ID |
| name | Customer Name |
| email | Customer Email |
| budget | Project Budget |
| message | Project Description |
| status | New / Contacted / Closed |

### Admin

| Field | Description |
|-------|-------------|
| id | Admin ID |
| username | Login Username |
| password | Hashed Password |

---

## Authentication

- Flask-Login is used for authentication.
- Passwords are securely hashed using Werkzeug.
- Session-based login protects the admin dashboard.
- Unauthorized users are redirected to the login page.

---

## Installation

```bash
git clone <repository-url>
cd LeadDesk-Mini

pip install -r requirements.txt

python app.py
```

---

## Deployment

This project is deployed on Render.

---

## Test Credentials

**Username**

```
admin
```

**Password**

```
admin123
```

---

## Project Workflow

1. User submits a lead.
2. Lead is stored in the SQLite database.
3. Admin logs in securely.
4. Admin views all submitted leads.
5. Admin updates the lead status.
6. Admin searches or exports lead data.

---

## Author

**Soumya Hallur**
Computer Science Engineering Student