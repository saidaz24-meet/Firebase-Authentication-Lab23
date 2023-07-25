from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
from datetime import datetime
import pyrebase

Config = {
  "apiKey": "AIzaSyC7KO2UQhGdrsGwg3TjYHFDk2QnLWcLNT8",
  "authDomain": "fir-first-36fdf.firebaseapp.com",
  "projectId": "fir-first-36fdf",
  "storageBucket": "fir-first-36fdf.appspot.com",
  "messagingSenderId": "409870507993",
  "appId": "1:409870507993:web:f9eb82c154e264b4ebc3c8",
  "measurementId": "G-9XX54YSZ57",
  "databaseURL" : "https://fir-first-36fdf-default-rtdb.firebaseio.com/"
    }

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            print("YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            UID = login_session['user']['localId']
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"email":request.form['email'],
            "password":request.form['password'],
            "full_name":request.form['full_name'],
            "username":request.form['username'],
            "bio":request.form['bio']}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error = ""
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if request.method == 'POST':

        try:
           
            tweet = {"Title":request.form['Title'],
            "Text":request.form['Text'],
            "uid": login_session['user']['localId'],
            "Timestamp" : dt_string
            }
            db.child("Tweets").push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            error = "Authentication failed"
   
    return render_template("add_tweet.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/all_tweets')
def all_tweets():
    
    return render_template("tweets.html",
        tweets = db.child("Tweets").get().val())

if __name__ == '__main__':
    app.run(debug=True)