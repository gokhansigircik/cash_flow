from flask_app import app, bcrypt
from flask import render_template, request, redirect, session, flash

from flask_app.models.user_model import User

#--- STEPS TO START USING APU IN PYTHON ---#
# 1. install request ----> python3 -m pip install requests 
# 2. import requests

import requests
# from YelpAPI import get_my_key
# define a bussiness ID
# bussines_id =

# define THE API KEY, DEFINE THE END POINT, define the header
# API_KEY = get_my_key()
# endpoint = 'http;//yelp.com/buss/search
# headers = we have to pass along to our api key to get autorization from yelp
# headers = {'Authorization': 'bearer %s' % API_KEY}

# DEFINE THE PAREMETERS
# PARAMETERS = {'term':'coffee'
#                 'limit':50,
#                 'radius': 10000,
#                 'location':'Dallas'
# }
# make a request to the yelp API_KEY
# res = requests.get(url= endpoint, params= Parameters, headers=Headers)

# convert the json string to a dict
# bussiness_data = response.json()

# print(bussiness_data.key())

# for biz in bussiness_data['bussiness']:
#     print(biz['name'])

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/register_page")
def register():
    return render_template('register.html')

@app.route("/new_user")
def go_back():
    return redirect('/')


# *******- Check login credentials, creates user session - moves to next page -****************
@app.route("/login", methods=["POST"])
def login():

    logged_in_user = User.validate_login(request.form)
    
    if not logged_in_user:
        return redirect("/")

    session['uid'] = logged_in_user.id
    session['fname'] = logged_in_user.first_name

    return redirect('/view/all')


# *******- Registers a new user -****************

@app.route('/new_user', methods=['POST'])
def new_user():


    register_check = User.validate(request.form)
    if not register_check:
        return redirect('/register_page')

    hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hash
    }

    User.register(data)
    return redirect("/")


# *******- Clears user from session (logout) -****************
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')