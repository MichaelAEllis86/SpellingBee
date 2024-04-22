from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from sqlalchemy.dialects.postgresql import ARRAY

db=SQLAlchemy()

bcrypt=Bcrypt()

def connect_db(app):
    db.app=app
    db.init_app(app)

#models go below
    
class User(db.Model):
    """User Model! A User plays many games!"""

    __tablename__ = "users"

    def __repr__(self):
        u=self
        return f"<user id={u.id} username={u.username} image={u.image}"
    
    def serialize_user(self):
        return {
            "id": self.id,
            "username": self.username,
            "image": self.image,
            }
    @classmethod
    def register(cls,username,pwd,image):
        """Register user w/hashed password and return user."""
        hashed=bcrypt.generate_password_hash(pwd)
        #turn bytestring into normal (unicode utf8) string
        hashed_utf8=hashed.decode("utf8")
        #return instance of user with username, image, and hashed pwd
        return cls(username=username, password=hashed_utf8, image=image)
    
    @classmethod
    def edit_password(cls,pwd):
        """Similar to register but just returns the hashed pw"""
        hashed=bcrypt.generate_password_hash(pwd)
        #turn bytestring into normal (unicode utf8) string
        hashed_utf8=hashed.decode("utf8")
        #return instance of user with username, image, and hashed pwd
        return hashed_utf8


    @classmethod
    def authenticate(cls,username,pwd):
        """validate that a user exists and password is correct
        returns the user if valid, else returns False"""

        user=User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password,pwd):
            return user
        else:
            return False
        
    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    username=db.Column(db.String(50),
                        nullable=False,
                        unique=True)
    password=db.Column(db.Text,
                       nullable=False,
                       unique=True)
    image=db.Column(db.Text,
                        nullable=False,
                        default='https://t4.ftcdn.net/jpg/04/35/29/29/360_F_435292900_BU8c1Uf9ZRA3j7EyP6kKfTXzpPt5dxDf.jpg')
    # rating=db.Column(db.Float,
    #               nullable=False,
    #               default=0)
    # pangrams=db.Column(db.integer, 
    #                     nullable=False,
    #                     default='0')

    games=db.relationship("Game", backref="player", cascade="all, delete-orphan")

class Game(db.Model):
    """A games model. A game is associated with one user, a user plays many games. Stores Essential stats for each game played!"""

    def __repr__(self):
        g=self
        return f"<game id={g.id} created_at={g.created_at} rating={g.rating} letters={g.letters} center_letter={g.center_letter} guessed_words={g.guessed_words} all_valid_words={g.all_valid_words} num_words={g.num_words} num_valid_words={g.num_valid_words} valid_pangrams={g.valid_pangrams} guessed_pangrams={g.guessed_pangrams} score={g.score} total_points={g.total_points} user_id={g.user_id} removed_center_letter={g.removed_center_letter} "



    def format_date(self):

        """This function can be used to format the game creation date. It formats from the datetime obj created in the "created_at" column to a "friendly" date string that 
        displays the date & time in the following format Example: April 15th, 2024 at 3:02 PM """

        months={1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
        month_key=self.created_at.month
        named_month=months[month_key]
        friendly_time=self.created_at.strptime(f'{self.created_at.hour}:{self.created_at.minute}','%H:%M').strftime('%I:%M %p')
        
        return f"{named_month} {self.created_at.day}, {self.created_at.year} at {friendly_time}"

    def print_current_time(self):
        print(f"{datetime.now()}")
        return(f"{datetime.now()}")
    
    def serialize_game(self):
        return {
            "id": self.id,
            "created_at": self.format_date(),
            "rating": self.rating,
            "letters":self.letters,
            "center_letter":self.center_letter,
            "guessed_words":self.guessed_words,
            "all_valid_words":self.all_valid_words,
            "num_words":self.num_words,
            "num_valid_words":self.num_valid_words,
            "valid_pangrams":self.valid_pangrams,
            "guessed_pangrams":self.guessed_pangrams,
            "score":self.score,
            "total_points":self.total_points,
            "user_id":self.user_id,
            "removed_center_letter":self.removed_center_letter
            }
    
    __tablename__ = "games"

    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    created_at=db.Column(db.DateTime,
                         nullable=False,
                         default=datetime.now())
    rating=db.Column(db.String(20),
                     nullable=False,
                     default="Beginner")
    letters=db.Column(db.String(7),
                         nullable=False,)
    center_letter=db.Column(db.String(1),
                         nullable=False,)
    guessed_words=db.Column(db.ARRAY(db.Text),
                           nullable=False,
                           default=[])
    all_valid_words=db.Column(db.ARRAY(db.Text),
                           nullable=False,
                           default=[])
    num_words=db.Column(db.Integer,
                            nullable=False,
                            default=0)
    num_valid_words=db.Column(db.Integer,
                               nullable=False,
                            default=0)
    valid_pangrams=db.Column(db.ARRAY(db.Text),
                           nullable=False,
                           default=[])
    guessed_pangrams=db.Column(db.ARRAY(db.Text),
                           nullable=False,
                           default=[])
    score=db.Column(db.Integer,
                    nullable=False,
                    default=0)
    total_points=db.Column(db.Integer,
                    nullable=False,
                    default=0)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    removed_center_letter=db.Column(db.String(7),
                         nullable=False,)
    

    

