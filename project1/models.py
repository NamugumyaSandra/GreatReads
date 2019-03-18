# from application import db,login_manager
# from flask_login import UserMixin


from application import db,login_manager
from flask_login import UserMixin

#static method that queries the db
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#create User table class and specify the attributes
class User(db.Model, UserMixin):  # user mixin helps in authentication and validity checks allowing for login and out
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(100),unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    review= db.relationship('Review', backref='reviwer', lazy=True)#r/ship with the Post model class

# representation format... what to be printed out
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

 #creating the post table in the db.Model baseclass   
class Reviews(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text,nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
