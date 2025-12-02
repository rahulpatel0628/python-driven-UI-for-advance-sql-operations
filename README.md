# 🚀 Python + Streamlit + MySQL — Advanced Database Operations UI

A complete **web-based SQL management system** built using **Python, Streamlit, and MySQL**.  
This project enables users to perform advanced SQL operations through a **simple and interactive UI** — without writing SQL manually.

---

## 📌 Features Overview

### ✅ **1. Advanced MySQL Backend**
The project includes:

- Fully structured relational database  
- **Views** for simplified query logic  
- **Stored Procedures** for CRUD operations  
- **Functions** for validation and calculations  
- **Transactions** (COMMIT/ROLLBACK)  
- **Joins** and multi-table relationships  

---

### ✅ **2. Streamlit Web UI**
User-friendly interface to perform:

- View tables and records  
- Insert new records  
- Update existing rows  
- Delete records safely  
- Execute stored procedures  
- Fetch data from SQL views  
- Perform advanced operations instantly  

All without writing a single SQL query.

---

### ✅ **3. Online MySQL Support**
This project works on **local machine** and also supports **Streamlit Cloud deployment** using an online MySQL service.

Secrets are stored as:

```toml
[mysql]
host = "your_online_mysql_host"
user = "your_user"
password = "your_password"
database = "your_db"
port = 3306
```

# Project Architecture
```nginx
Streamlit UI  →  Python Backend  →  Online MySQL Database
```

# Tech Stack
  - Streamlit
  - Python
  - Mysql
  - Advance Sql operation(Views, Stored Procedures, Functions, Transactions)
  - Deployement on streamlit cloude
# ⚙️ Installation & Local Setup
## 1️⃣ Clone Repository
```bash
git clone https://github.com/rahulpatel0628/python-driven-UI-for-advance-sql-operations.git
cd python-driven-UI-for-advance-sql-operations
```
## 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
## 3️⃣ Setup Local Databas
```bash
mysql -u root -p < database.sql
```
## 4️⃣ Add Streamlit Secrets (Local)
```toml
[mysql]
host = "localhost"
user = "root"
password = "your_password"
database = "your_db"
port = 3306
```
# 🌐 Deploy on Streamlit Cloud
## 1️⃣ Push project to GitHub
## 2️⃣ Create Online MySQL Database (Railway )
## 3️⃣ Add secrets in Streamlit Cloud:
```toml
[mysql]
host = "your_online_host"
user = "root"
password = "your_password"
database = "dbname"
port = 12345
```
## 4️⃣ Deploy → Your App is live 🎉

# 🎯 Use Cases

- Inventory management

- Admin dashboard

- E-commerce databases

- Student/employee management

- CRUD-based applications

- SQL + Python teaching projects

# 📚 Skills Demonstrated

- Streamlit web development

- Python + MySQL integration

- Stored procedures & triggers

- Advanced SQL logic

- Transactions handling

- Deployment with cloud DB

- End-to-end system design
