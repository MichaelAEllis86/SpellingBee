import os
from flask import Flask, jsonify, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from spellingbee import SpellingBee
from models import db, connect_db, User,Game
from flask_sqlalchemy import SQLAlchemy
from form import Guessform, Userform, Dictionaryform, Loginform
from flask_bcrypt import Bcrypt

app=Flask(__name__)
app.app_context().push()

# set environment variable to NOTTEST if were working the real DB in app.py, if we are in test mode in test.py this variable is set to "TEST" and we use the test database
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///cupcakes' if os.environ.get("TEST", "NOTTEST") == "NOTTEST" else 'postgresql:///test_cupcakes' 
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///spellingbee_db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgresql:///spellingbee_db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_ECHO']= True
# app.config['SQLALCHEMY_ECHO']= True if os.environ.get("TEST", "NOTTEST") == "NOTTEST" else False
app.config['SECRET_KEY']="oh-so-secret"
debug=DebugToolbarExtension(app)

connect_db(app)
bcrypt=Bcrypt()

# <---------------Spellingbee Game helper functions, move these later maybe to a new code sheet---------------->?

def read_dict(dict_path):
    """Read and return all words in dictionary .txt file"""
    dict_file = open(dict_path)
    words = [w.strip() for w in dict_file]
    dict_file.close()
    return words

def subtract_s_words(word_list):
    """removes all the words that have an S in them from a list of words. Used because the spellingbee game is deliberately "s" free per the game rules """
    no_s_word_list={word for word in word_list if "s" not in word}
    return no_s_word_list

def word_list_init(dict_path):
    """prepare a word list for use by the Spellingbee class/game. Reads words txt file and then filters out all the words with S from said list."""
    words=read_dict(dict_path)
    no_s_word_list=set(subtract_s_words(words))
    return no_s_word_list

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
    session["removed_center_letter"]="empty"
    session["game_id"]="empty"

def set_sessions_for_newgame():
    """makes new instance of spellingbee game. Updates all session values to reflect the new game.
    DOES NOT UPDATE the session["game_id"]!!!! WE do that in the view function after the game has been assigned an id in the database!"""
    game=SpellingBee(no_s_words)
    print("the new spellingbee instance has been created")
    
    session["letters"]=game.letters
    session["center_letter"]=game.center_letter
    session["guessed_words"]=game.guessed_words
    session["all_valid_words"]=game.all_valid_words
    session["num_words"]=game.num_words
    session["num_valid_words"]=game.num_valid_words
    session["valid_pangrams"]=game.valid_pangrams
    session["guessed_pangrams"]=game.guessed_pangrams
    session["score"]=game.score
    session["total_points"]=game.total_points
    session["removed_center_letter"]=game.removed_center_letter
    session["game_id"]="Not set yet"
    session["rating"]=evaluate_rating(session["score"],session["total_points"])

def assign_sessions_for_db(user_id):
    """Currently unused function. Intended purpose is to take all existing session game data and make a new game with it in the db"""
    newgame=Game(rating=session["rating"], letters=session["letters"], center_letter=session["center_letter"], guessed_words=session["guessed_words"], all_valid_words=session["all_valid_words"], num_words=session["num_words"], num_valid_words=session["num_valid_words"],valid_pangrams=session["valid_pangrams"],guessed_pangrams=session["guessed_pangrams"],score=session["score"],total_points=session["total_points"],removed_center_letter=session["removed_center_letter"],user_id=user_id)
    db.session.add(newgame)
    db.session.commit()
    return newgame
    
def evaluate_rating(num_of_points, total_num_points):
        """Determines ranks for a given point value, given a known total amount of points possible from the board.
        Ranks are based on the percentage of possible points in a puzzle.
        Example: A rating of Genius has a minimum point threshold of 90% of the total points so 90/100 total points =rating Genius.
        Amazing however would apply between 80-90% ranks"""
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

