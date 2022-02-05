from flask import render_template, request, redirect, session, flash

from flask_app import app

from flask_app.models.users import User
from flask_app.models.recipes import Recipe

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    session['user_id'] = None
    return render_template("register_login.html")

@app.route('/register',methods=['POST'])
def registeruser():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "password":pw_hash,
        "email":request.form['email'],
    }
    print(request.form)
    print(data)
    User.save(data)
    return redirect("/")

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password", 'email/pass error')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", 'email/pass error')
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")

@app.route('/dashboard')
def loggedin():
    try: 
        id = session['user_id']
        data = {
            "id":id
            }
        return render_template('dashboard.html', user=User.get_one(data), recipes = Recipe.get_all())
    except: 
        return render_template('register_login.html')


@app.route('/logout',methods=['POST'])
def logout():
    session['user_id'] = None
    return redirect('/')



@app.route('/create/recipe')
def createrecipe():
    id = session['user_id']
    data = {
        "id":id
            }
    return render_template('create_recipe.html', user=User.get_one(data))

@app.route('/create_recipe', methods=['POST'])
def finalrecipe():
    data = {
        'users_id':session['user_id'],
        'description':request.form['description'],
        'instructions':request.form['instructions'],
        'under_30':request.form['under_30'],
        'created_at':request.form['created_at'],
        'name':request.form['name']
    }
    Recipe.save(data)
    return redirect('/create/recipe')

@app.route('/delete/<int:id>', methods=['POST'])
def deleterecipe(id):
    data = {
        'id':id
    }
    Recipe.delete(data)
    return redirect('/dashboard')

@app.route('/view/<int:id>')
def viewrecipe(id):
    data = {
        'id':id
    }
    recipe=Recipe.get_one(data)
    return render_template('view_recipe.html', recipe=recipe)

@app.route('/edit/<int:id>')
def editrecipelink(id):
    data = {
        'id':id
    }
    recipe=Recipe.get_one(data)
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/update/recipe',methods=['POST'])
def update():
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30": request.form["under_30"],
        "created_at": request.form["created_at"],
        "id": request.form['id']
    }
    Recipe.update(data)
    return redirect('/dashboard')

