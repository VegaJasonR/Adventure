from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash , request
from flask_app.models import user, adventure


class Adventure:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.reward = data['reward']
        self.user_id = data['user_id']
        self.user = None
        self.completed = data['completed']
        self.times_completed = data['times_completed']

    @classmethod
    def get_all(cls, data):
        query = """
            SELECT *, (SELECT COUNT(user_id) FROM completed WHERE completed.adventure_id=adventures.id AND user_id=%(id)s) AS completed,
            (SELECT COUNT(user_id) FROM completed WHERE completed.adventure_id=adventures.id) AS times_completed FROM adventures
            LEFT JOIN users ON adventures.user_id=users.id
            ORDER BY times_completed DESC;"""

        results = connectToMySQL('schema_adventure').query_db(query, data)

        adventures = []

        for row in results:
            this_adventure = cls(row)

            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'username': row['username'],
                'email': row['email'],
                'password': row['password'],
            }
            this_adventure.user = user.User(user_data)

            adventures.append(this_adventure)

        return adventures
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO adventures
                    (title, description, reward, user_id)
                    VALUES
                    (%(title)s, %(description)s, %(reward)s, %(user_id)s);"""
        return connectToMySQL('schema_adventure').query_db(query, data)
    
    @classmethod
    def get_one(cls, data):
        print("data being passed into get one: ",data)
        query = """
                        SELECT a.*,
                (
                    SELECT COUNT(user_id)
                    FROM completed
                    WHERE completed.adventure_id=a.id
                    AND user_id=%(user_id)s
                )
            AS completed,
                (
                    SELECT COUNT(user_id)
                    FROM completed
                    WHERE completed.adventure_id=a.id
                )
            AS times_completed
            FROM adventures a
            LEFT JOIN users  u
            ON a.user_id=u.id
            WHERE a.id=%(adventure_id)s;
                        """
        results = connectToMySQL('schema_adventure').query_db(query, data)
    
        print("results from get one: ", results)

        if results:
            this_adventure = cls(results[0])

            # user_data = {
            #     'id': results[0]['user_id'],
            #     'first_name': results[0]['first_name'],
            #     'last_name': results[0]['last_name'],
            #     'username': results[0]['username'],
            #     'email': results[0]['email'],
            #     'password': results[0]['password'],
            # }
            
            # this_adventure.user = user.User(user_data)
            return this_adventure
        else:
            # Handle the case where results is not as expected
            return None

    
    @classmethod
    def update(cls, data):
        print("data in update: ", data)
        query = """
                    UPDATE adventures SET
                    title = %(title)s,
                    description = %(description)s,
                    reward = %(reward)s
                    WHERE
                    adventures.id = %(adventure_id)s"""
        result = connectToMySQL('schema_adventure').query_db(query,data)
        print("result in update", result)
        return result
    
    @classmethod
    def destroy(cls, id):
        query = "DELETE FROM adventures WHERE id=%(id)s"
        return connectToMySQL('schema_adventure').query_db(query, {"id":id})
    
    @staticmethod
    def validate_adventure(adventure):
        is_valid = True
        if len(adventure['title']) < 1: #cannot be blank
            flash("Gave your adventure a title!")
            is_valid= False
        if len(adventure['description']) < 1: # cannot be blank
            flash("Give it a description!")
            is_valid= False
        if len(adventure['reward']) < 1: # cannot be blank
            flash("What is the reward")
            is_valid= False

        return is_valid
    
    @classmethod
    def completed(cls, data):
        query = "INSERT INTO completed (user_id, adventure_id) VALUES (%(user_id)s,%(adventure_id)s);"
        return connectToMySQL('schema_adventure').query_db(query, data)
    
    @classmethod
    def not_completed(cls, data):
        query = "DELETE FROM completed WHERE user_id=%(user_id)s AND adventure_id=%(adventure_id)s;"
        return connectToMySQL('schema_adventure').query_db(query, data)