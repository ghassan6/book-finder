from flask import session , redirect , render_template
from functools import wraps
from cs50 import SQL


def lookUp(book):
        if book.get('ISBN') == None:
             return "None"
        if book["ISBN"][0]["type"] == "OTHER":
            return f'Other: {book["ISBN"][0]["identifier"]}'
        if len(book["ISBN"]) == 1:
            return f'ISBN: {book["ISBN"][0]["identifier"]}'
        else:
            return f'ISBN: {book["ISBN"][1]["identifier"]}'

def get_category(book):
     if len(book['category']) == 0:
          return 
     else:
          return book["category"][0]
     

def login_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
     
def add_book(db , book , user_id , state):
     
     db.execute('''
        INSERT OR REPLACE INTO books (title , authors , img , desc , identifier , pages , category , date , user_id , google ) 
            VALUES (? , ? , ? , ? , ? , ? , ? , ? , ? , ?)
            ''',
            book['title'],
            book['authors'],
            book['img'],
            book['desc'],
            book['identifier'],
            book['pages'],
            book['category'],
            book['date'],
            user_id,
            book['googleLink']
            )
     b_id = db.execute('SELECT book_id FROM books WHERE title = ? AND identifier = ? AND user_id = ?' , book['title'] , book['identifier'] , user_id)[0]['book_id']

     db.execute('''
            INSERT INTO lists (book_id , user_id , state)
                VALUES (? , ? , ?)
                ''' , 
                b_id ,
                user_id , 
                state)
     
    