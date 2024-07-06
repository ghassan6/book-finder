
# instead of <state>

# @app.route("/read_list" , methods=["POST"])
# def read_list():
#     user_id = session['user_id']
#     id = request.get_json()
#     book = books[int(id)]

#     db.execute('''
#         INSERT OR REPLACE INTO lists (title , authors , img , desc , identifier , pages , category , date , user_id , list , add_date) 
#             VALUES (? , ? , ? , ? , ? , ? , ? , ? , ? , 'read' , DATE())
#             ''',
#                 book['title'],
#                 book['authors'],
#                 book['img'],
#                 book['desc'],
#                 book['identifier'],
#                 book['pages'],
#                 book['category'],
#                 book['date'],
#                 user_id,
#             )

#     return id


# instead of have read and want to read

# @app.route('/have-read')
# def have_read():
#     user_id = session['user_id']
#     name = db.execute('SELECT username FROM users WHERE id = ?' , user_id)[0]['username']

#     book_list = db.execute('''
#             SELECT * FROM books WHERE
#                      book_id IN ( 
#                            SELECT book_id FROM lists WHERE user_id = ? AND
#                                 state = 'have read' );
#                            ''' , 
#                            user_id)
    
#     return render_template('have-read.html' , name=name , books=book_list)


# @app.route('/want-to-read')
# def want_to_read():
#     user_id = session['user_id']
#     name = db.execute('SELECT username FROM users WHERE id = ?' , user_id)[0]['username']

#     book_list = db.execute('''
#             SELECT * FROM books WHERE
#                      book_id IN ( 
#                            SELECT book_id FROM lists WHERE user_id = ? AND
#                                 state = 'want to read' );
#                            ''' , 
#                            user_id) 
    
    
#     return render_template('want-to-read.html' , name=name , books=book_list)
