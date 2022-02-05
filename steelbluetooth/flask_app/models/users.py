from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models.cars import Car
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  

import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.cars = []
        self.users = []

    @staticmethod
    def validate_user( user ):
        is_valid = True
        if (user['password'] != user['passwordcheck']):
            flash("passwords do not match", 'register error')
            is_valid = False
        if (len(user['password']) < 7):
            flash("password must be at least 8 characters", 'register error')
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (username,password) VALUES (%(username)s,%(password)s);"
        # comes back as the new row id
        result = connectToMySQL('steelbt_db').query_db(query,data)
        return result

    @classmethod
    def get_by_username(cls,data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        result = connectToMySQL("steelbt_db").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])



    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('steelbt_db').query_db(query)
        users = []
        for u in results:
            users.append( cls(u) )
        return users


    
    @classmethod
    def get_user_with_car(cls):
        query = "SELECT * FROM users JOIN cars ON cars.user_id = users.id"
        results = connectToMySQL('steelbt_db').query_db(query)
        u_cars = []
        for users_cars in results:
            user_instance = User(users_cars)
            car_data = {
                "id":users_cars["cars.id"],
                "model":users_cars["model"],
                "make":users_cars["make"],
                "year":users_cars["year"],
                "description":users_cars["description"],
                "price":users_cars["price"],
                "user_id":users_cars["user_id"],
                "created_at":users_cars["cars.created_at"],
                "updated_at":users_cars["cars.updated_at"]
            }
            user_instance.car = Car(car_data)
            u_cars.append(user_instance)
        return u_cars

    @classmethod
    def get_specific_user_with_car(cls, data):
        query = "SELECT * FROM users JOIN cars ON cars.user_id = users.id WHERE users.id = %(id)s"
        results = connectToMySQL('steelbt_db').query_db(query,data)
        u_cars = cls(results[0])
        for users_cars in results:
            user_data = {
                "id":users_cars["id"],
                "first_name":users_cars["first_name"],
                "last_name":users_cars["last_name"],
                "email":users_cars["email"],
                "model":users_cars["model"],
                "password":users_cars["password"],
                "created_at":users_cars["created_at"],
                "updated_at":users_cars["updated_at"],
            }
            car_data = {
                "id":users_cars["id"],
                "user_id":users_cars["user_id"],
                "created_at":users_cars["created_at"],
                "updated_at":users_cars["updated_at"],
                "model":users_cars["model"],
                "make":users_cars["make"],
                "year":users_cars["year"],
                "description":users_cars["description"],
                "price":users_cars["price"],
            }
            u_cars.users.append(User(user_data))
            u_cars.cars.append(Car(car_data))
            print("this is the print", u_cars)
        return u_cars

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('steelbt_db').query_db(query,data)
        print(result[0])
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('steelbt_db').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('steelbt_db').query_db(query,data)