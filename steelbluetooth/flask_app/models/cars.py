from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users
from flask import session, flash
class Car:
    def __init__(self, data):
        self.id = data['id']
        self.description = data['description']
        self.make = data['make']
        self.model = data['model']
        self.year = data['year']
        self.price = data['price']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_car( car ):
        is_valid = True
        if (len(car['model']) < 1):
            flash("car model is required")
            is_valid = False
        if (len(car['make']) < 1):
            flash("car make is required")
            is_valid = False
        if (len(car['description']) < 1):
            flash("description is required")
            is_valid = False
        try: #int and float conversion does not work for input type "number" as required by wireframe for year and price. This was handled with a min and max in the html. However, if the min and max was removed in the html the remaining try and exempt conditions would still work. 
            if (int(car['price']) < 1):
                flash(f"{car['price']} price must be greater than 0")
                is_valid = False
        except:
            flash(f"{car['price']} price must be greater than 0")
            is_valid = False
        try: 
            if (int(car['year']) < 1):
                flash(f"{car['year']} price must be greater than 0")
                is_valid = False
        except:
            flash(f"{car['year']} year must be greater than 0")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO cars (description,model,price,user_id,make,year) VALUES (%(description)s,%(model)s,%(price)s,%(user_id)s,%(make)s,%(year)s);"
        result = connectToMySQL('steelbt_db').query_db(query,data)
        return result
    
    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM cars WHERE id = %(id)s;"
        result = connectToMySQL('steelbt_db').query_db(query,data)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars;"
        results =  connectToMySQL('steelbt_db').query_db(query)
        all_paintings = []
        for row in results:
            all_paintings.append( cls(row) )
        return all_paintings

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM cars WHERE id = %(id)s"
        result = connectToMySQL('steelbt_db').query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE cars SET model=%(model)s,make=%(make)s,price=%(price)s,year=%(year)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('steelbt_db').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('steelbt_db').query_db(query,data)