import os
import psycopg2
import requests

from flask import Flask, session,redirect,request,flash,url_for,render_template,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from forms import LoginForm,ReviewForm,RegistrationForm,SearchForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,validators
from db import Database

# from import.py import users

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# login_manager.init_app(app)
login_manager.login_view = 'login'
# login_manager.login_message ='Please login to access this page!'
login_manager.login_message_category = 'info'
# login_manager.session_protection = 'strong'

# connect to the database
db = Database()

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# # Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# # Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def home():
    return render_template('home.html')

#register a new user
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('books'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit:
        pwd_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.execute(f"INSERT INTO users(username,email,password) VALUES('{form.username.data}','{form.email.data}','{pwd_hash}')")
        db.commit()
        flash('Your account has been created! Welcome!!!','success')
        return redirect(url_for('login'))
    return render_template('signup.html',title='Register', form=form)

@login_manager.user_loader
@login_required
def load_user(user_id):
    user = db.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'").fetchone()
    return user.get(user_id)

# login a registered user
@app.route('/login',methods=['POST','GET'])
def login():
    # check if credentials provided are valid (is_authenticated)
    if current_user.is_authenticated:
        return redirect(url_for('books'))
    # check if POST request is valid (validate_on _submit)
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit:
        user = db.execute(f"SELECT email,password FROM users WHERE email = '{form.email.data}'").fetchone()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(current_user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Welcome, you have successfully logged in!','success')
            return redirect(next_page) if next_page else redirect(url_for('get_books'))
        else:
            flash('Invalid Credentials!, Login unsuccessful.','danger')
            return redirect (url_for('login'))
    return render_template('login.html',title='Login', form=form)
        

# logout and clean up user cookie session
@app.route('/logout')
# @login_required
def logout():
    logout_user()
    flash('See you next time!','success')
    return redirect ('index')

# #books page listing all books
# @app.route('/books', methods=['GET'])
# # @login_required
# def get_books():
#     # for current_user in users:
#     books = db.execute('SELECT * FROM books ORDER BY title')
#     print(books)
#     # return jsonify({'books':[dict(row) for row in books]})
#     return render_template('books.html', books=books)

# #books search results
# @app.route('/books/search/<string:search>')
# # @login_required
# def results(search):
#     # form = SearchForm()
#     # if form.valid_on_submit:
#     results = db.execute(f"SELECT * from books WHERE isbn LIKE ('%{search}%') OR author LIKE ('{search}%') OR title LIKE ('{search}%')")
#     if results:
#         return jsonify({'books':[dict(row) for row in results]}),200
#         #   return render_template ('books.html',books=results)
#     flash('No book with the specified values!','danger')
#     return jsonify(message='NOT FOUND')
#         # return ('Resource not found')
# #if not working try using search form
# # catch exeception for true regardless of the casing

# #get book page
# @app.route('/books/<string:isbn>')
# # @login_required
# def get_book(isbn):
#     url = "https://www.goodreads.com/book/review_counts.json"
#     response = requests.get(url, params={
#         "key":"Ua37abPi9E9sOrgQscJftg", 
#         "isbns": f"{isbn}"})
#     if response.status_code!= 200:
#         raise Exception('ERROR:404 REQUEST NOT FOUND')
#     data = response.json()
#     return jsonify(data) #return(data)
#     # books = db.execute(f"INSERT INTO books(goodreads_average_rating,goodreads_number_of_rating) VALUES ('data['books'][0]['average_rating']','data['books'][0]['work_ratings_count']')")
#     # db.commit()
#     # return jsonify({'book':[dict(row)for row in books]})
    
#     # return jsonify(message=data['average_rating','number'])

# #review a book
# @app.route('/books/<string:isbn>/reveiw',methods=['POST','GET'])
# # @login_required
# def review(isbn):
#     form = ReviewForm()
#     if request.method=='POST' and form.valid_on_submit:
#         user = db.cur.execute('SELECT * FROM reviews WHERE reviewer = current_user.user_id')
#         if user == 0:
#             db.cur.execute(f"INSERT * INTO reveiws(reviewer,rated_book,review,rating) VALUES(current_user['username'],{isbn},{form.review.data},{form.rating.data})")
#             db.cur.commit()
#             flash('Successfully Inserted!','success')
#             print('current_user')
#             return('Successfully Inserted!')
#         flash('You have already reviewed this book, thankyou!','danger')
#         return redirect('get_book')
#     return render_template('reveiw.html')
#     #consume the API to get the reviews

# #greatreads api
# @app.route('/api/<string:isbn>')
# def book_review_count(isbn):
#     # db.execute("SELECT * FROM users WHERE isbn='isbn'")
#     pass
    