def get_rating_point_thresholds(total_num_points):
    """returns a dictionary that gives the point thresholds for all ranks of a particular board/game. Calculates based on the game's number of total possible points"""
    thresholds={"Genius":round(total_num_points*0.9,0),"Amazing":round(total_num_points*0.8,0),"Great":round(total_num_points*0.7,0),"Nice":round(total_num_points*0.6,0,),"Solid":round(total_num_points*0.5,0),
                "Good":round(total_num_points*0.4,0),"Moving up":round(total_num_points*0.3,0),"Good start":round(total_num_points*0.2)}
    return thresholds
def get_points_away_from_rating(num_of_points, total_num_points):
     """returns a dictionary that determines how far away a user is from a given rank given the player's score and the number of total points possible"""
     points_to_go={"points_from_Genius":(total_num_points*0.9)-num_of_points,"points_from_Amazing":(total_num_points*0.8)-num_of_points,"points_from_Great":(total_num_points*0.7)-num_of_points,"points_from_Nice":(total_num_points*0.6)-num_of_points,"points_from_Solid":(total_num_points*0.5)-num_of_points,
                "points_from_Good":(total_num_points*0.4)-num_of_points,"points_from_Moving_up":(total_num_points*0.3)-num_of_points,"points_From_Good_start":(total_num_points*0.2)-num_of_points}
     return points_to_go

def get_words_by_letter(wordlst):
    """This function takes in a list of valid words for a given board/hive and then provides a dictionary break down of how many of those words start with a given letter
    The purpose of this is to provide the user additional game hint data regarding how many words in a given hive start with the specified letter. 
    Final output looks like this num_valid_words_by_letter={"A":4, "B":3, etc}"""
    startswithA=[word for word in wordlst if word.startswith("A")==True]
    startswithB=[word for word in wordlst if word.startswith("B")==True]
    startswithC=[word for word in wordlst if word.startswith("C")==True]
    startswithD=[word for word in wordlst if word.startswith("D")==True]
    startswithE=[word for word in wordlst if word.startswith("E")==True]
    startswithF=[word for word in wordlst if word.startswith("F")==True]
    startswithG=[word for word in wordlst if word.startswith("G")==True]
    startswithH=[word for word in wordlst if word.startswith("H")==True]
    startswithI=[word for word in wordlst if word.startswith("I")==True]
    startswithX=[word for word in wordlst if word.startswith("X")==True]
    startswithK=[word for word in wordlst if word.startswith("K")==True]
    startswithL=[word for word in wordlst if word.startswith("L")==True]
    startswithM=[word for word in wordlst if word.startswith("M")==True]
    startswithN=[word for word in wordlst if word.startswith("N")==True]
    startswithO=[word for word in wordlst if word.startswith("O")==True]
    startswithP=[word for word in wordlst if word.startswith("P")==True]
    startswithR=[word for word in wordlst if word.startswith("R")==True]
    startswithT=[word for word in wordlst if word.startswith("T")==True]
    startswithU=[word for word in wordlst if word.startswith("U")==True]
    startswithV=[word for word in wordlst if word.startswith("V")==True]
    startswithW=[word for word in wordlst if word.startswith("W")==True]
    startswithY=[word for word in wordlst if word.startswith("Y")==True]
    words_by_letter={"A_words":startswithA,"B_words":startswithB,"C_words":startswithC,"D_words":startswithD,"E_words":startswithE,"F_words":startswithF,"G_words":startswithG,
                     "H_words":startswithH,"I_words":startswithI,"X_words":startswithX,"K_words":startswithK,"L_words":startswithL,"M_words":startswithM,"N_words":startswithN,
                     "O_words":startswithO,"P_words":startswithP,"R_words":startswithR,"T_words":startswithT,"U_words":startswithU,"V_words":startswithV,"W_words":startswithW,
                     "Y_words":startswithY}
    valid_words_by_letter={key:value for key,value in words_by_letter.items() if len(value)>0 }
    num_valid_words_by_letter={key:len(value) for key,value in valid_words_by_letter.items()}
    return num_valid_words_by_letter

