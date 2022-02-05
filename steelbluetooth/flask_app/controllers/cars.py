from flask import render_template, request, redirect, session, flash

from flask_app import app

from flask_app.models.users import User
from flask_app.models.cars import Car


@app.route('/create/car')
def createcar():
    if session['user_id'] == None:
        return redirect('/')
    id = session['user_id']
    data = {
        "id":id
            }
    return render_template('create_car.html', user=User.get_one(data))

@app.route('/create_car', methods=['POST'])
def finalcar():
    if not Car.validate_car(request.form):
        return redirect('/create/car')
    id = session['user_id']
    data = {
        'user_id':session['user_id'],
        'description':request.form['description'],
        'price':request.form['price'],
        'model':request.form['model'],
        'make':request.form['make'],
        'year':request.form['year']
    }
    Car.save(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def deletecar(id):
    data = {
        'id':id
    }
    Car.delete(data)
    return redirect('/dashboard')

@app.route('/view/<int:id>')
def viewcar(id):
    if session['user_id'] == None:
        return redirect('/')
    data = {
        'id':id
    }
    car=Car.get_one(data)
    data_seller = {
        'id':car.user_id
    }
    user=User.get_one(data_seller)
    return render_template('view_car.html', car=car, user=user)

@app.route('/edit/<int:id>')
def editcarlink(id):
    if session['user_id'] == None:
        return redirect('/')
    data = {
        'id':id
    }
    car=Car.get_one(data)
    return render_template('edit_car.html', car=car)

@app.route('/update/car',methods=['POST'])
def update():
    if not Car.validate_car(request.form):
        return redirect('/dashboard')
    data = {
        "model": request.form["model"],
        "make": request.form["make"],
        "year": request.form["year"],
        "description": request.form["description"],
        "price": request.form["price"],
        "id": request.form['id']
    }
    Car.update(data)
    return redirect('/dashboard')