# Core Banking System (CBS) — Terminal Interface

The **Core Banking System (CBS)** is a modular, secure, multi-tier command-line interface (CLI) application engineered in **Python** and backed by a local **MySQL** relational database. The platform simulates mission-critical banking operations including **Role-Based Access Control (RBAC)**, customer profile management, secure financial transactions, administrative account management, and comprehensive transaction auditing.

---

# 1. Core Engineering Architecture

## Role-Based Access Control (RBAC)

Restricts administrative commands (`-employee`, `-status`) exclusively to authenticated **ADMIN** users while allowing standard banking operations for **STAFF** accounts.

## Atomic Financial Execution Engine

Processes deposits (`CREDIT`), withdrawals (`DEBIT`), and inter-account transfers (`TRANSFER`) while preserving transaction integrity through database transaction management.

## Transaction Rollback Protection

Automatically invokes `db.rollback()` whenever an exception occurs during a transaction, preventing partial updates and ensuring database consistency.

## Administrative Access Isolation

Allows administrators to manage employee accounts, review customer information, and modify account states (`ACTIVE` / `BLOCKED`) without exposing privileged functionality to standard staff members.

## Comprehensive Master Ledger Auditing

Displays structured transaction histories including sender, receiver, transaction type, amount, and timestamps directly within the terminal.

---

# 2. Project Directory Structure

```text
CBS-TERMINAL/
├── cbs.sql                # Database schema and default seed data
├── connection.py          # Database connection manager
├── login.py               # Authentication system
├── help.py                # Interactive command reference
├── main.py                # Application entry point
├── customer_info.py       # Customer CRUD operations
├── employees_info.py      # Employee management (Admin only)
├── banking_operations.py  # Banking transaction engine
└── status.py              # Account status management (Admin only)
```

---

# 3. System Requirements

## 3.1 Base Operating Environment

- Python **3.8** or later
- MySQL Server **8.0** or later
- Windows PowerShell, Command Prompt, Bash, or Zsh

---

## 3.2 Python Dependency

The application now uses **PyMySQL**, a pure-Python MySQL driver that improves portability and eliminates native driver compatibility issues.

Install it using:

```bash
pip install pymysql
```

---

# 4. Environment Configuration

## Step 1 — Configure Database Credentials

Open `connection.py` and update the database configuration with the appropriate credentials if required.

```python
config = {
    "host": "your_database_host",
    "user": "your_username",
    "password": "your_password",
    "database": "cbs"
}
```

> **Note:** If you're using the hosted database provided with the project, no local database setup or SQL script execution is required.

---

## Step 2 — Install Required Dependency

```bash
pip install pymysql
```

---

## Step 3 — Run the Application

```bash
python main.py
```


---

# 5. Running the Application

Launch the application using:

```bash
python main.py
```

---

# 5.1 Interactive Command Guide

| Command | Access Level | Description |
|----------|-------------|-------------|
| `-help` | Guest / Staff / Admin | Display available commands |
| `-clear` | Guest / Staff / Admin | Clear terminal screen |
| `-login` | Guest / Staff / Admin | Log into the system |
| `-customer` | Staff / Admin | Customer management |
| `-transaction` | Staff / Admin | Deposit, withdrawal, transfer, history |
| `-employee` | Admin Only | Employee management |
| `-status` | Admin Only | Modify account status |
| `-logout` | Staff / Admin | Logout current user |
| `-exit` | Guest / Staff / Admin | Exit application |

---

# 6. Troubleshooting

## 6.1 Cannot Connect to MySQL

### Symptom

```
Can't connect to MySQL server on 'localhost'
```

### Solution

Ensure the MySQL service is running.

Windows PowerShell:

```powershell
Start-Service -Name "mysql"
```

or manually start the service from **Services.msc**.

---

## 6.2 Invalid MySQL Credentials

### Symptom

```
Access denied for user 'root'@'localhost'
```

### Solution

Verify the credentials inside `connection.py`.

```python
config = {
    "host": "localhost",
    "user": "root",
    "password": "YourPasswordHere",
    "database": "cbs"
}
```

Ensure:

- Username is correct
- Password is correct
- Database name is `cbs`

---

## 6.3 Missing PyMySQL Driver

### Symptom

```
ModuleNotFoundError: No module named 'pymysql'
```

### Solution

Install PyMySQL:

```bash
python -m pip install pymysql
```

---

## 6.4 Unknown Database

### Symptom

```
Unknown database 'cbs'
```

### Solution

Execute the provided `cbs.sql` file.

Alternatively:

```sql
CREATE DATABASE cbs;
```

Then rerun `cbs.sql`.

---

# Technology Stack

- Python 3.8+
- MySQL Server 8.0+
- PyMySQL

---

# Features

- Secure Role-Based Access Control (RBAC)
- Authentication System
- Customer Management
- Employee Management
- Deposit Operations
- Withdrawal Operations
- Inter-account Transfers
- Transaction History
- Account Status Management
- ACID-Compliant Database Transactions
- Automatic Transaction Rollback
- Interactive Command-Line Interface (CLI)
- Pure-Python Database Driver (PyMySQL)

---

# Release Highlights

- Migrated from **mysql-connector-python** to **PyMySQL** for improved portability and runtime stability.
- Eliminated silent application exits by replacing forced process termination with graceful exception handling.
- Improved database connection diagnostics and authentication error reporting.
- Verified authentication workflow using the default seeded accounts included in `cbs.sql`.

---

# License

This project is developed for **educational, learning, and academic purposes**. It demonstrates the implementation of a simplified Core Banking System using Python, MySQL, and a modular command-line architecture.