def get_words_by_length(wordlst):
    """Creates a dictionary to store the lengths of each valid words in a hive, and then how many times a word of a given length appears in the hive's valid word list.
    final output is a dictionary with a number of letters a word has as a key, then a value that corresponds to the amount of times a 4 letter word appears in the valid word list
     EX output {"4":20, "5":10, "6":3} meaning that there are 20 4 letter words, 10 5 letter words, and 3 6 letter words in that puzzle """
    word_length_counts={}
    for word in wordlst:
        word_length=len(word)
        if word_length in word_length_counts:
            word_length_counts[word_length]+=1
        else:
            word_length_counts[word_length]=1
    return word_length_counts

def validate_word_from_session(wordguess):
    """ This Function validates a wordguess from the user and gives feedback depending on if the word is valid or not!
    All validity evaluation from this function is based upon session data!!! The Function also updates scoring parameters in session
    including, score, rating, pangrams, guessed_words and num_words"""

    length_check=len(wordguess) >= 4
        # print(f"the length check is {length_check}")
    
    already_guessed_check=wordguess in session["guessed_words"]
        # print(f"already_guessed_check results are {already_guessed_check}")

    central_letter_check=session["center_letter"] in wordguess
        # print(f"the center letter check is {central_letter_check}")
    
    letter_check=all([letter in session["letters"] for letter in wordguess])
        # print(f"letter_check_results are {letter_check_results}")

    word_exists_check=wordguess in session["all_valid_words"]
        # print(f"the word exists check is {word_exists_check}")
        
    if length_check== False:
            result="too short"
            return result
    elif already_guessed_check== True:
            result="already guessed"
            return result
    elif length_check==True and already_guessed_check==False and central_letter_check==False:
            result="missing center letter"
            return result
    elif length_check==True and already_guessed_check==False and central_letter_check==True and letter_check==False:
            result="invalid letters"
            return result
    elif length_check==True and already_guessed_check==False and central_letter_check==True and letter_check==True and word_exists_check==False:
            result="not a word"
            return result
    else:
            result="valid"
            session["score"]+=len(wordguess)
            session["guessed_words"].append(wordguess)
            session["rating"]=evaluate_rating(session["score"],session["total_points"])
            session["num_words"]=len(session["guessed_words"])
            if wordguess in session["valid_pangrams"]:
                session["guessed_pangrams"].append(wordguess)
                result="pangram"
            return result
#<-----------Init of the games words dictionary files----------->
no_s_words=word_list_init("words.txt")

#<-----------ROUTES BEGIN HERE----------->

#<-----------Utility routes for testing and development purposes are below These Can be delete safely if noted----------->

@app.route("/clear")
def clear_session_and_redirect():
    """Clears all game data from the session, redirects to home"""
    clear__all_sessions()
    return redirect("/")

# connect_db(app)
#-------html routes go below --------
@app.route("/base")
def show_base():
    """show base template page for reference"""
    return render_template("base.html")

#delete me later
@app.route("/old")
def generate_and_show_game():
    """Displays the board with a guess form , updates session with game parameters"""
    form=Guessform()
    game=SpellingBee()

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

    if session.get("removed_center_letter","empty") =="empty":
        session["removed_center_letter"]=game.removed_center_letter
    else:session["removed_center_letter"]=session["removed_center_letter"]
    print(f"here is session removed_center_letter {session['num_valid_words']}")
    print(f"here is the game.removed_center_letter {game.removed_center_letter}")
# Add game id into this!!!!

    return render_template("home.html", form=form, game=game)

# <-----------Routes concerning user login, signup, logout, and authorization/validation for said routes are below----------->
@app.route("/")
def redirect_to_loginsignup():
    return redirect("/spellingbee/loginsignup")

@app.route("/spellingbee/loginsignup", methods=["GET", "POST"])
def show_loginsignup_page():
    """Shows login and singup page in GET route. In POST route handles the submission of the signup form to save a new user into the Users db model/users table"""
    form=Userform()
    if form.validate_on_submit():
        username=form.username.data
        pwd=form.password.data
        image=form.image.data
        print(f"the new user form data is username={username} image={image}")
        new_user=User.register(username,pwd,image)
        db.session.add(new_user)
        db.session.commit()
        flash("New User created!!")
        flash(f"your new user is {new_user.username}, with an id of {new_user.id}", "success")
        session["user_id"]=new_user.id
        user_id=int(session["user_id"])
        return redirect(f"/spellingbee/users/{user_id}")
    else: 
        return render_template("loginsignup.html", form=form)
