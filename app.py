
import os
from flask import Flask , render_template , session , redirect , request
from cs50 import sql
from werkzeug.security import generate_password_hash , check_password_hash
from flask_session import Session


app = Flask(__name__)

print("asg")

@app.route("/")
def index():
    return render_template("index.html")