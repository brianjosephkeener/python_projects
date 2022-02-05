from flask import render_template, request, redirect, flash

from flask_app import app

from flask_app.models.dojos import Dojo

@app.route('/')
def index():
    return render_template("dojos.html")