from flask import Flask, render_template, request, redirect
import psycopg2
import hashlib

app = Flask(__name__)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="cse412_passwordEncryptDemo",  # Replace with your database name
    user="postgres",          # Replace with your PostgreSQL username
    password="1234", # Replace with your PostgreSQL password
    host="localhost",
    port="5432"
)

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    student_id = request.form['student_id']
    university = request.form['university']
    course = request.form['course']
    username = request.form['username']
    password = request.form['password']
    
    hash_object = hashlib.sha256() # Create 256 bit hash object
    hash_object.update(password.encode()) #Convert pw to bytes, add the hash object
    hashed_password = hash_object.hexdigest() #Convert hashed password to hex

    try:
        cur = conn.cursor()
        # Insert data into the table
        cur.execute("""
            INSERT INTO students (first_name, last_name, student_id, university, course, username, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, student_id, university, course, username, hashed_password)) #Now inserts the hashed_password into DB
        conn.commit()
        cur.close()
        return redirect('/show_entries')
    except Exception as e:
        return f"Error: {e}"

@app.route('/show_entries')
def show_entries():
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    cur.close()
    return render_template('entries.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
