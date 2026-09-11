# MigrantShield

**MigrantShield** is a Django-based web application designed to provide a centralized system for managing migrant worker information, employment records, documentation, and related monitoring activities.

The system uses **role-based access control** to provide different functionality to administrators, police personnel, contractors, employers, and migrant workers.

---

## 🚀 Features

### 👥 Role-Based Access Control

The application supports multiple user roles, each with access to relevant functionality:

* Administrator
* Police
* Contractor
* Employer
* Migrant Worker

---

### 🧑‍💼 Migrant Management

* Register and manage migrant worker information
* Store personal and employment details
* Search and view migrant records
* Manage migrant-related information
* Generate unique migrant identification information
* Track relevant migrant records

---

### 📄 Document Management

* Aadhaar card document upload and management
* Police Clearance Certificate (PCC) management
* NOC generation
* UMIN card generation
* PDF document generation and handling

---

### 🚨 Crime Reporting & Monitoring

* Record crime reports
* Associate reports with migrant records
* View and manage crime-related information
* Search crime reports
* Flag migrant records requiring attention
* Monitor relevant red-flag information

---

### 💼 Employment & Job Management

* Manage employers and contractors
* Maintain employment records
* Manage worker-employer relationships
* Post and manage job opportunities
* Store salary-related information
* Generate salary receipts

---

### 📊 Dashboard & Reports

* Role-specific dashboards
* Search and filtering functionality
* View relevant migrant information
* Display employment-related information
* Generate reports
* Generate PDF documents

---

## 🛠️ Technologies Used

| Technology             | Purpose                   |
| ---------------------- | ------------------------- |
| **Python**             | Backend programming       |
| **Django 4.2**         | Web application framework |
| **MySQL**              | Database                  |
| **HTML5**              | Frontend structure        |
| **CSS3**               | Styling                   |
| **JavaScript**         | Client-side functionality |
| **ReportLab**          | PDF generation            |
| **pdfkit**             | PDF generation            |
| **XAMPP**              | Local MySQL environment   |
| **Visual Studio Code** | Development environment   |

---

## 🏗️ Project Structure

The project is organized into multiple Django applications. Each application contains its own templates and supporting files.

```text
Migrantshield/
│
├── migrantshield/
│   │
│   ├── admin_app/
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── static/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── contractor_app/
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── static/
│   │   └── ...
│   │
│   ├── employer_app/
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── static/
│   │   └── ...
│   │
│   ├── migrant_app/
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── static/
│   │   └── ...
│   │
│   ├── police_app/
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── static/
│   │   └── ...
│   │
│   └── ...
│
├── migrantshieldvenv/
│   └── Python virtual environment
│
└── manage.py
```

Each Django app follows a modular structure and can contain its own:

* Models
* Views
* Forms
* URLs
* Templates
* Static files
* Database migrations

This makes the application easier to organize and maintain as different features are separated into individual Django applications.

---

## 🔐 User Roles

### Administrator

The administrator has access to the overall system and can manage users, migrant information, reports, and other system-level data.

### Police

Police users can access relevant migrant information, police clearance information, and crime reports.

### Contractor

Contractors can manage workers and employment-related information.

### Employer

Employers can manage workers, employment information, and job-related functionality.

### Migrant Worker

Migrant workers can access their relevant personal, employment, and job information.

---

## 🔄 Application Workflow

```text
                    ┌─────────────────┐
                    │      User       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Authentication  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Role Assignment │
                    └────────┬────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Role-Based Dashboard│
                  └──────────┬───────────┘
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
     Migrant Data       Employment        Documentation
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ▼
                    ┌─────────────────┐
                    │ Reports &       │
                    │ Monitoring      │
                    └─────────────────┘
```

---

## 🗄️ Database

MigrantShield uses **MySQL** for data storage.

The project was developed and tested using **XAMPP** as the local MySQL environment.

Major categories of information handled by the system include:

* User accounts
* Migrant information
* Employer information
* Contractor information
* Police station information
* Employment records
* Job information
* Crime reports
* Document information
* Salary information

---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/kvbnpd/project_pg.git
```

Navigate into the project:

```bash
cd project_pg/Migrantshield
```

---

## 2. Create a Virtual Environment

The repository currently contains the development virtual environment. However, a new environment can also be created:

```powershell
python -m venv migrantshieldvenv
```

Activate it on Windows:

```powershell
.\migrantshieldvenv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

Install the required Python packages:

```powershell
pip install -r requirements.txt
```

If a `requirements.txt` file is not available, the major dependencies include Django and the packages required for MySQL and PDF generation.

---

## 4. Configure MySQL

Start **Apache** and **MySQL** from XAMPP.

Create a database named:

```text
migrantdb
```

Configure the database connection in the Django project's settings.

Example:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'migrantdb',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Update the username, password, host, and port according to your local MySQL configuration.

---

## 5. Apply Database Migrations

Run:

```powershell
python manage.py migrate
```

---

## 6. Create a Superuser

Create an administrator account:

```powershell
python manage.py createsuperuser
```

Follow the instructions displayed in the terminal.

---

## 7. Run the Development Server

Start the Django development server:

```powershell
python manage.py runserver
```

The application will normally be available at:

```text
http://127.0.0.1:8000/
```

Open the address in a web browser.

---

# 📁 Media & Documents

The application supports document and media management for features such as:

* Aadhaar documents
* PCC documents
* Generated NOC documents
* UMIN cards
* Other project-related PDF files

Uploaded files are stored through Django's media handling system.

> **Note:** Real personal documents or sensitive user information should not be used in a public production repository.

---

# 🎯 Project Objectives

The main objectives of MigrantShield are:

* Centralize migrant worker information
* Improve migrant data management
* Provide role-based access to information
* Simplify employment management
* Manage documentation digitally
* Maintain crime and clearance-related records
* Provide searchable records
* Generate reports and documents
* Improve coordination between different stakeholders

---

# 💡 Key Concepts Demonstrated

This project demonstrates practical experience with:

* Django MVC/MVT architecture
* Python web development
* MySQL database integration
* CRUD operations
* User authentication
* Role-based access control
* Django models and migrations
* Django forms
* URL routing
* HTML/CSS/JavaScript integration
* File uploads
* PDF generation
* Database relationships
* Search and filtering
* Dashboard development

---

# 🔮 Future Improvements

Possible improvements for future versions include:

* REST API development
* Mobile application integration
* Cloud deployment
* Docker containerization
* Advanced analytics and dashboards
* Automated email/SMS notifications
* Improved document verification
* Enhanced security and encryption
* Multi-language support
* Production-ready deployment
* Automated testing and CI/CD

---

# 📸 Screenshots

Screenshots of the application can be added here to demonstrate the major interfaces.

```text
Add screenshots of:

• Login page
• Administrator dashboard
• Migrant dashboard
• Migrant registration
• Migrant details
• Crime reports
• Job management
• UMIN card / NOC generation
• Reports
```

---

# 👨‍💻 Developer

**Brahmadathan K V**

MSc Computer Science

GitHub: **[@kvbnpd](https://github.com/kvbnpd)**

---

## 📌 Disclaimer

MigrantShield was developed as a software development/academic project.

Any sample or development data included with the project should not be considered real production data. Sensitive personal information should be removed before deploying or sharing the application publicly.
