
# import the necessary packages
from flask import Flask, flash, render_template, request, session, redirect, url_for
import gunicorn
import sklearn
import cv2
import os
import numpy as np
import joblib
import mediapipe as mp
from werkzeug.utils import secure_filename

from prediction_models.predict_img import predict_image_letters
from prediction_models.predict_img_lite import predict_landmark_letters

from dotenv import load_dotenv
from models.models import Db, User,File
from forms.forms import SignupForm, LoginForm
from os import environ
from passlib.hash import sha256_crypt

load_dotenv('.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL').replace('postgres://', 'postgresql://') # this is to solve a bug in heroku
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = environ.get('SECRET_KEY') # Make sure this is set in Heroku dashboard for this new app!
Db.init_app(app)

# set some constants
MAX_STRING_LENGTH   = 64
MIN_PASSWORD_LENGTH = 8 # set something reasonable
MAX_PASSWORD_LENGTH = 128 # see models/model.py
# MAX_BLAB_LENGTH     = 1024

def check_string(str=None, label="", max_length=MAX_STRING_LENGTH):
    # can't have a null value!
    if str == None:
        raise ValueError(f'Variable {label} cannot be null!')

    # strip the string of leading & trailing whitespace
    str = str.strip()

    if str == "":
        raise ValueError(f'Variable {label} is empty!')
    elif len(str) > max_length:
        raise ValueError(f'Variable {label} is too long! {len(str)} > {max_length}')

    return str


def check_int(num=None, label="", min=float('-inf'), max=float('inf')):
    try:
        num = int(num)
    except:
        raise ValueError(f'Variable {label} malformed! ({num})')

    if num < min or num > max:
        raise ValueError(f'Variable {label} is out of range! ({num} <> [{min},{max}])')

    return num


def check_float(num=None, label="", min=float('-inf'), max=float('inf')):
    try:
        num = float(num)
    except:
        raise ValueError(f'Variable {label} malformed! ({num})')

    if num < min or num > max:
        raise ValueError(f'Variable {label} is out of range! ({num} <> [{min},{max}])')

    return num


# NEW Get Error from exception
def get_error(e):
    return e.message if hasattr(e, 'message') else str(e)


# NEW Check Password
# This is only to sanitize passwords for NEW users. Why don't we want to do these checks
# when someone is authenticating? (Hint: security)
def check_password(password=None, label="password", min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH):
    # can't have a null value!
    if password == None:
        raise ValueError(f'Variable {label} cannot be null!')

    # we don't want to strip any characters from the password!

    # string can't be empty
    if password == "":
        raise ValueError(f'Variable {label} is empty!')

    # Need a minimum number of chars
    if len(password) < min_length:
        raise ValueError(f'Variable {label} is too short! {len(password)} < {min_length}')

    # Need a maximum number of chars
    if len(password) > max_length:
        raise ValueError(f'Variable {label} is too long! {len(password)} > {max_length}')

    return password


# This is to ensure the passwords are both valid and the same
def verify_password(password=None, verify=None, min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH):
    password = check_password(password, 'password', min_length, max_length)
    verify = check_password(verify, 'verify', min_length, max_length)

    if password != verify:
        raise ValueError('Passwords do not match!')

    return password, verify  # returns both password & verification


# Get the currently logged in user
def logged_in_user():
    # Three checks:
    # 1. if the username key exists in a session
    # 2. if the username isn't empty
    # 3. if the username is actually valid
    if 'username' in session and session['username'] != "":
        # Will return None if no such user exists
        return User.query.filter_by(username=session['username']).first()
    else:
        return None


# User CRUD
# Create a new user /user/create
@app.route('/user/create', methods=['POST'])
def user_create():
    try:
        # Init credentials from form request
        username = check_string(request.form['username'], 'username', MAX_STRING_LENGTH)
        password, verify = verify_password(request.form['password'], request.form['verify'], MIN_PASSWORD_LENGTH,
                                           MAX_PASSWORD_LENGTH)

        # Does the user already exist?
        user = User.query.filter_by(username=username).first()
        if user:
            raise LookupError(f'User with username "{username}" already exists! Please choose another username.')

            # User is unique, so let's create a new one
        user = User(username=username, password=sha256_crypt.hash(password))
        Db.session.add(user)
        Db.session.commit()

        # Message Flashing
        # https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/#flashing-with-categories
        flash('Congratulations, you are now a registered user!', 'success')

        # Redirect to login page
        return redirect(url_for('login'))
    except Exception as e:
        # show the error
        flash(get_error(e), 'danger')

        # redirect back to signup page
        return redirect(url_for('signup'))


