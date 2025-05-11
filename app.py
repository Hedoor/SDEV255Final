from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
app = Flask(__name__)
print(app.template_folder)

with open('init_db.sql', 'r') as f:
    sql = f.read()

conn = sqlite3.connect('school.db')
conn.executescript(sql)
conn.close()

print("Database 'school.db' created and initialized.")


app = Flask(__name__)
app.secret_key = 'your-secret-key'

def get_db_connection():
    conn = sqlite3.connect('school.db')
    conn.row_factory = sqlite3.Row
    return conn

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            if user['role'] == 'teacher':
                return redirect('/teacher-dashboard')
            else:
                return redirect('/student-dashboard')
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

"""_______________________________________________"""

# STUDENT DASHBOARD
@app.route('/student-dashboard')
def student_dashboard():
    if 'username' in session and session.get('role') == 'student':
        conn = get_db_connection()
        all_classes = conn.execute("""
            SELECT * FROM classes
            WHERE id NOT IN (
                SELECT class_id FROM enrollments WHERE student_id = ?
            )
        """, (session['user_id'],)).fetchall()

        my_classes = conn.execute("""
            SELECT c.* FROM classes c
            JOIN enrollments e ON c.id = e.class_id
            WHERE e.student_id = ?
        """, (session['user_id'],)).fetchall()
        conn.close()

    return render_template('student_dashboard.html', all_classes=all_classes, my_classes=my_classes)

@app.route('/enroll/<int:class_id>', methods=['POST'])
def enroll(class_id):
    if session.get('role') != 'student':
        return "Unauthorized", 403
    conn = get_db_connection()
    conn.execute("INSERT INTO enrollments (student_id, class_id) VALUES (?, ?)", (session['user_id'], class_id))
    conn.commit()
    conn.close()
    return redirect('/student-dashboard')

@app.route('/drop/<int:class_id>', methods=['POST'])
def drop(class_id):
    if session.get('role') != 'student':
        return "Unauthorized", 403
    conn = get_db_connection()
    conn.execute("DELETE FROM enrollments WHERE student_id = ? AND class_id = ?", (session['user_id'], class_id))
    conn.commit()
    conn.close()
    return redirect('/student-dashboard')

"""_______________________________________________"""

# TEACHER DASHBOARD
@app.route('/teacher-dashboard')
def teacher_dashboard():
    if 'username' in session and session.get('role') == 'teacher':
        conn = get_db_connection()
        # Get all classes created by the teacher
        teacher_classes = conn.execute("SELECT * FROM classes WHERE teacher_id = ?", (session['user_id'],)).fetchall()
        conn.close()
        return render_template('teacher_dashboard.html', username=session['username'], teacher_classes=teacher_classes)
    return redirect('/login')


@app.route('/create-class', methods=['POST'])
def create_class():
    title = request.form['title']
    description = request.form['description']
    conn = get_db_connection()
    conn.execute("INSERT INTO classes (title, description, teacher_id) VALUES (?, ?, ?)", (title, description, session['user_id']))
    conn.commit()
    conn.close()
    return redirect('/teacher-dashboard')

@app.route('/edit-class/<int:class_id>', methods=['POST'])
def edit_class(class_id):
    if session.get('role') != 'teacher':
        return "Unauthorized", 403
    title = request.form['title']
    description = request.form['description']
    conn = get_db_connection()
    conn.execute("UPDATE classes SET title = ?, description = ? WHERE id = ? AND teacher_id = ?", (title, description, class_id, session['user_id']))
    conn.commit()
    conn.close()
    return redirect('/teacher-dashboard')

@app.route('/delete-class/<int:class_id>', methods=['POST'])
def delete_class(class_id):
    if session.get('role') != 'teacher':
        return "Unauthorized", 403
    conn = get_db_connection()
    conn.execute("DELETE FROM classes WHERE id = ? AND teacher_id = ?", (class_id, session['user_id']))
    conn.commit()
    conn.close()
    return redirect('/teacher-dashboard')

"""_______________________________________________"""

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

"""_______________________________________________"""

@app.route('/')
def home():
    return redirect('/login')

"""_______________________________________________"""

if __name__ == '__main__':
    app.run(debug=True)