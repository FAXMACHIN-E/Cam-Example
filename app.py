
# import the necessary packages
from flask import Flask, render_template, request, session, redirect, url_for
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


app = Flask(__name__)

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
    
    return render_template('index.html')

# for image upload and storage

upload_folder = os.path.join('static','uploads')
allowed_extensions = {'jpg','jpeg','gif','png'}
app.config['UPLOAD_FOLDER'] = upload_folder
app.secret_key = 'finalprojectsecretkey'

@app.route('/image_interpretation')
def image_interpretation():
    return render_template('image_interpretation.html')


@app.route('/image_interpretation',methods=('POST','GET'))
def upload_image():
    if request.method == "POST":
        uploaded_img = request.files['myfile']
        img_filename = secure_filename(uploaded_img.filename)
        
        if len(img_filename) == 0:
            return render_template(
                'image_interpretation2.html',
                img_file_path='""', 
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
            img_file_path=img_file_path, pred=pred_str
        )


@app.route('/mediapipe', methods=['GET'])	
def mpipe():
    return render_template('mediapipe.html')


@app.route('/mediapipe_pred', methods=['POST'])	
def mpipe_pred():
    mp_obj = request.get_json()
    letter, prob = predict_landmark_letters(
        mp_obj['multiHandWorldLandmarks'], model_xtree
    )
    return f'Letter: {letter} (prob: {prob * 100:.1f}%)'


@app.route('/video', methods=['GET'])	
def video():
    return render_template('video.html')


@app.route('/video_pred', methods=['POST'])
def video_pred():
    if request.method != 'POST':
        return ''
    
    file = request.files['image']
    if file:
        fstream = file.read()
        img = cv2.imdecode(
            np.fromstring(fstream, np.uint8), 
            cv2.IMREAD_COLOR
        )
        
        if img is None:
           
            return ''

        pred = predict_image_letters([img], model_xtree, mphands=get_mphands())[0]
        letter, prob = pred

        pred_str = 'No ASL Detected' if letter is None else (
            f'Letter: {letter} (prob: {prob * 100:.1f}%)'
        )

        return pred_str
 


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


# Route for handling the create account page logic
@app.route('/create', methods=['GET', 'POST'])
def create():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('create.html', error=error)
