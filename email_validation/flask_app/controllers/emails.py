from flask import render_template, request, redirect

from flask_app import app

from flask_app.models.emails import Email

@app.route('/')
def email():
    return render_template("email.html")

@app.route('/create_email',methods=['POST'])
def createemail():
    print(request.form)
    if not Email.validate_email(request.form):
        return redirect('/')
    Email.save(request.form)
    return redirect('/success')

@app.route('/success')
def success():
    return render_template("success.html",emails=Email.get_all())
