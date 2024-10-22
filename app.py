from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home page (Read operation)
@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)

# Create a new student (Create operation)
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO students (name, age) VALUES (?, ?)', (name, age))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    return render_template('create.html')

# Update a student (Update operation)
@app.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        
        conn.execute('UPDATE students SET name = ?, age = ? WHERE id = ?', (name, age, id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('update.html', student=student)

# Delete a student (Delete operation)
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Initialize the database
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL
                    );''')
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
