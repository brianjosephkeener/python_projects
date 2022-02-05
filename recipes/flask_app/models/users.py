from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models.recipes import Recipe
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  

import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user( user ):
        is_valid = True
        if not EMAIL_REGEX.match(user['email'] or user['email'] == None): 
            flash("Invalid email address!", 'register error')
            is_valid = False
        if (user['password'] != user['passwordcheck']):
            flash("passwords do not match", 'register error')
            is_valid = False
        if (len(user['first_name']) < 3):
            flash("first name must be at least 2 characters", 'register error')
            is_valid = False
        if (len(user['last_name']) < 3):
            flash("last name must be at least 2 characters", 'register error')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        # comes back as the new row id
        result = connectToMySQL('exam_db').query_db(query,data)
        return result

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("exam_db").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('exam_db').query_db(query)
        users = []
        for u in results:
            users.append( cls(u) )
        return users
    
    
    @classmethod
    def get_user_with_recipe(cls, data):
        query = "SELECT * FROM users JOIN recipes ON recipes.users_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL('exam_db').query_db(query,data)
        print("here are results", results)
        user = cls(results[0])
        for row in results:
            n = {
                'id': row['recipes.id'],
                'name':row['recipes.name'],
                'instructions':row['recipes.instructions'],
                'under_30':row['recipes.under_30'],
            }
            user.recipes.append(Recipe(n))
        return user
    



    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('exam_db').query_db(query,data)
        print(result[0])
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('exam_db').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('exam_db').query_db(query,data)