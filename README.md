# Core Banking System (CBS) — Terminal Interface

The **Core Banking System (CBS)** is a modular, secure, multi-tier command-line interface (CLI) application engineered in **Python** and backed by a local **MySQL** relational database. The platform simulates mission-critical financial operations including **Role-Based Access Control (RBAC)**, customer profile lifecycle administration, atomic ledger transaction recording with ACID adherence, and administrative account security mitigation systems.

---

# 1. Core Engineering Architecture

### Role-Based Access Control (RBAC)
Restricts high-clearance execution segments (`-employee`, `-status`) strictly to users authenticated with **ADMIN** privileges, while permitting standard transactional access for banking **STAFF**.

### Atomic Financial Execution Engine
Ensures data integrity for cash updates including deposits (`CREDIT`), withdrawals (`DEBIT`), and inter-account transfers (`TRANSFER`) through structured query compilation.

### Transaction Rollback Protection
Employs programmatic `db.rollback()` exception handling routines during unexpected mid-transit execution or connection drops to eliminate ledger fragmentation and financial balance anomalies.

### Administrative Access Isolation
Implements a localized security subsystem allowing administrators to actively verify structural logs, implement `BLOCKED` account states, or reinstate an `ACTIVE` operational profile on targeted worker or client records.

### Comprehensive Master Ledger Auditing
Renders formatted tabular data schemas directly to the console window displaying comprehensive execution logs including sender, recipient, transactional classifications, chronological timestamps, and absolute valuations.

---

# 2. Project Directory Structure

```text
CBS-TERMINAL/
├── cbs.sql                # Master self-contained database schema initialization script
├── connection.py          # Relational database connector abstraction layer
├── login.py               # Authentication middleware and credential verification logic
├── help.py                # State-aware, role-contextual command dictionary
├── main.py                # Primary runtime application shell orchestrator
├── customer_info.py       # Customer data management (CRUD processes / Datagrids)
├── employees_info.py      # Workforce administration tools (Admin Clearance Restricted)
├── banking_operations.py  # Financial ledger transaction router
└── status.py              # Account state modification panel (Admin Clearance Restricted)
```

---

# 3. System Requirements

## 3.1 Base Operating Environment

- **Python Runtime:** Python 3.8 or higher
- **Database Management System:** MySQL Server 8.0 or higher
- **Terminal Shell:** PowerShell, Bash, Zsh, or Command Prompt with UTF-8 character encoding support

## 3.2 External Library Dependencies

The system relies on the official MySQL driver for secure database communication.

```text
mysql-connector-python
```

---

# 4. Environment Configuration & Installation

## Step 1: Database Initialization

Before launching the application, initialize the database.

1. Open **MySQL Workbench**.
2. Select **File → Open SQL Script**.
3. Open the provided **cbs.sql** file.
4. Execute the entire script.

This will:

- Create the required database.
- Create all tables.
- Configure foreign keys.
- Configure auto-increment values.
- Seed default records.

---

## Step 2: Configure Database Credentials

Open **connection.py** and update the configuration.

```python
# connection.py

config = {
    'host': 'localhost',
    'user': 'root',                 # Replace with your MySQL username
    'password': 'YourPasswordHere', # Replace with your MySQL password
}
```

---

## Step 3: Install Required Dependency

```bash
pip install mysql-connector-python
```

---

# 5. Deployment & Execution

Run the application using:

```bash
python main.py
```

---

## 5.1 Interactive Command Guide

| Command | Access Level | Description |
|---------|--------------|-------------|
| `-help` | Guest / Staff / Admin | Displays all available commands based on current login session. |
| `-clear` | Guest / Staff / Admin | Clears the terminal screen. |
| `-login` | Guest / Staff / Admin | Opens the secure login interface. |
| `-customer` | Staff / Admin | Customer management (Create, View, Update, Delete). |
| `-transaction` | Staff / Admin | Deposit, Withdrawal, Transfer, Transaction History. |
| `-employee` | **Admin Only** | Employee management interface. |
| `-status` | **Admin Only** | Change account status (ACTIVE / BLOCKED). |
| `-logout` | Staff / Admin | Ends the current user session. |
| `-exit` | Guest / Staff / Admin | Safely exits the application and closes the database connection. |

---

# 6. Troubleshooting

## 6.1 Database Connection Error

### Symptom

```text
mysql.connector.errors.InterfaceError:
2003: Can't connect to MySQL server on 'localhost'
```

### Solution

Ensure that your MySQL Server is running.

On Windows:

```powershell
Start-Service -Name "mysql"
```

Alternatively, open **Services.msc** and manually start the **MySQL** service.

---

## 6.2 Authentication Failure

### Symptom

```text
mysql.connector.errors.ProgrammingError:
1045 (28000): Access denied for user 'root'@'localhost'
```

### Solution

Verify the credentials inside `connection.py`.

Example:

```python
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YourPasswordHere'
}
```

Ensure:

- Username is correct.
- Password is correct.
- No extra spaces are present.

---

## 6.3 Missing Python Driver

### Symptom

```text
ModuleNotFoundError:
No module named 'mysql'
```

### Solution

Install the required driver.

```bash
python -m pip install mysql-connector-python
```

---

## 6.4 Missing Database

### Symptom

```text
mysql.connector.errors.ProgrammingError:
1049 (42000): Unknown database 'cbs'
```

### Solution

The database has not been created.

Execute the provided `cbs.sql` file or run:

```sql
CREATE DATABASE cbs;
```

Then rerun the SQL initialization script.

---

# Technology Stack

- Python 3.8+
- MySQL Server 8.0+
- mysql-connector-python

---

# Features

- Role-Based Access Control (RBAC)
- Secure Authentication System
- Customer Management
- Employee Management
- Deposit, Withdrawal & Transfer Operations
- Transaction History
- Account Status Control (ACTIVE/BLOCKED)
- ACID-Compliant Transactions
- Automatic Rollback Protection
- Console-Based Interactive Interface

---

# License

This project is intended for **educational and academic purposes**.
