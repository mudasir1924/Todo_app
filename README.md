
# Flask To-Do App

A simple web-based To-Do application built using 
Flask, 
MySQL (via PyMySQL), and 
HTML/CSS. It allows users to register, log in, manage tasks (add, edit, delete), and view their personal dashboard.

---

## Features

- User Registration and Login (with password hashing)
- Session-based user authentication
- Add, Edit, and Delete personal tasks
- Flash messages for feedback
- MySQL database integration using raw SQL (PyMySQL)

---

## Getting Started

1. set-up virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate


2. Install dependencies
   Flask: A lightweight web framework for Python, which you're using to build the web application.
   PyMySQL: A MySQL database connector for Python, allowing your application to interact with MySQL databases.
   Werkzeug: A utility library that Flask uses for various operations like password hashing.

3. MySQL Configuration
   db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root123",
    "database": "todo_db"
}

4. Create the database manually in MySQL:
   CREATE DATABASE todo_db;

5. Project Structure

6. flask-todo-app/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── update.html
│
├── static/
│   └── (Optional: CSS/JS files)
│
├── app.py
├── README.md
└── requirements.txt

  Running the app 
  python app.py

7. tech stack: 

  Backend: Flask
  Database: MySQL with PyMySQL (Raw SQL queries)
  Frontend: HTML, CSS (no Bootstrap)

- Authentication

  Passwords are hashed using werkzeug.security.
  Session-based authentication ensures users can only access their own data.



## Application Overview and Screenshots

Login Page Screenshot
![Login Page](https://Login.png)

Dashboard Screenshot  
![Dashboard](https://task.png)

Add Task Page Screenshot
![Add Task](https://task.png)


