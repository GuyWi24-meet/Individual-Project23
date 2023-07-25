from flask import Flask, render_template, request, redirect, url_for, flash, session
import pyrebase

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure random key

# Firebase configuration details
config = { 
'apiKey': "AIzaSyDB9y26xcCgxl4E3gbFkaD935bE43rmx4g",
  'authDomain': "rogalachem.firebaseapp.com",
  'databaseURL': "https://rogalachem-default-rtdb.europe-west1.firebasedatabase.app/",
  'projectId': "rogalachem",
  'storageBucket': "rogalachem.appspot.com",
  'messagingSenderId': "286426368528",
  'appId': "1:286426368528:web:6a67e87b9cd50f3eaf5895",
  'measurementId': "G-SWDS6VP6GH"
};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
# Check if the user is logged in (session check)
def is_logged_in():
    return 'logged_in' in session and session['logged_in']

# Home page
@app.route('/')
def index():
    return render_template('home.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']

        try:
            user = auth.sign_in_with_email_and_password(username, password)
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        except:
            error = "Invalid credentials. Please try again."
            return render_template('login.html', error=error)

    return render_template('login.html')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']

        try:
            auth.create_user_with_email_and_password(username, password)
            session['logged_in'] = True  # Set the session status here
            return render_template('dashboard.html')
        except:
            error = "Error creating the account. Please try again."
            return render_template('signup.html', error=error)

    return render_template('signup.html')

# Dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))

    if request.method == 'POST':
        suggestion = request.form['suggestion']
        db.child('flavor_suggestions').push(suggestion)


    suggestions = db.child('flavor_suggestions').get().val()
    suggestions_list = []
    if suggestions:
        suggestions_list = (suggestions.values())

    return render_template('dashboard.html', suggestions=suggestions_list, flag = is_logged_in())

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
