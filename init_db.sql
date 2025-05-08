-- Drop old tables if they exist
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('student', 'teacher')) NOT NULL
);

-- Create classes table
CREATE TABLE classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES users(id)
);

-- Create enrollments table
CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    class_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (class_id) REFERENCES classes(id),
    UNIQUE(student_id, class_id)
);

-- Insert sample users
INSERT INTO users (username, password, role) VALUES 
('logan', 'pass123', 'student'),
('hunter', 'pass123', 'student'),
('aleczander', 'pass123', 'student'),
('mr_prof', 'pass123', 'teacher');

-- Insert sample classes (created by prof_jane who has ID = 3)
INSERT INTO classes (title, description, teacher_id) VALUES
('Intro to Python', 'Beginner programming class', 3),
('Web Development', 'HTML, CSS, JS Basics', 3);
