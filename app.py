from flask import Flask , render_template , session , redirect , request ,flash , jsonify , make_response , json
from cs50 import SQL
from werkzeug.security import generate_password_hash , check_password_hash
from flask_session import Session

from helpers import lookUp , get_category , add_book
# import requests


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
books = []
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///book.db")

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
        user_list = db.execute('''
            SELECT * FROM books INNER JOIN
                    lists ON
                        books.book_id = lists.book_id 
                               WHERE books.user_id = ?
                               ''',
                               session['user_id'])
        name = db.execute("SELECT username from users WHERE id = ?" , session["user_id"])[0]['username']
        return render_template("index.html" , name=name , books=user_list)
    
    
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
        
        rows = db.execute("SELECT * FROM users WHERE username = ?" , name)
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
        
        session.clear()
        session["user_id"] = rows[0]["id"]
        
        # return render_template('index.html' , name=name)
        return redirect('/')


    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()

    return redirect('/')


@app.route("/change" , methods=["POST" , "GET"])
def change():
    if request.method == "POST":
        old = request.form.get("old-password")
        new = request.form.get("new")
        confirm = request.form.get("confirm")
        flag = request.form.get("register")
        rows = db.execute("SELECT * FROM users WHERE id = ?" , session["user_id"])

        if not old or not new or not confirm:
            flash("Can't have a blank field" , "error")
            return redirect("/change")
        
        if not check_password_hash(rows[0]["hash"] , old):
            flash("Old password is incorrect" , "error")
            return redirect("/change")
        
        if new != confirm:
            flash("Passwords do not match" , "error")
            return redirect("/change")
        if (flag == 'false'):
            flash("Invalid password" , "error")
            return redirect("/change")
        
        db.execute("UPDATE users SET hash = ? WHERE id = ?" , generate_password_hash(new) , session["user_id"])
        return redirect('/')


    name = db.execute("SELECT username from users WHERE id = ?" , session["user_id"])[0]['username']
    return render_template("change-password.html" , name=name)


@app.route("/result" , methods=["POST"])
def result():
    books.clear()
    req = request.get_json()
    for book in req:
        books.append(book)
    
    return req
          

@app.route("/search")
def search():
    if (session):
        name = db.execute("SELECT username from users WHERE id = ?" , session["user_id"])[0]['username']
        return render_template("search.html" , books=books , name=name)
    
    
    return render_template("search.html" , books=books)

@app.route("/info/<int:id>")
def info(id):
    book = books[id]
    category = get_category(book) 

    if(session):
        name = db.execute("SELECT username from users WHERE id = ?" , session["user_id"])[0]['username']
        return render_template("info.html" , book=books[id] , name=name , category=category)

    return render_template("info.html" , book=books[id] ,  category=category)


@app.route("/article/<article_id>")
def article(article_id):
    print(article_id)
    return render_template(f"/article/{article_id}.html")

@app.route('/contact')
def contact():
    if (session):
        name = db.execute("SELECT username from users WHERE id = ?" , session["user_id"])[0]['username']
        return render_template("contact.html" , name=name)
    
    return render_template('contact.html')
    
@app.route('/contact/feedback' , methods=["POST"])
def feedback():
    req = request.get_json()
    filename = 'static/data/messages.json'

    with open(filename , 'r') as f:
        msg = json.load(f)
      
    with open(filename , "w") as file:
        msg["messages"].append(req)
        json.dump(msg , file , indent=4)

    return req
   

@app.route('/add_list/<state>' , methods=["POST"])
def add_list(state):
    user_id = session['user_id']
    id = request.get_json()
    book = books[int(id)]

    add_book(db , book , user_id , state)
    return id

@app.route('/lists/<list>')
def lists(list):
    user_id = session['user_id']
    name = db.execute('SELECT username FROM users WHERE id = ?' , user_id)[0]['username']
    state = list.replace('-' , ' ')
    book_list = db.execute('''
            SELECT * FROM books WHERE
                     book_id IN ( 
                           SELECT book_id FROM lists WHERE user_id = ? AND
                                state = ? );
                           ''' , 
                           user_id,
                           state)
    
    return render_template(f'lists/{list}.html' , name=name , books=book_list)


@app.route('/delete' , methods=["POST"])
def delete():
    q = request.get_json()

    db.execute('''
        DELETE FROM lists 
               WHERE book_id = ? 
               AND user_id = ?
               ''' ,
               int(q),
               session['user_id']
               )
    
    db.execute('''
    DELETE FROM books 
               WHERE book_id = ? 
               AND user_id = ?
               ''' ,
               int(q),
               session['user_id'])

    return q


if __name__ == "__main__":
    app.run(debug=True)
