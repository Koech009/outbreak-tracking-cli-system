# 🦠 Outbreak CLI System

> A role-based infectious disease outbreak tracking system built with Python (CLI-based).

---

## 📌 Overview

**Outbreak CLI** is a modular, object-oriented command-line application designed to manage infectious disease outbreak data using a structured service-layer architecture.

The system implements **Role-Based Access Control (RBAC)** and allows secure:

- User authentication
- Case reporting & classification
- Region management
- Outbreak monitoring & summaries

This project demonstrates practical backend system design using clean architecture principles.

---

## 🎯 Key Learning Objectives

This project demonstrates:

- ✅ Object-Oriented Programming (OOP)
- ✅ Service Layer Architecture
- ✅ Role-Based Access Control (RBAC)
- ✅ Input Validation & Data Integrity
- ✅ File-Based Persistence (JSON)
- ✅ Unit & Integration Testing (pytest)
- ✅ Git Feature Branch Workflow

---

## 👥 User Roles & Permissions

| Role                    | Permissions                                                      |
| ----------------------- | ---------------------------------------------------------------- |
| 👑 **Admin**            | Manage users, Manage regions, View all cases, Monitor statistics |
| 🧑‍⚕️ **Health Worker**    | View cases, Update classification, Update patient status         |
| 👥 **Community Member** | Register, Login, Report suspected cases, View personal reports   |

---

## 🚀 Features

### 🔐 Authentication System

- Secure user registration & login
- Password hashing
- Email format validation
- Strong password enforcement
- ENUM-controlled role assignment

---

### 🧑‍⚕️ Case Management

- Report outbreak cases
- Update case classification:
  - `suspected`
  - `confirmed`
  - `discarded`
- Update patient status:
  - `under_treatment`
  - `recovered`
  - `deceased`
- Confirm diseases (health workers only)
- Role-based case visibility
- Outbreak summary statistics

---

### 🌍 Region Management

- Add regions
- Remove regions
- View all regions
- Enforced foreign key relationship (Region → Case)

---

### 📊 Reporting & Monitoring

- Classification summary
- Patient outcome summary
- Structured CLI table output (Rich)

---

## 🏗️ System Architecture

The project follows a layered architecture:

Models → Define system entities  
Services → Business logic & RBAC enforcement  
Utils → Validation & file handling  
Data → JSON persistence layer  
Tests → Unit & integration testing

This separation ensures:

- High maintainability
- Scalability
- Clear responsibility boundaries
- Clean code structure

---

## 📁 Project Structure

```
outbreak_cli/
├── main.py
├── models/
│   ├── case.py
│   ├── user.py
│   ├── region.py
│   └── person.py
├── services/
│   ├── auth_service.py
│   ├── case_service.py
│   └── region_service.py
├── utils/
│   ├── validators.py
│   ├── file_handler.py
│   └── decorators.py
├── data/
│   ├── users.json
│   ├── cases.json
│   └── regions.json
├── tests/
│   ├── test_auth_service.py
│   ├── test_case.py
│   ├── test_case_service.py
│   ├── test_validators.py
│   ├── test_region_service.py
│   ├── test_user_model.py
│   ├── test_region_model.py
│   ├── test_file_handler.py
│   └── test_main_cli.py
├── db_diagram/
│   ├── outbreak_schema.dbml
│   └── outbreak_schema.png
├── requirements.txt
├── pytest.ini
├── README.md
└── .gitignore
```

---

## 🗄️ Database Design (Conceptual Schema)

Although the project uses JSON persistence, it is designed using relational database principles.

### 👤 Users

- `id` (Primary Key)
- `name`
- `email` (Unique)
- `password_hash`
- `role` (ENUM: `community`, `health_worker`, `admin`)
- `created_at`

### 🌍 Regions

- `id` (Primary Key)
- `name` (Unique)
- `location`
- `created_at`

### 🧑‍⚕️ Cases

- `id` (Primary Key)
- `patient_name`
- `age`
- `gender`
- `region_id` (Foreign Key → Regions)
- `reported_by` (Foreign Key → Users)
- `date_reported`
- `classification_status` (ENUM)
- `patient_status` (ENUM)
- `created_at`
- `updated_at`

---

## 🔗 Relationships

- One **User** can report many **Cases**
- One **Region** can contain many **Cases**
- Each **Case** belongs to one **Region**
- Each **Case** is reported by one **User**

Foreign key rules are enforced at the application level.

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Koech009/outbreak-tracking-cli-system
cd outbreak-tracking-cli-system
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
python main.py
```

---

## 🧪 Running Tests

The project uses **pytest**.

Run all tests:

```bash
pytest
```

---

## 🛠️ Technologies Used

- Python 3
- Pytest
- Rich (CLI formatting)
- JSON (file-based storage)
- DBML (schema design)

---

## 🔮 Future Improvements

- Replace JSON with SQLite or PostgreSQL
- Add advanced filtering & search
- Export reports (CSV / PDF)
- Convert CLI to REST API
- Deploy as a web-based system

---

## 👨‍💻 Author

**Ian Kipchirchir Koech**  
📧 iankipchirchir51@gmail.com

---

## 📜 License

Developed for academic and demonstration purposes.
