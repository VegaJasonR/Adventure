from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_app import app
from flask_app.models.adventure import Adventure
from flask_app.controllers import users

from flask_app.models import user
from flask_app.models.user import User

# Route for adding a new adventure
@app.route('/adventures/add', methods=['GET', 'POST'])
def add_adventure():
    # Display the form to add a new adventure
    if request.method == 'GET':
        return render_template("add_adventure.html")

    # Validate the form data before adding the adventure
    if not Adventure.validate_adventure(request.form):
        flash("Invalid data. Please check your input.", "error")
        return redirect("/adventures/add")  # Redirect back to the add adventure page if data is invalid

    # Save the adventure data
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'reward': request.form['reward'],
        'user_id': request.form['user_id']
    }
    Adventure.save(data)
    flash("Adventure added successfully.", "success")
    return redirect("/dashboard")

# Route for viewing a specific adventure
@app.route("/adventures/<int:id>")
def view_adventure(id):
    data = {
        'adventure_id': id,
        'user_id': session["user_id"]
    }
    adventure = Adventure.get_one(data)
    return render_template("view_adventure.html", adventure=adventure)

# Route for updating an existing adventure
@app.route("/adventures/<int:id>/update", methods=["GET", "POST"])
def update_adventure(id):
    if request.method == 'GET':
        data = {
            "user_id": session["user_id"],
            "adventure_id": id
        }
        adventure = Adventure.get_one(data)
        print("adventure data for edit page: ", adventure)
        return render_template("update_adventure.html", adventure=adventure)
    
    if not Adventure.validate_adventure(request.form):
        return redirect(f'/adventures/{id}/update')
    
    data = {
        'adventure_id': id,
        'title': request.form['title'],
        'description': request.form['description'],
        'reward': request.form['reward']
    }
    adventure = Adventure.update(data)
    return redirect("/dashboard")

# Route for marking an adventure as completed
@app.route("/adventures/<int:id>/completed")
def completed(id):
    data = {
        "user_id": session["user_id"],
        "adventure_id": id
    }
    Adventure.completed(data)
    return redirect("/dashboard")

# Route for marking an adventure as not completed
@app.route("/adventures/<int:id>/not_completed")
def not_completed(id):
    data = {
        "user_id": session["user_id"],
        "adventure_id": id
    }
    Adventure.not_completed(data)
    return redirect("/dashboard")

# Route for deleting an adventure
@app.route("/adventures/<int:id>/delete")
def destroy_adventure(id):
    Adventure.destroy(id)
    return redirect("/dashboard")