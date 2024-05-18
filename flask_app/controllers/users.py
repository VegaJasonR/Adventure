from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models import adventure
from flask_app.models.adventure import Adventure
from flask_app.controllers import adventures

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for user registration
@app.route('/register', methods=['POST'])
def register():

    # Validate user input data
    if not User.validate_user(request.form):
        return redirect('/')

    # Hash the password before saving
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    # Prepare user data for registration
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "username": request.form['username'],
        "email": request.form['email'],
        "password": pw_hash
    }

    # Save the user data and get the user ID
    id = User.save(data)

    # Set the user ID in the session
    session['user_id'] = id

    return redirect('/dashboard')

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    # Check if the user exists
    user = User.get_by_username(request.form)

    if not user:
        flash("Invalid Username")
        return redirect('/')
    
    # Check if the password is correct
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')
    
    print(user.id)
    session['user_id'] = user.id

    return redirect('/dashboard')

# Route for the user dashboard
@app.route('/dashboard')
def dashboard():
    # Redirect to logout if user is not logged in
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id': session['user_id']
    }

    # Get user details and adventures for the dashboard
    user = User.get_by_id(data)  # Retrieve the user object
    adventures = adventure.Adventure.get_all(data)

    return render_template("dashboard.html", user=user, adventures=adventures)

# Route for viewing a specific user
@app.route('/users/<int:id>')
def view_user(id):
    # Redirect to logout if user is not logged in
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id': id
    }

    # Get user details and adventures for the specific user view
    user = User.get_user_adventures(data)
    
    return render_template("view_user.html", user=user)

# Route for user logout
@app.route('/logout')
def logout():
    # Clear the session data on logout
    session.clear()
    return redirect('/')