# this route is a GET request soley so it can be used in anchor tags so easy user access to logout! It violates restful protocol and would at least be a POST request Can wrap in form!
@app.route("/spellingbee/logout")
def logout():
    """Saves game in session to the db if one exists, then logs user out by removing "user_id" from the session.
    Clears the session of all game data after saving. Redirects back to login/signup page with a friendly message :)"""
    if session.get("game_id", "empty")!="empty":
        session_game_id=int(session["game_id"])
        sessiongamequery=Game.query.get_or_404(session_game_id)
        game_user_id=sessiongamequery.user_id
        sessiongamequery.rating=session["rating"]
        sessiongamequery.letters=session["letters"]
        sessiongamequery.center_letter=session["center_letter"]
        sessiongamequery.guessed_words=session["guessed_words"]
        sessiongamequery.all_valid_words=session["all_valid_words"]
        sessiongamequery.num_words=session["num_words"]
        sessiongamequery.num_valid_words=session["num_valid_words"]
        sessiongamequery.valid_pangrams=session["valid_pangrams"]
        sessiongamequery.guessed_pangrams=session["guessed_pangrams"]
        sessiongamequery.score=session["score"]
        sessiongamequery.total_points=session["total_points"]
        sessiongamequery.removed_center_letter=session["removed_center_letter"]
        db.session.commit()
        flash(" Board Saved!! Have an awesome day!" , "success")
        session.pop("user_id")
        print("the previous game's session has been saved to the game DB entry! logging the user out!")
        clear__all_sessions()
        return redirect("/spellingbee/loginsignup")
    else:
        flash("Have a nice day!" , "success")
        print("There was nothing in the session to save!")
        session.pop("user_id")
        clear__all_sessions()
        return redirect("/spellingbee/loginsignup")

    
#loginform page and login handle form
@app.route("/spellingbee/login", methods=["GET","POST"])
def validate_login_redirect():
   """renders lightweight form page for login via GET.
   Handles login valdiation via POST takes data from login form username and pwd and compares to encrypted password  """
   loginform=Loginform()
   if loginform.validate_on_submit():
        username=loginform.username.data
        pwd=loginform.password.data
        print(f"the login form data is username={username}")
        user=User.authenticate(username,pwd)

        if user:
            session["user_id"]=user.id
            user_id=int(session["user_id"])
            flash("login successful! taking you to your game hub","success")
            return redirect(f"/spellingbee/users/{user_id}")
        else:
           flash("invalid username or password", "error")
           return redirect("/spellingbee/loginsignup")
   return render_template("login.html", loginform=loginform)
    
    
# #delete me later
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

#updated for passwords delete all the edit form shit if it doesnt work! 
@app.route("/spellingbee/users/<user_id>")
def show_user_detail(user_id):
    if "user_id" not in session:
        flash("You must be logged in to view", "error")
        return redirect("/spellingbee/loginsignup")
    else:
        int_user_id=int(user_id)
        user=User.query.get_or_404(int_user_id)
       
    # query's for user and game history statistics
        games=user.games
        user_word_total=db.session.query(db.func.sum(Game.num_words)).filter(Game.user_id==int_user_id).scalar()
        user_game_count=Game.query.filter_by(user_id=int_user_id).count()
        gamecount_genius=Game.query.filter_by(user_id=int_user_id,rating="Genius").count()
        gamecount_amazing=Game.query.filter_by(user_id=int_user_id,rating="Amazing").count()
        gamecount_great=Game.query.filter_by(user_id=int_user_id,rating="Great").count()
        gamecount_nice=Game.query.filter_by(user_id=int_user_id,rating="Nice").count()
        gamecount_solid=Game.query.filter_by(user_id=int_user_id,rating="Solid").count()
        gamecount_good=Game.query.filter_by(user_id=int_user_id,rating="Good").count()
        gamecount_moving_up=Game.query.filter_by(user_id=int_user_id,rating="Moving up").count()
        gamecount_good_start=Game.query.filter_by(user_id=int_user_id,rating="Good start").count()
        gamecount_beginner=Game.query.filter_by(user_id=int_user_id,rating="Beginner").count()
        return render_template("userdetail.html", user_id=int_user_id, user=user,games=games, user_word_total=user_word_total, user_game_count=user_game_count,gamecount_genius=gamecount_genius,
                           gamecount_amazing=gamecount_amazing, gamecount_great=gamecount_great, gamecount_nice=gamecount_nice, gamecount_solid=gamecount_solid,
                           gamecount_good=gamecount_good, gamecount_moving_up=gamecount_moving_up, gamecount_good_start=gamecount_good_start, gamecount_beginner=gamecount_beginner)
    
