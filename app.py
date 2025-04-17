from flask import Flask, render_template, request, redirect, session, url_for, flash
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ---------- Database Config ----------
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root123",
    "database": "todo_db"
}

def get_db():
    return pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)

# ---------- Create Tables ----------
def create_tables():
    db = get_db()
    with db.cursor() as cursor:

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE,
        password VARCHAR(500)  
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            title VARCHAR(255),
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )""")
    db.commit()
    db.close()

# ---------- Routes ----------

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    create_tables()
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            if cursor.fetchone():
                flash("Username already exists")
                db.close()
                return redirect(url_for('register'))

            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
        db.close()
        flash("Registered successfully! Please log in.")
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    create_tables()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                db.close()
                return redirect(url_for('dashboard'))
        db.close()
        flash("Invalid credentials")
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    with db.cursor() as cursor:
        
        cursor.execute("SELECT * FROM tasks WHERE user_id=%s ORDER BY lastupdated DESC", (session['user_id'],))
        tasks = cursor.fetchall()
    db.close()
    return render_template("dashboard.html", tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    title = request.form['title']
    description = request.form['description']

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("INSERT INTO tasks (user_id, title, description) VALUES (%s, %s, %s)",
                       (session['user_id'], title, description))
        db.commit()
    db.close()
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:id>')
def delete_task(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM tasks WHERE id=%s AND user_id=%s", (id, session['user_id']))
        db.commit()
    db.close()
    return redirect(url_for('dashboard'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        with db.cursor() as cursor:
            cursor.execute("UPDATE tasks SET title=%s, description=%s WHERE id=%s AND user_id=%s",
                           (title, description, id, session['user_id']))
            db.commit()
        db.close()
        return redirect(url_for('dashboard'))

    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks WHERE id=%s AND user_id=%s", (id, session['user_id']))
        task = cursor.fetchone()
    db.close()
    return render_template("update.html", task=task)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