@app.route('/user/retrieve/<username>')
def user_retrieve(username):
    try:
        # user must be logged in to view user profiles!
        user = logged_in_user()
        if user == None:
            raise KeyError('You are not logged in!')  # session key not found!

        # sanitize input
        username = check_string(username, 'username')

        # The logged in user can only see their own profile!
        profile_user = User.query.filter_by(username=username).first()
        if profile_user == None:
            raise KeyError("User does not exist!")
        # if username != user.username:
        #     raise PermissionError( 'Unauthorized action!' )

        # get the user's files
        # Lab7 HW: Use relationships to get these
        # See: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
        files = File.query.filter_by(uploader=profile_user.uid).all()

        return render_template("profile.html", user=user, profile_user=profile_user, files=files,
                               title=f'@{profile_user.username}')

    # Not logged in, go to login page
    except KeyError as ke:
        # show the error
        flash(get_error(ke), 'danger')

        return redirect(url_for('login'))

    # Not authorized, go to index page, could be combined with below
    except PermissionError as pe:
        # show the error
        flash(get_error(pe), 'danger')

        # redirect to index
        # how would we go back to the page we were just at?
        # See: https://tedboy.github.io/flask/generated/generated/flask.Request.referrer.html
        return redirect(url_for('index'))

    # Any other error
    except Exception as e:
        # show the error
        flash(get_error(e), 'danger')

        # redirect back to signup page
        return redirect(url_for('index'))


@app.route('/user/update/<username>', methods=['POST'])
def user_update(username):
    try:
        # user must be logged in to view user profiles!
        user = logged_in_user()
        if user == None:
            raise KeyError('You are not logged in!')

        # sanitize input
        username = check_string(request.form['username'], 'username')
        # if we had additional information for updating, it would be here!
        # variable1 = check_???( request.form['variable1'], 'variable1'
        # variable2 = check_???( request.form['variable2'], 'variable2'
        # variable3 = check_???( request.form['variable3'], 'variable3'

        # The logged in user can only update their own profile!
        if username != user.username:
            raise PermissionError('Unauthorized action!')

        # Hrm..! There's not much to do here! Why don't we want to modify passwords here??? Where would we do it instead?
        # See below
        # if we did have extra variables to update:
        # user.variable1 = variable1
        # user.variable2 = variable2
        # user.variable3 = variable3
        # Db.session.commit()

        # Go back to user profile
        return redirect(url_for(f'user/retrieve/{username}'))

    # Not authorized, go to login page
    except KeyError as ke:
        # show the error
        flash(get_error(ke), 'danger')

        # redirect to login
        return redirect(url_for('login'))

    # Any other error
    except Exception as e:
        # show the error
        flash(get_error(e), 'danger')

        # redirect back to index page (or referrer)
        # if we use this a lot, what could we do?
        last_page = request.referrer if request.referrer else url_for('index')
        return redirect(last_page)


# Update User password
# Q: How would we update the username??
@app.route('/user/update_password/<username>', methods=['POST'])
def user_update_pasword(username):
    try:
        # user must be logged in to view user profiles!
        user = logged_in_user()
        if user == None:
            raise KeyError('You are not logged in!')

        # sanitize username
        username = check_string(request.form['username'], 'username')

        # we can only change our own passwords!
        if (username != user.username):
            raise PermissionError('Unauthorized action!')

        # sanitize & check that the passwords match
        password, verify = verify_password(request.form['password'], request.form['verify'], MIN_PASSWORD_LENGTH,
                                           MAX_PASSWORD_LENGTH)

        # set the password
        user.password = sha256_crypt.hash(password)

        # commit to Db
        Db.session.commit()

        # flash a message to the user
        flash('Password successfully changed!', 'success')

        # return the blab as a json
        return redirect(url_for(f'user/retrieve/{username}'))

    # Not authorized, go to login page
    except KeyError as ke:
        # show the error
        flash(get_error(ke), 'danger')

        # redirect to login
        return redirect(url_for('login'))

    # Any other error
    except Exception as e:
        # show the error
        flash(get_error(e), 'danger')

        # redirect back to index page (or referrer)
        # if we use this a lot, what could we do?
        last_page = request.referrer if request.referrer else url_for('index')
        return redirect(last_page)


