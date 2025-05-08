from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

# Define custom paths for templates and static files
template_folder= "/Users/ltill/Desktop/ivyTech/spring2025/Website SDEV255/templates"
static_folder= "/Users/ltill/Desktop/ivyTech/spring2025/Website SDEV255/static"

# Initialize Flask app with custom paths
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

# Connect to SQLite database
def get_db():
    conn = sqlite3.connect('database.db')
    return conn

# Initialize the database
def init_db():
    conn = get_db()
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS courses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            description TEXT NOT NULL,
                            teacher_id INTEGER NOT NULL)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS teachers (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            password TEXT NOT NULL)''')
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()
    conn.close()
    return render_template('index.html', courses=courses)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form['name']
        description = request.form['description']
        teacher_id = 1  # Placeholder for teacher ID
        conn = get_db()
        conn.execute('INSERT INTO courses (name, description, teacher_id) VALUES (?, ?, ?)',
                     (course_name, description, teacher_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_course.html')

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
    course = cursor.fetchone()
    conn.close()
    return render_template('course_detail.html', course=course)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


@app.route('/delete_course/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    conn = get_db()
    conn.execute('DELETE FROM courses WHERE id = ?', (course_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

