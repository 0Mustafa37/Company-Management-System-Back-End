# Company Management System

## 1. Overview
The **Company Management System** is a backend solution that provides functionality for managing companies, departments, employees, and projects.  
It supports full CRUD operations, a structured **Employee Performance Review Workflow**, and **role-based access control** for secure data handling.

This project is designed to reflect real-world enterprise system requirements while ensuring scalability, maintainability, and security.

---

## 2. Approach & Implementation Details

### Tech Stack
- **Framework**: Django REST Framework (DRF)
- **Authentication**: JWT (JSON Web Tokens) using `djangorestframework-simplejwt`
- **Database**: SQLite (default) / PostgreSQL (production-ready)
- **Language**: Python 3.10+

### Key Features
- **User Roles**:
  - Admin
  - Manager
  - Employee
- **Auto-Calculated Fields**:
  - Company: Number of departments, employees, projects
  - Department: Number of employees, projects
  - Employee: Days employed
- **Employee Performance Review Cycle**:
  - Stages: Pending Review → Review Scheduled → Feedback Provided → Under Approval → Review Approved/Rejected
  - Transitions strictly controlled
- **APIs**: RESTful endpoints for all entities
- **Testing**: Unit and integration tests
- **Bonus**: Logging with Django logging module

---

## 3. Setup Instructions

### Prerequisites
- Python 3.10+
- pip & virtualenv
- Django 4.x
- Django REST Framework
- SimpleJWT package

### Installation
```bash
# Clone repository
git clone https://github.com/0Mustafa37/Company-Management-System-Back-End.git
cd company-management-system

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Access
- API Root: `http://127.0.0.1:8000/api/`
- Admin Panel: `http://127.0.0.1:8000/admin/`

---

## 4. Task Completion Checklist ✅

- [x] **Data Models**  
  - User (Admin, Manager, Employee roles)  
  - Company (auto-calculated departments, employees, projects)  
  - Department (auto-calculated employees, projects)  
  - Employee (auto-calculated days employed)  
  - Project (bonus, with assigned employees)  

- [x] **CRUD Operations**  
  - Full RESTful APIs for all models (Company, Department, Employee, Project)  

- [x] **Employee Performance Review Workflow**  
  - Implemented with all defined stages & transitions  

- [x] **Role-Based Access Control**  
  - Different permissions for Admin, Manager, Employee  

- [x] **Authentication & Authorization**  
  - JWT-based secure authentication with refresh tokens  

- [x] **API Documentation**  
  - Endpoints, parameters, and example responses  

- [x] **Testing**  
  - Unit tests for models & APIs  
  - Integration tests for workflows  

- [ ] **Bonus: Logging**  
  - Basic logging implemented (optional improvement)  

---

### 🔹 Assumptions
- "Days Employed" is only calculated if `hired_on` is set.  
- One employee belongs to exactly one company and one department.  
- Projects can have multiple employees assigned.  

---

## 5. Security Measures
- **Role-based access control**:
  - **Admin**: Full CRUD permissions across all models
  - **Manager**: Can manage employees, projects, and departments within their company
  - **Employee**: Limited to viewing personal details and assigned projects
- **Authentication**: Secure JWT tokens (access + refresh)
- **Authorization**: DRF permissions (`IsAuthenticated`, custom role-based permissions)
- **Data Protection**: Passwords securely hashed with Django’s PBKDF2

---

## 6. API Documentation

### Authentication
- `POST /api/user/login/` → Obtain access & refresh tokens
- `POST /api/user/register/` → For register
### Companies
- `GET /api/companies/` → List companies
- `GET /api/companies/{id}/` → Retrieve company details

### Departments
- `GET /api/departments/` → List departments
- `GET /api/departments/{id}/` → Retrieve department details

### Employees
- `POST /api/employees/` → Create employee
- `GET /api/employees/` → List employees
- `PATCH /api/employees/{id}/` → Update employee
- `DELETE /api/employees/{id}/` → Delete employee

### Projects (Bonus)
- `POST /api/projects/` → Create project
- `GET /api/projects/` → List projects
- `PATCH /api/projects/{id}/` → Update project
- `DELETE /api/projects/{id}/` → Delete project
### API Documentation
- `http://127.0.0.1:8000/api/docs/`
---

## 7. Notes
- Submit the project via GitHub (public repository).  
- README includes setup, documentation, and checklist.  
- Bonus features are optional and add extra value.  

---
