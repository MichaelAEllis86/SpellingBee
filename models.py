from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY

db=SQLAlchemy()

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


    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    username=db.Column(db.String(20),
                        nullable=False)
    image=db.Column(db.Text,
                        nullable=False,
                        default='https://tinyurl.com/demo-cupcake')
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
        return f"<game id={g.id} created_at={g.created_at} rating={g.rating} letters={g.letters} center_letter={g.center_letter} guessed_words={g.guessed_words} all_valid_words={g.all_valid_words} num_words={g.num_words} num_valid_words={g.num_valid_words} valid_pangrams={g.valid_pangrams} guessed_pangrams={g.guessed_pangrams} score={g.score} total_points={g.total_points} user_id={g.user_id} "



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
            "user_id":self.user_id
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
    

    

