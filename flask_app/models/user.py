from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

from flask_app.models import adventure, user
from flask_app.models.adventure import Adventure

# Regular expression pattern for validating email addresses
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data) -> None:
        # Initialize user attributes
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.adventures = [] # holds adventure list

    # Get all users from the database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('schema_adventure').query_db(query)
        
        users = []
        for row in results:
            users.append(cls(row))

        return users
    
    # Save a new user to the database
    @classmethod
    def save(cls, data):
        query = """INSERT INTO
                        users
                    (first_name, last_name, username, email, password)
                        VALUES
                    ( %(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s)"""
        return connectToMySQL('schema_adventure').query_db(query, data)
    
    # Get a user by their username
    @classmethod
    def get_by_username(cls,data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL('schema_adventure').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    # Get a user by their ID
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('schema_adventure').query_db(query,data)
        return cls(results[0])

    # Validate user input before saving to the database
    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        
        results = connectToMySQL('schema_adventure').query_db(query,user)

        if len(results) >= 1:
            flash("E-mail already taken.")
            is_valid = False

        if len(results) >= 1:
            flash("Username already taken.")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email format")
            is_valid = False

        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters")
            is_valid= False
        
        if len(user['last_name']) < 2:
                flash("Last name must be at least 2 characters")
                is_valid= False
        
        if len(user['username']) < 2:
            flash("First name must be at least 2 characters")
            is_valid= False

        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords do not match")

        return is_valid
    
    # Get all adventures associated with a user
    @classmethod
    def get_user_adventures(cls, data):
        query = "SELECT * FROM users LEFT JOIN adventures ON users.id=adventures.user_id WHERE users.id=%(id)s"
        results = connectToMySQL('schema_adventure').query_db(query, data)
        user = cls(results[0])
        for adventure in results:
            adventure_data = {
                'id': adventure['adventures.id'],
                'title': adventure['title'],
                'description': adventure['description'],
                'reward': adventure['reward'],
                'user_id': adventure['user_id'],
                'completed': None,
                'times_completed': None
            }
            this_adventure = Adventure(adventure_data)
            user.adventures.append(this_adventure)
        return user