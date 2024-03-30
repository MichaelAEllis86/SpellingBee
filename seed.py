from models import User,Game, db
from app import app

#create all tables
db.drop_all()
db.create_all()

#imageURL strings

default_user_imageURL="https://tinypic.host/image/bee-default.DaJjax"

u1=User(first_name="Michael", last_name="Ellis", image_url=default_user_imageURL)
u2=User(first_name="Toasty", last_name="Toastada", image_url=default_user_imageURL)
u3=User(first_name="Rosie", last_name="Ellis", image_url=default_user_imageURL)
u4=User(first_name="Daffy", last_name="Duck", image_url=default_user_imageURL)
u5=User(first_name="Roomie", last_name="TheRoomba", image_url="https://i.chzbgr.com/full/7889062656/h10C497C8/cat-spinning-on-a-roomba")


db.session.add_all([u1,u2,u3,u4,u5])
db.session.commit()


g1=Game(first_name="Michael", last_name="Ellis", image_url=default_user_imageURL)
g2=User(first_name="Toasty", last_name="Toastada", image_url=default_user_imageURL)
g3=User(first_name="Rosie", last_name="Ellis", image_url=default_user_imageURL)
g4=User(first_name="Daffy", last_name="Duck", image_url=default_user_imageURL)
g5=User(first_name="Roomie", last_name="TheRoomba", image_url="https://i.chzbgr.com/full/7889062656/h10C497C8/cat-spinning-on-a-roomba")