# HW: Add /user/delete
# NOTE: This method is DANGEROUS! How could we make it less so?
@app.route('/user/delete/<username>')
def user_delete(username):
    try:
        # user must be logged in to view user profiles!
        user = logged_in_user()
        if user == None:
            raise KeyError('You are not logged in!')

        # sanitize username
        username = check_string(request.form['username'], 'username')

        # we're the only ones who can delete our own user!
        if (username != user.username):
            raise PermissionError('Unauthorized action!')

        # Delete all of the users' blabs
        # Lab7 HW: Use relationships to get these
        # See: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
        files = File.query.filter_by(uploader=user.uid).all()
        for file in files:
            Db.session.delete(file)

        # Delete the user
        Db.session.delete(user)

        # Commit the changes
        Db.session.commit()

        # Our user is dead, so we need to log out!
        return redirect(url_for('logout'))

    # Not authorized, go to login page
    except KeyError as ke:
        # show the error
        flash(get_error(ke), 'danger')

        # redirect to login
        return redirect(url_for('login'))

    # Any other error
    except Exception as e:
        # show the error
        flash(get_error(e), 'danger')

        # redirect back to index page (or referrer)
        # if we use this a lot, what could we do?
        last_page = request.referrer if request.referrer else url_for('index')
        return redirect(last_page)


# Log a user in, if already logged in, log the current user out first!
# GET returns the login form
# blab processes the login form input
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            # Init & sanitize credentials from form request
            username = check_string(request.form['username'], 'username')
            password = check_password(request.form['password'], 'password')
            # print(username, password)
            # Get the user user by Db query
            user = User.query.filter_by(username=username).first()
            if user == None:
                # print('User is None')
                raise KeyError('Invalid username or password')

            # Control login validity
            # we have some unhashed passwords in the database, so we may need to fix them
            if user.password == password:
                user.password = sha256_crypt.hash(password)  # password wasn't hashed so we need to do it now
                Db.session.commit()  # save the password hash
                user = User.query.filter_by(username=username).first()  # get the user back again

            # check the password against the hashed version
            if not sha256_crypt.verify(password, user.password):
                raise PermissionError('Invalid username or password')

            # set the logged in user's username in the session
            session['username'] = username

            # let the user know login was sucessful
            flash(f'{username} is now logged in!', 'success')

            # go to the index page
            return redirect(url_for('index'))

        else:  # GET
            # Get the logged in user
            user = logged_in_user()

            # Init form
            form = LoginForm()

            # Show the login form
            return render_template('login.html', title='Login', form=form, user=user)

    # Any error
    except Exception as e:
        # show the error
        # print('enter exception loop')
        # print(get_error(e))
        flash(get_error(e), 'danger')

        # redirect back to login page
        return redirect(url_for('login'))

    # blab /logout


@app.route('/logout')
def logout():
    # Clear all session data
    session.clear()
    
    flash('Successfully logged out!', 'success')
    # Go back to index page
    return redirect(url_for('index'))


# Register as a new user /signup
@app.route('/user/form/signup')
def signup():
    # Init form
    form = SignupForm()

    return render_template('signup.html', title='Signup', form=form)


@app.route('/user_list')
def user_list():
    users = User.query.all()
    # print('#users:',len(users))
    return render_template('user_list.html',users=users)

###############################################

model_xtree = joblib.load(os.path.join(app.root_path, 'prediction_models', 'xtree.pkl'))

mphands = None

def get_mphands():
    global mphands
    if mphands is None:
        mphands = mp.solutions.hands.Hands(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.3
        )
    return mphands


@app.route('/')
def index():
    # users = User.query.all()
    # print('#users:', len(users))
    # for u in users:
    #     print(u.username,u.password)
    user = logged_in_user()
    return render_template('index.html',user=user)