@app.route("/spellingbee/users/<user_id>/edit" ,methods=["GET","POST"])
def show_handle_user_edit(user_id):
    int_user_id=int(user_id)
    if "user_id" not in session or int(session["user_id"])!=int_user_id:
         flash("You must be logged in to edit a user", "error")
         return redirect("/spellingbee/loginsignup")
    user=User.query.get_or_404(int_user_id)
    edit_form=Userform(obj=user)
    if edit_form.validate_on_submit():
        username=edit_form.username.data
        pwd=edit_form.password.data
        image=edit_form.image.data
        hashed_pwd=User.edit_password(pwd)
        print(f"checking the form data username={username} pwd={pwd} image={image}")
        user.username=username
        user.password=hashed_pwd
        user.image=image
        print(f"checking the final edited user....  user_id={user.id} username={user.username} password={user.password} image={user.image}")
        db.session.commit()
        flash("User edited!!")
        flash(f"your edited user is {user.username}, with an id of {user.id}", "success")
        return redirect(f"/spellingbee/users/{session['user_id']}")



    return render_template("edit.html", edit_form=edit_form, user=user)
        
#  user_edit_form=Userform(obj=user) 
 # if user_edit_form.validate_on_submit():
        #     username=user_edit_form.username.data
        #     pwd=user_edit_form.password.data
        #     image=user_edit_form.image.data
        #     print(f"the edit user form data is username={username} pwd={pwd} image={image}")
        #     user=User.register(username,pwd,image)
        #     db.session.commit()
        #     flash("User edited!!")
        #     flash(f"your edited user is {user.username}, with an id of {user.id}", "success")
        #     session["user_id"]=user.id
        #     user_id_from_session=int(session["user_id"])
        #     return redirect(f"/spellingbee/users/{user_id_from_session}")
        # else:

