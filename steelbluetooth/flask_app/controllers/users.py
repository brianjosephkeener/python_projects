from flask import render_template, request, redirect, session, flash
from flask_app import app
import bluetooth
from flask_app.models.users import User
from flask_app.models.cars import Car

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

def randomString(): 
    result = ''.join((random.choice(string.ascii_letters) for x in range(20)))
    return result

@app.route('/')
def index():
    session['user_id'] = None
    return render_template("index.html", register=0, login=0)

@app.route('/registerpop')
def registerpop():
    session['user_id'] = None
    return render_template("index.html", register=1, login=0)

@app.route('/loginpop')
def loginpop():
    session['user_id'] = None
    return render_template("index.html", register=0, login=1)

@app.route("/profile/<username>/")
def profile(username):
    if session['user_id'] == None:
        return redirect('/')
    id = session['user_id']
    session['username'] = username
    data = {
        "id":id
            }
    return render_template("user.html", user=User.get_one(data), username=username, VideoID='liJVSwOiiwg')

@app.route('/addvideo', methods=['POST'])
def addingvideo():
    VideoID = request.form['addvideo']
    username = session['username']
    return redirect(f"/profile/{username}/{VideoID}")


@app.route("/profile/<username>/<VideoID>")
def videoadd(username, VideoID):
    if session['user_id'] == None:
        return redirect('/')
    id = session['user_id']
    data = {
        "id":id
            }
    return render_template("user.html", user=User.get_one(data), username=username, VideoID=VideoID)


@app.route('/register',methods=['POST'])
def registeruser():
    if not User.validate_user(request.form):
        return redirect('/registerpop')
    data = { "username" : request.form["username"] }
    user_in_db = User.get_by_username(data)
    if user_in_db:
        flash("Username taken", "register error")
        return redirect('/registerpop')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "username": request.form['username'],
        "password":pw_hash,
    }
    print(request.form)
    print(data)
    User.save(data)
    return redirect("/")

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "username" : request.form["username"] }
    user_in_db = User.get_by_username(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Username/Password", 'email/pass error')
        return redirect("/loginpop")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Username/Password", 'email/pass error')
        return redirect('/loginpop')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    username = user_in_db.username
    return redirect(f"/profile/{username}")

@app.route('/dashboard')
def logg():
    if session['user_id'] == None:
        return redirect('/')
    id = session['user_id']
    data = {
        "id":id
            }
    return render_template('dashboard.html', user=User.get_one(data), cars = Car.get_all(), car_many = User.get_user_with_car())


@app.route('/logout',methods=['POST'])
def logout():
    session['user_id'] = None
    session['username'] = None
    return redirect('/')