# for image upload and storage

upload_folder = os.path.join('static','uploads')
allowed_extensions = {'jpg','jpeg','gif','png'}
app.config['UPLOAD_FOLDER'] = upload_folder
app.secret_key = 'finalprojectsecretkey'

@app.route('/image_interpretation')
def image_interpretation():
    try:
        user = logged_in_user()
        # print(user.username)
        # print('----')
        if user == None:
            raise KeyError('You are not logged in!')
        # # sanitize username
        # username = check_string(request.form['username'], 'username')
        # print(username)
        # # we're the only ones who can delete our own user!
        # if (username != user.username):
        #     raise PermissionError('Unauthorized action!')
        return render_template('image_interpretation.html',user=user)
    except KeyError as ke:
        flash( get_error(ke),'danger')
        return redirect(url_for('login'))
    except Exception as e:
        # show the error
        flash(get_error(e), 'danger')

        # redirect back to index page (or referrer)
        # if we use this a lot, what could we do?
        last_page = request.referrer if request.referrer else url_for('index')
        return redirect(last_page)





@app.route('/image_interpretation',methods=('POST','GET'))
def upload_image():
    user = logged_in_user()
    if request.method == "POST":
        uploaded_img = request.files['myfile']
        img_filename = secure_filename(uploaded_img.filename)
        
        if len(img_filename) == 0:
            return render_template(
                'image_interpretation2.html',
                img_file_path='""',
                user=user,
                pred='<span style="color:red">No file uploaded</span>'
            )

        local_img_filename = 'asl.jpg'
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], local_img_filename))
        session['uploaded_img_file_path'] = os.path.join(
            app.config['UPLOAD_FOLDER'], local_img_filename
        )
        img_file_path = session.get('uploaded_img_file_path', None)
        
        img = cv2.imread(img_file_path)

        if img is None:
            return render_template(
                'image_interpretation2.html',
                img_file_path='""',
                user=user,
                pred=(
                    '<span style="color:red">Invalid file uploaded: '
                    f'{img_filename}</span>'
                )
            )

        pred = predict_image_letters([img], model_xtree, mphands=get_mphands())[0]
        letter, prob = pred

        pred_str = (
            '<span style="font-size: 18pt;color:grey">'
            'No ASL Detected</span>'
        ) if letter is None else (
            f'Letter: {letter} (prob: {prob * 100:.1f}%)'
        )
        return render_template(
            'image_interpretation2.html',
            img_file_path=img_file_path, pred=pred_str,user=user
        )


@app.route('/mediapipe', methods=['GET'])	
def mpipe():
    user = logged_in_user()
    return render_template('mediapipe.html',user=user)


@app.route('/mediapipe_pred', methods=['POST'])	
def mpipe_pred():
    mp_obj = request.get_json()
    letter, prob = predict_landmark_letters(
        mp_obj['multiHandWorldLandmarks'], model_xtree
    )
    # return f'{letter}|{prob * 100:.1f}%'
    return f'{letter}|{prob:.5f}%'


@app.route('/video', methods=['GET'])	
def video():
    user = logged_in_user()
    return render_template('video.html',user=user)


@app.route('/video_pred', methods=['POST'])
def video_pred():    
    file = request.files['image']
    if not file:
        return ' |0'
    else:
        fstream = file.read()
        img = cv2.imdecode(
            np.fromstring(fstream, np.uint8), 
            cv2.IMREAD_COLOR
        )
        
        if img is None:
            return ' |0'

        pred = predict_image_letters([img], model_xtree, mphands=get_mphands())[0]
        letter, prob = pred

        # pred_str = 'No ASL Detected' if letter is None else (
        #     f'Letter: {letter} (prob: {prob * 100:.1f}%)'
        # )

        pred_str = f'{" " if letter is None else letter}|{prob:.5f}'

        return pred_str
 

#
# # Route for handling the login page logic
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             return redirect(url_for('home'))
#     return render_template('login.html', error=error)
#
#
# # Route for handling the create account page logic
# @app.route('/create', methods=['GET', 'POST'])
# def create():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             return redirect(url_for('home'))
#     return render_template('create.html', error=error)