# Post route to delete a user! 
@app.route("/spellingbee/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """simple delete user POST route. Deletes the queried user from the DB. Queries user by taking the user id from the route."""
    int_user_id=int(user_id)
    if "user_id" not in session or int(session["user_id"])!=int_user_id:
         flash("You must be logged in to delete a user", "error")
         return redirect("/spellingbee/loginsignup")
    else:
        user=User.query.get_or_404(int_user_id)
        db.session.delete(user)
        db.session.commit()
        session.pop("user_id")
        flash("User successfully deleted", "success")
        return redirect("/spellingbee/loginsignup")


#this route allows users to make a new board/hive!
#updated for passwords
@app.route("/spellingbee/users/<user_id>/game/new")
def generate_new_game(user_id):

    if "user_id" not in session:
        flash("You must be logged in to view", "error")
        return redirect("/spellingbee/loginsignup")
    else:
        int_user_id=int(user_id)
        #grabbing previous game's sessions data if present
        if session.get("game_id", "empty")!="empty":
            game_id=int(session["game_id"])
            #updating game database with previous game's session data
            sessiongamequery=Game.query.get_or_404(game_id)
            sessiongamequery.rating=session["rating"]
            sessiongamequery.letters=session["letters"]
            sessiongamequery.center_letter=session["center_letter"]
            sessiongamequery.guessed_words=session["guessed_words"]
            sessiongamequery.all_valid_words=session["all_valid_words"]
            sessiongamequery.num_words=session["num_words"]
            sessiongamequery.num_valid_words=session["num_valid_words"]
            sessiongamequery.valid_pangrams=session["valid_pangrams"]
            sessiongamequery.guessed_pangrams=session["guessed_pangrams"]
            sessiongamequery.score=session["score"]
            sessiongamequery.total_points=session["total_points"]
            sessiongamequery.removed_center_letter=session["removed_center_letter"]
            db.session.commit()
            flash("Previous Board Saved!! Making a New Game!" , "success")
            print("the previous game session has been saved to the game DB entry! Making new Game!")
        else:
            print("There is no current game to save! Making new game")

    #clearing old session data, making a new game, setting the session for newgame
    clear__all_sessions()
    set_sessions_for_newgame()
   
    # Saving the new gaming into the game DB
    newgame=Game(rating=session["rating"], letters=session["letters"], center_letter=session["center_letter"], guessed_words=session["guessed_words"], all_valid_words=session["all_valid_words"], num_words=session["num_words"], num_valid_words=session["num_valid_words"],valid_pangrams=session["valid_pangrams"],guessed_pangrams=session["guessed_pangrams"],score=session["score"],total_points=session["total_points"],removed_center_letter=session["removed_center_letter"],user_id=int_user_id)
    db.session.add(newgame)
    db.session.commit()
    #set the game_id from the new game into the session
    session["game_id"]=newgame.id
    return redirect(f"/spellingbee/users/{int_user_id}/game/{session['game_id']}")

#updated for passwords
@app.route("/spellingbee/users/<user_id>/game/continue")
def continue_game(user_id):
    if "user_id" not in session:
        flash("You must be logged in to view", "error")
        return redirect("/spellingbee/loginsignup")
    else:
        int_user_id=int(user_id)
    #grabbing previous game's sessions data if present
        if session.get("game_id", "empty")!="empty":
            game_id=int(session["game_id"])
            #updating game database with previous game's session data
            sessiongamequery=Game.query.get_or_404(game_id)
            sessiongamequery.rating=session["rating"]
            sessiongamequery.letters=session["letters"]
            sessiongamequery.center_letter=session["center_letter"]
            sessiongamequery.guessed_words=session["guessed_words"]
            sessiongamequery.all_valid_words=session["all_valid_words"]
            sessiongamequery.num_words=session["num_words"]
            sessiongamequery.num_valid_words=session["num_valid_words"]
            sessiongamequery.valid_pangrams=session["valid_pangrams"]
            sessiongamequery.guessed_pangrams=session["guessed_pangrams"]
            sessiongamequery.score=session["score"]
            sessiongamequery.total_points=session["total_points"]
            sessiongamequery.removed_center_letter=session["removed_center_letter"]
            db.session.commit()
            flash("Previous Board Saved!! Continuing your present game!" , "success")
            print("the previous game session has been saved to the game DB entry! Continuing with the current board!")
            return redirect(f"/spellingbee/users/{int_user_id}/game/{session['game_id']}")
        else:
            flash("You don't have a game going yet! Make a new game!", "error")
            return redirect(f"/spellingbee/users/{int_user_id}")
# gameplay page updated for passwords
@app.route("/spellingbee/users/<user_id>/game/<game_id>")
def showgameboardpage(user_id,game_id):
    if "user_id" not in session:
        flash("You must be logged in to view", "error")
        return redirect("/spellingbee/loginsignup")
    else:
        int_user_id=int(user_id)
        int_game_id=int(game_id)
        form=Guessform()
        dictionaryform=Dictionaryform()
        user=User.query.get_or_404(int_user_id)
        gamequery=Game.query.get_or_404(int_game_id)
        rank_thresholds=get_rating_point_thresholds(session["total_points"])
        num_valid_words_by_letter=get_words_by_letter(session["all_valid_words"])
        num_valid_words_by_length=get_words_by_length(session["all_valid_words"])
        return render_template("home.html", user=user, gamequery=gamequery, form=form, dictionaryform=dictionaryform,user_id=int_user_id,game_id=int_game_id, rank_thresholds=rank_thresholds, num_valid_words_by_length=num_valid_words_by_length, num_valid_words_by_letter=num_valid_words_by_letter)

# hints page navigated to from the gameplay page updated for passwords!
@app.route("/spellingbee/users/<user_id>/game/<game_id>/hints")
def showgamehintspage(user_id,game_id):
    if "user_id" not in session:
        flash("You must be logged in to view", "error")
        return redirect("/spellingbee/loginsignup")
    else:
        int_user_id=int(user_id)
        int_game_id=int(game_id)
        user=User.query.get_or_404(int_user_id)
        gamequery=Game.query.get_or_404(int_game_id)
        number_of_pangrams=len(session["valid_pangrams"])
        rating_thresholds=get_rating_point_thresholds(session["total_points"])
        num_valid_words_by_letter=get_words_by_letter(session["all_valid_words"])
        num_valid_words_by_length=get_words_by_length(session["all_valid_words"])
        is_bingo_hive=len(num_valid_words_by_letter)==7
        print(f"here is valid_words_by_letter ----> {num_valid_words_by_letter}")
        return render_template("hints.html", user=user, gamequery=gamequery,user_id=int_user_id,game_id=int_game_id,number_of_pangrams=number_of_pangrams,rating_thresholds=rating_thresholds, num_valid_words_by_letter=num_valid_words_by_letter, is_bingo_hive=is_bingo_hive, num_valid_words_by_length=num_valid_words_by_length)


#updated for passwords! Alternate Gameplaypage navigated to via a game replay on the user hub.
@app.route("/spellingbee/users/<int:user_id>/<int:game_id>")
def show_game_replay_page(user_id, game_id):
    if "user_id" not in session:
        flash("You must be logged in to view", "error")
        return redirect("/spellingbee/loginsignup")
    else:
        int_user_id=int(user_id)
        int_game_id=int(game_id)
        form=Guessform()
        dictionaryform=Dictionaryform()
        
        if session.get("game_id", "empty")!="empty":
            session_game_id=int(session["game_id"])
            #updating game database with previous game's session data
            sessiongamequery=Game.query.get_or_404(session_game_id)
            sessiongamequery.rating=session["rating"]
            sessiongamequery.letters=session["letters"]
            sessiongamequery.center_letter=session["center_letter"]
            sessiongamequery.guessed_words=session["guessed_words"]
            sessiongamequery.all_valid_words=session["all_valid_words"]
            sessiongamequery.num_words=session["num_words"]
            sessiongamequery.num_valid_words=session["num_valid_words"]
            sessiongamequery.valid_pangrams=session["valid_pangrams"]
            sessiongamequery.guessed_pangrams=session["guessed_pangrams"]
            sessiongamequery.score=session["score"]
            sessiongamequery.total_points=session["total_points"]
            sessiongamequery.removed_center_letter=session["removed_center_letter"]
            db.session.commit()
            flash("Previous Board Saved!! Now continuing to your replay!" , "success")
            print("the previous game session has been saved to the game DB entry! Continuing with the current board!")
        else:
            flash("no previous board to save, Now continuing to your replay!",)
        clear__all_sessions()
        user=User.query.get_or_404(int_user_id)
        gamequery=Game.query.get_or_404(int_game_id)
        print("testing the session from the game replay!")
        print(f"here is session score after the sessionreset---> {session['score']}")

        #updating the session with the game from the database we are pulling for the replay

        session["rating"]=gamequery.rating
        session["letters"]=gamequery.letters
        session["center_letter"]=gamequery.center_letter
        session["guessed_words"]=gamequery.guessed_words
        session["all_valid_words"]=gamequery.all_valid_words
        session["num_words"]=gamequery.num_words
        session["num_valid_words"]=gamequery.num_valid_words
        session["valid_pangrams"]=gamequery.valid_pangrams
        session["guessed_pangrams"]=gamequery.guessed_pangrams
        session["score"]=gamequery.score
        session["total_points"]=gamequery.total_points
        session["game_id"]=gamequery.id
        session["removed_center_letter"]=gamequery.removed_center_letter
        print("testing the session from the game replay!")
        print(f"here is session score after the db.query---> {session['score']}")
        num_valid_words_by_letter=get_words_by_letter(session["all_valid_words"])
        num_valid_words_by_length=get_words_by_length(session["all_valid_words"])

        return render_template("home.html", user=user,game=gamequery, form=form, dictionaryform=dictionaryform, user_id=int_user_id, game_id=int_game_id, num_valid_words_by_letter=num_valid_words_by_letter, num_valid_words_by_length=num_valid_words_by_length)

# API Route Saving/Updating a game
# This route is not restful! It has to be a get because it is currently utilized as an anchor tag in game ui. As data is changed it violated resfulconvention for GET route Should we change this?
@app.route("/spellingbee/save")
def save_game():
    if session.get("game_id", "empty")!="empty":
        session_game_id=int(session["game_id"])
        sessiongamequery=Game.query.get_or_404(session_game_id)
        user_id=sessiongamequery.user_id
        sessiongamequery.rating=session["rating"]
        sessiongamequery.letters=session["letters"]
        sessiongamequery.center_letter=session["center_letter"]
        sessiongamequery.guessed_words=session["guessed_words"]
        sessiongamequery.all_valid_words=session["all_valid_words"]
        sessiongamequery.num_words=session["num_words"]
        sessiongamequery.num_valid_words=session["num_valid_words"]
        sessiongamequery.valid_pangrams=session["valid_pangrams"]
        sessiongamequery.guessed_pangrams=session["guessed_pangrams"]
        sessiongamequery.score=session["score"]
        sessiongamequery.total_points=session["total_points"]
        sessiongamequery.removed_center_letter=session["removed_center_letter"]
        db.session.commit()
        flash(" Board Saved!!" , "success")
        print("the previous game's session has been saved to the game DB entry! Continuing with the current board!")
        return redirect(f"/spellingbee/users/{user_id}/game/{session_game_id}")
    else:
        flash(" no game stored in the session!" , "error")
        print("There was nothing in the session to save!")
        return redirect("/spellingbee/users")
    
@app.route("/spellingbee/validate", methods=["POST"])
def validate_word():
    print(f"printing request.json")
    wordguess=request.json["word"]
    response=validate_word_from_session(wordguess)
    print(f"printing the response----> {response}")
    return jsonify({'result': response,
                    "rating":session["rating"],
                    "letters":session["letters"],
                    "center_letter":session["center_letter"],
                    "guessed_words":session["guessed_words"],
                    "all_valid_words":session["all_valid_words"],
                    "num_words":session["num_words"],
                    "num_valid_words":session["num_valid_words"],
                    "valid_pangrams":session["valid_pangrams"],
                    "guessed_pangrams":session["guessed_pangrams"],
                    "score":session["score"],
                    "total_points":session["total_points"],
                    "removed_center_letter":session["removed_center_letter"],
                    "game_id":session["game_id"]
                    })

                   
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
#     return (jsonify(new_cupcake=serialized_new_cupcake),20int_user_id)

# @app.route("/api/cupcakes/<cupcake_id>", methods=["DELETE"])
# def del_a_cupcake(cupcake_id):
#     int_cupcake_id=int(cupcake_id)
#     cupcake=Cupcake.query.get_or_404(int_cupcake_id)
#     db.session.delete(cupcake)
#     db.session.commit()
#     return jsonify({"message":f"Successfully Deleted Cupcake with an id of {cupcake.id}"})

# #Several approaches to this patch route which I will detail.

# #int_user_id replace with all fields found in request.json. This method is good if the user doesn't want to update all fields. However, if anything doesn't conform to the model we will get a bug,which is possible.

# # @app.route("/api/cupcakes/<cupcake_id>", methods=["PATCH"])
# # def edit_a_cupcake_vint_user_id(cupcake_id):
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
# 		"image": "https://tinypic.host/images/2024/03/25/vegan-lemon-cupcakes-int_user_id..jpeg",
# 		"rating": 7.0,
# 		"size": "small"
# 	}
# }


