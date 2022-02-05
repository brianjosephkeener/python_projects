from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users
from flask import session
class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.name = data['name']


    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (description,instructions,under_30,name,users_id) VALUES (%(description)s,%(instructions)s,%(under_30)s,%(name)s,%(users_id)s);"
        result = connectToMySQL('exam_db').query_db(query,data)
        return result
    
    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL('exam_db').query_db(query,data)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results =  connectToMySQL('exam_db').query_db(query)
        all_recipes = []
        for row in results:
            all_recipes.append( cls(row) )
        return all_recipes

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM recipes WHERE id = %(id)s"
        result = connectToMySQL('exam_db').query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s,description=%(description)s,under_30=%(under_30)s,created_at=%(created_at)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('exam_db').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('exam_db').query_db(query,data)