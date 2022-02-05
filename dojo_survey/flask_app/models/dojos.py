from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
class Dojo:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.language = data['language']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls, data):
        query = "INSERT INTO dojos (name, location ,language ,comment ) VALUES (%(name)s,%(location)s,%(language)s,%(comment)s);"

        # comes back as the new row id
        result = connectToMySQL('dojo_survey_schema').query_db(query,data)
        return result

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM dojos WHERE name = %(name)s"
        result = connectToMySQL('dojo_survey_schema').query_db(query,data)
        return cls(result[0])

    @staticmethod
    def validate_dojo(dojo):
        is_valid = True
        if len(dojo['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        return is_valid