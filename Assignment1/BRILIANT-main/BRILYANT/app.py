from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a secure key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        
        if user:
            session['username'] = username
            flash('Login successful! Welcome to your dashboard.', 'success')
            return redirect(url_for('grades'))
        else:
            flash('Login failed. Please register first or check your credentials.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/grades')
def grades():
    if 'username' not in session:
        flash('Please log in to view your grades.', 'danger')
        return redirect(url_for('login'))

    # Read grades from CSV file
    try:
        df = pd.read_csv('grades.csv')
        # Optionally filter grades by username if needed
        grades = df.to_html(classes='grades_table', index=False)  # Added CSS class for styling
        return render_template('grades.html', grades=grades)
    except Exception as e:
        flash(f'Error reading grades: {str(e)}', 'danger')
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
