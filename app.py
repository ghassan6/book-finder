
import os
from flask import Flask , render_template , session , redirect , request ,flash
from cs50 import SQL
from werkzeug.security import generate_password_hash , check_password_hash
from flask_session import Session


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///book-finder.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    if (session):
        name = db.execute("SELECT username from users WHERE id = ?" , session["user_id"])
        return render_template("index.html" , name=name[0]["username"])

    
    return render_template("index.html")

@app.route("/register", methods=["GET" , "POST"])
def register():

    
    if request.method == "POST":
        name = request.form.get('username')
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        flag = request.form.get("register")
        rows = db.execute("SELECT * FROM users")
        if not name:
            flash("please enter a username!" , "error")
            return redirect('/register')

        if not password:
            flash("Please Enter a password!" , "error")
            return redirect('/register')
        
        if (flag == 'false'):
            flash("invalid password" , "error")
            return redirect("/register")
        
        if confirmation != password:
            flash("Passwords do not match!" ,"error")
            return redirect('/register')
        
        for key in rows:
            if (name == key["username"]):
                flash("Username is taken" , "error")
                return redirect('/register')
        
        db.execute("INSERT INTO users (username , hash) VALUES (? , ?) " , 
                   name , generate_password_hash(password))
        
        rows = db.execute("SELECT * FROM users")
        session["user_id"] = rows[0]["id"]
        return redirect("/")
        
        


    return render_template("register.html")


@app.route('/login' , methods=["GET" , "POST"])
def login():
    # why not working?
    # session.clear()

    if request.method == "POST":
        name = request.form.get('username')
        password = request.form.get('password')
        rows = db.execute("SELECT * FROM users WHERE username = ?" , name)

        if not name or not password:
            flash("Must provide a name and a password" , "error")
            return redirect('/login')
        if (len(rows) != 1 or not check_password_hash(rows[0]["hash"] , password)):
            flash("invalid name or/and password" , "error")
            return redirect('/login')
        
        session["user_id"] = rows[0]["id"]
        
        return render_template('index.html' , name=name)


    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()

    return redirect('/')
