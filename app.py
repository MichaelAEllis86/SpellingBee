import os
from flask import Flask, jsonify, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from spellingbee import SpellingBee
from models import db, connect_db, User,Game
from flask_sqlalchemy import SQLAlchemy
from form import Guessform, Userform

app=Flask(__name__)
app.app_context().push()

# set environment variable to NOTTEST if were working the real DB in app.py, if we are in test mode in test.py this variable is set to "TEST" and we use the test database
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///cupcakes' if os.environ.get("TEST", "NOTTEST") == "NOTTEST" else 'postgresql:///test_cupcakes' 
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///spellingbee_db'



app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_ECHO']= True
# app.config['SQLALCHEMY_ECHO']= True if os.environ.get("TEST", "NOTTEST") == "NOTTEST" else False
app.config['SECRET_KEY']="oh-so-secret"
debug=DebugToolbarExtension(app)

connect_db(app)

#helpers functions, move these later maybe?
def clear__all_sessions():
    "used to clear the session of all game data so the user can start a new game."
    session["rating"]="empty"
    session["letters"]="empty"
    session["center_letter"]="empty"
    session["guessed_words"]="empty"
    session["all_valid_words"]="empty"
    session["num_words"]="empty"
    session["num_valid_words"]="empty"
    session["valid_pangrams"]="empty"
    session["guessed_pangrams"]="empty"
    session["score"]="empty"
    session["total_points"]="empty"
    

def evaluate_rating(num_of_points, total_num_points):
        """Ranks are based on a percentage of possible points in a puzzle."""
        percentage_score=num_of_points/total_num_points
        if percentage_score >= 0.9:
            rating="Genius"
            return rating
        elif percentage_score < 0.9 and percentage_score >=0.8:
            rating="Amazing"
            return rating
        elif percentage_score <0.8 and percentage_score >=0.7:
            rating="Great"
            return rating
        elif percentage_score < 0.7 and percentage_score >=0.6:
            rating="Nice"
            return rating
        elif percentage_score < 0.6 and percentage_score >=0.5:
            rating="Solid"
            return rating
        elif percentage_score < 0.5 and percentage_score >=0.4:
            rating="Good"
            return rating
        elif percentage_score < 0.4 and percentage_score >=0.3:
            rating="Moving up"
            return rating
        elif percentage_score < 0.3 and percentage_score >=0.2:
            rating="Good start"
            return rating
        else:
            rating="Beginner"
            return rating
    
#Start the game
game=SpellingBee()

@app.route("/clear")
def clear_session_and_redirect():
    clear__all_sessions()
    return redirect("/")

# connect_db(app)
#-------html routes go below --------
@app.route("/base")
def show_base():
    """show base template page for reference"""
    return render_template("base.html")

@app.route("/")
def generate_and_show_game():
    """Displays the board with a guess form , updates session with game parameters"""
    form=Guessform()

    if session.get("letters","empty") =="empty":
        session["letters"]=game.letters
    else:session["letters"]=session["letters"]
    print(f"here is session letters---> {session['letters']}")
    print(f"here is game.letters---> {game.letters}")

    if session.get("guessed_words","empty") =="empty":
        session["guessed_words"]=game.guessed_words
    else:session["guessed_words"]=session["guessed_words"]
    print(f"here is session guessed_words---> {session['guessed_words']}")
    print(f"here is game.guessed_words---> {game.guessed_words}")

    if session.get("center_letter","empty") =="empty":
        session["center_letter"]=game.center_letter
    else:session["center_letter"]=session["center_letter"]
    print(f"here is session center_letter---> {session['center_letter']}")
    print(f"here is game.center_letter---> {game.center_letter}")

    if session.get("score","empty") =="empty":
        session["score"]=game.score
    else:session["score"]=session["score"]
    print(f"here is session score---> {session['score']}")
    print(f"here is game.score---> {game.score}")

    if session.get("all_valid_words","empty") =="empty":
        session["all_valid_words"]=game.all_valid_words
    else:session["all_valid_words"]=session["all_valid_words"]
    print(f"here is session all_valid_words---> {session['all_valid_words']}")
    print(f"here is game.all_valid_words---> {game.all_valid_words}")

    if session.get("total_points","empty") =="empty":
        session["total_points"]=game.total_points
    else:session["total_points"]=session["total_points"]
    print(f"here is session total_points---> {session['total_points']}")
    print(f"here is game.total_points---> {game.total_points}")

    score=session["score"]
    print(f"printing the score argument for evaluate rating {score}")
    total_points=session["total_points"]
    print(f"printing the total_points argument for evaluate rating {total_points}")

    if session.get("rating","empty") =="empty":
        session["rating"]=evaluate_rating(score,total_points)
    else:session["rating"]=session["rating"]
    print(f"here is session rating {session['rating']}")

    if session.get("valid_pangrams","empty") =="empty":
        session["valid_pangrams"]=game.valid_pangrams
    else:session["valid_pangrams"]=session["valid_pangrams"]
    print(f"here is session valid_pangrams {session['valid_pangrams']}")
    print(f"here is the game.valid_pangrams {game.valid_pangrams}")

    if session.get("guessed_pangrams","empty") =="empty":
        session["guessed_pangrams"]=game.guessed_pangrams
    else:session["guessed_pangrams"]=session["guessed_pangrams"]
    print(f"here is session guessed_pangrams {session['guessed_pangrams']}")
    print(f"here is the game.guessed_pangrams {game.guessed_pangrams}")

    if session.get("num_words","empty") =="empty":
        session["num_words"]=game.num_words
    else:session["num_words"]=session["num_words"]
    print(f"here is session num_words {session['num_words']}")
    print(f"here is the game.num_words {game.num_words}")

    if session.get("num_valid_words","empty") =="empty":
        session["num_valid_words"]=game.num_valid_words
    else:session["num_valid_words"]=session["num_valid_words"]
    print(f"here is session num_valid_words {session['num_valid_words']}")
    print(f"here is the game.num_valid_words {game.num_valid_words}")


    return render_template("home.html", form=form, game=game)



