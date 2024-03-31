from models import User,Game, db
from app import app

#create all tables
db.drop_all()
db.create_all()

#imageURL strings

default_user_imageURL="https://t4.ftcdn.net/jpg/04/35/29/29/360_F_435292900_BU8c1Uf9ZRA3j7EyP6kKfTXzpPt5dxDf.jpg"

u1=User(username="Apop",  image=default_user_imageURL)
u2=User(username="Toasty", image=default_user_imageURL)
u3=User(username="Rosie", image=default_user_imageURL)
u4=User(username="Daffy", image=default_user_imageURL)
u5=User(username="Roomie", image="https://i.chzbgr.com/full/7889062656/h10C497C8/cat-spinning-on-a-roomba")


db.session.add_all([u1,u2,u3,u4,u5])
db.session.commit()


g1=Game(rating="Genius",guessed_words=["testword1"],valid_pangrams=["learning"],letters="gniearl",center_letter="n",user_id=1, guessed_pangrams=["learning"],all_valid_words=["testword2"], num_words=14, num_valid_words=29, score=75, total_points=150)
g2=Game(rating="Solid",guessed_words=["testword1","testword2"],valid_pangrams=["there are none"],letters="aklectv",center_letter="k",user_id=2, guessed_pangrams=["learning"],all_valid_words=["testword2"], num_words=6, num_valid_words=27, score=75, total_points=150)
g3=Game(rating="Amazing",guessed_words=["testword1","testword2","testword3"],valid_pangrams=["learning","stickier"],letters="verifyu",center_letter="r",user_id=3, guessed_pangrams=["learning"],all_valid_words=["testword2"], num_words=30, num_valid_words=33, score=75, total_points=150)
g4=Game(rating="Nice",guessed_words=["there are none"],valid_pangrams=["testpangram1"],letters="testleg",center_letter="t",user_id=4, guessed_pangrams=["learning"], all_valid_words=["testword2"], num_words=12, num_valid_words=17,score=75, total_points=150)
g5=Game(rating="Good Start",guessed_words=["testword65"],valid_pangrams=["learning to code slowly"],letters="testlet",center_letter="r",user_id=5, guessed_pangrams=["learning"],all_valid_words=["testword2"], num_words=9, num_valid_words=16, score=75, total_points=150)
g6=Game(rating="Amazing",guessed_words=["testword1"],valid_pangrams=["learning"],letters="gniearl",center_letter="n",user_id=1, guessed_pangrams=["learning"],all_valid_words=["testword2"], num_words=5, num_valid_words=13, score=75, total_points=150)
g7=Game(rating="Great",guessed_words=["testword1"],valid_pangrams=["learning"],letters="gniearl",center_letter="n",user_id=1 ,guessed_pangrams=["learning"],all_valid_words=["testword2"], num_words=3, num_valid_words=10, score=75, total_points=150)
g8=Game(rating="Nice",guessed_words=["testword1"],valid_pangrams=["learning"],letters="gniearl",center_letter="n",user_id=1, guessed_pangrams=["learning"],all_valid_words=["testword2"], num_words=2, num_valid_words=16, score=75, total_points=150)
g9=Game(rating="Solid",guessed_words=["testword1"],valid_pangrams=["learning"],letters="gniearl",center_letter="n",user_id=1, guessed_pangrams=["learning"],all_valid_words=["testword2"], num_words=14, num_valid_words=22,  score=75, total_points=150)
g10=Game(rating="Good",guessed_words=["testword1"],valid_pangrams=["learning"],letters="gniearl",center_letter="n",user_id=1, guessed_pangrams=["learning"],all_valid_words=["testword2"], num_words=10, num_valid_words=40,  score=47, total_points=160)
g11=Game(rating="Moving up",guessed_words=["testword1"],valid_pangrams=["learning"],letters="gniearl",center_letter="n",user_id=1, guessed_pangrams=["learning"],all_valid_words=["testword2"], num_words=7, num_valid_words=19,  score=60, total_points=300)
g12=Game(rating="Good start",guessed_words=["testword1"],valid_pangrams=["learning"],letters="gniearl",center_letter="n",user_id=1, guessed_pangrams=["learning"], all_valid_words=["testword2"], num_words=10, num_valid_words=27,  score=20, total_points=105)
g13=Game(rating="Beginner",guessed_words=["testword1"],valid_pangrams=["learning"],letters="gniearl",center_letter="n",user_id=1, guessed_pangrams=["learning"], all_valid_words=["testword2"], num_words=20, num_valid_words=35, score=4, total_points=75)

db.session.add_all([g1,g2,g3,g4,g5,g6,g7,g8,g9,g10,g11,g12,g13])
db.session.commit()
