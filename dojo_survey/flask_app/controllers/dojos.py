from flask import render_template, request, redirect, session

from flask_app import app

from flask_app.models.dojos import Dojo

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/show_result/<name>')
def showresult(name):
    data = { 
        "name":name
    }
    return render_template("showresult.html", dojo=Dojo.get_one(data))

@app.route('/dojo_create')
def create():
    print(request.form)
    Dojo.save(request.form)
    session['name'] = request.form['name']
    return redirect('/show_result/<name>', name = session['name'])