@app.route("/spellingbee/users", methods=["GET", "POST"])
def show_and_add_users():
   form=Userform()
   users=User.query.all()

   if form.validate_on_submit():
       username=form.username.data
       image=form.image.data
       print(f"the new user form data is username={username} image={image}")
       new_user=User(username=username, image=image)
       db.session.add(new_user)
       db.session.commit()
       flash("New User created!!")
       flash(f"your new user is {new_user.username}, with an id of {new_user.id}", "success")

   return render_template("userlist.html",users=users, form=form)

@app.route("/spellingbee/users/<user_id>")
def show_user_detail(user_id):
    int_user_id=int(user_id)
    user=User.query.get_or_404(int_user_id)
    games=user.games
    return render_template("userdetail.html", user=user,games=games)




# @app.route("/showcupcakes")
# def show_cupcakes_page():
#     """show html of all our beautiful cupcakes. It's here because I can and the images are pretty good"""
#     all_cupcakes=Cupcake.query.all()
#     return render_template("cupcakelist.html", cupcakes=all_cupcakes)

#-------api routes go below --------
# @app.route("/api/cupcakes")
# def get_all_cupcakes():
#     cupcakes=Cupcake.query.all()
#     serialized_cupcakes=[cupcake.serialize_cupcake() for cupcake in cupcakes]
#     return jsonify(cupcakes=serialized_cupcakes)

# @app.route("/api/cupcakes/<cupcake_id>")
# def get_a_cupcake(cupcake_id):
#     int_cupcake_id=int(cupcake_id)
#     cupcake=Cupcake.query.get_or_404(int_cupcake_id)
#     serialized_cupcake=cupcake.serialize_cupcake()
#     return jsonify(cupcake=serialized_cupcake)

# @app.route("/api/cupcakes", methods=['POST'])
# def add_new_cupcake():
#     print(" Checking the data we received in request.json!!!->->",request.json)
#     cake_flavor=request.json["flavor"]
#     cake_size=request.json["size"]
#     cake_rating=request.json["rating"]
#     cake_image=request.json["image"]
#     new_cupcake=Cupcake(flavor=cake_flavor, size=cake_size, rating=cake_rating, image=cake_image)
#     db.session.add(new_cupcake)
#     db.session.commit()
#     serialized_new_cupcake=new_cupcake.serialize_cupcake()
#     return (jsonify(new_cupcake=serialized_new_cupcake),201)

# @app.route("/api/cupcakes/<cupcake_id>", methods=["DELETE"])
# def del_a_cupcake(cupcake_id):
#     int_cupcake_id=int(cupcake_id)
#     cupcake=Cupcake.query.get_or_404(int_cupcake_id)
#     db.session.delete(cupcake)
#     db.session.commit()
#     return jsonify({"message":f"Successfully Deleted Cupcake with an id of {cupcake.id}"})

# #Several approaches to this patch route which I will detail.

# #1 replace with all fields found in request.json. This method is good if the user doesn't want to update all fields. However, if anything doesn't conform to the model we will get a bug,which is possible.

# # @app.route("/api/cupcakes/<cupcake_id>", methods=["PATCH"])
# # def edit_a_cupcake_v1(cupcake_id):
# #     print(" Checking the data we received in request.json!!!->->",request.json)
# #     int_cupcake_id=int(cupcake_id)
# #     cupcake=Cupcake.query.get_or_404(int_cupcake_id)
# #     Cupcake.query.filter_by(id=int_cupcake_id).update(request.json)
# #     db.session.commit()
# #     serialized_cupcake=cupcake.serialize_cupcake()
# #     return jsonify(edited_cupcake=serialized_cupcake)

# #2 Edits the existing cupcake one field/attribute at a time. A bit longer/tedious but works well given the exercises assumption that all an entire cupcake obj is passed in to the backend. 
# #If this wasn't the case it could be problematic for updating just one or two fields.
# @app.route("/api/cupcakes/<cupcake_id>", methods=["PATCH"])
# def edit_a_cupcake_v2(cupcake_id):
#     print(" Checking the data we received in request.json!!! ->->",request.json)
#     int_cupcake_id=int(cupcake_id)
#     cupcake=Cupcake.query.get_or_404(int_cupcake_id)
#     cupcake.flavor=request.json["flavor"]
#     cupcake.size=request.json["size"]
#     cupcake.rating=request.json["rating"]
#     cupcake.image=request.json["image"]
#     db.session.commit()
#     serialized_cupcake=cupcake.serialize_cupcake()
#     return jsonify(edited_cupcake=serialized_cupcake)



# {
# 	"cupcake": {
# 		"flavor": "lemon",
# 		"id": 3,
# 		"image": "https://tinypic.host/images/2024/03/25/vegan-lemon-cupcakes-1..jpeg",
# 		"rating": 7.0,
# 		"size": "small"
# 	}
# }
