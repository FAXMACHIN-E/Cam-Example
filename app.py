
# import the necessary packages
from flask import Flask, render_template, request,session
import gunicorn
# from imutils.video import VideoStream
# from flask import Response
# import threading
# import argparse
# import datetime
# import imutils
# import time
import cv2
import os
import numpy as np
import joblib
import mediapipe as mp
from werkzeug.utils import secure_filename

from models.predict_img import predict_image_letters




# outputFrame = None
# lock = threading.Lock()

app = Flask(__name__)

model_xtree = joblib.load(os.path.join(app.root_path, 'models', 'xtree.pkl'))


mphands = mp.solutions.hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.3
)

# vs = VideoStream(src=0).start()
# time.sleep(2.0)

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

        pred = predict_image_letters([img], model_xtree)[0]
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

        pred = predict_image_letters([img], model_xtree, mphands=mphands)[0]
        letter, prob = pred

        pred_str = 'No ASL Detected' if letter is None else (
            f'Letter: {letter} (prob: {prob * 100:.1f}%)'
        )

        return pred_str
        # return render_template(
        #     'video.html', pred=pred_str, val=pred_str
        # )
    
    


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



        
# def detect_motion(frameCount):
# 	# grab global references to the video stream, output frame, and
# 	# lock variables
# 	global vs, outputFrame, lock
# 	# initialize the motion detector and the total number of frames
# 	# read thus far
# 	# md = SingleMotionDetector(accumWeight=0.1)
# 	total = 0
#     	# loop over frames from the video stream
# 	while True:
# 		# read the next frame from the video stream, resize it,
# 		# convert the frame to grayscale, and blur it
# 		frame = vs.read()
# 		frame = imutils.resize(frame, width=400)
# 		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 		gray = cv2.GaussianBlur(gray, (7, 7), 0)
# 		# grab the current timestamp and draw it on the frame
# 		timestamp = datetime.datetime.now()
# 		cv2.putText(frame, timestamp.strftime(
# 			"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
# 			cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
#         		# if the total number of frames has reached a sufficient
# 		# number to construct a reasonable background model, then
# 		# continue to process the frame
# 		# if total > frameCount:
# 		# 	# detect motion in the image
# 		# 	motion = md.detect(gray)
# 		# 	# check to see if motion was found in the frame
# 		# 	if motion is not None:
# 		# 		# unpack the tuple and draw the box surrounding the
# 		# 		# "motion area" on the output frame
# 		# 		(thresh, (minX, minY, maxX, maxY)) = motion
# 		# 		cv2.rectangle(frame, (minX, minY), (maxX, maxY),
# 		# 			(0, 0, 255), 2)
#
# 		# update the background model and increment the total number
# 		# of frames read thus far
# 		#md.update(gray)
# 		#total += 1
# 		# acquire the lock, set the output frame, and release the
# 		# lock
# 		with lock:
# 			outputFrame = frame.copy()
#
# def generate():
# 	# grab global references to the output frame and lock variables
# 	global outputFrame, lock
# 	# loop over frames from the output stream
# 	while True:
# 		# wait until the lock is acquired
# 		with lock:
# 			# check if the output frame is available, otherwise skip
# 			# the iteration of the loop
# 			if outputFrame is None:
# 				continue
# 			# encode the frame in JPEG format
# 			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
# 			# ensure the frame was successfully encoded
# 			if not flag:
# 				continue
# 		# yield the output frame in the byte format
# 		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
# 			bytearray(encodedImage) + b'\r\n')

# @app.route("/video_feed")
# def video_feed():
# 	# return the response generated along with the specific media
# 	# type (mime type)
# 	return Response(generate(),
# 		mimetype = "multipart/x-mixed-replace; boundary=frame")
# # check to see if this is the main thread of execution
# if __name__ == '__main__':
# 	# construct the argument parser and parse command line arguments
# 	ap = argparse.ArgumentParser()
# 	ap.add_argument("-i", "--ip", type=str, required=True,
# 		help="ip address of the device")
# 	ap.add_argument("-o", "--port", type=int, required=True,
# 		help="ephemeral port number of the server (1024 to 65535)")
# 	ap.add_argument("-f", "--frame-count", type=int, default=32,
# 		help="# of frames used to construct the background model")
# 	args = vars(ap.parse_args())
# 	# start a thread that will perform motion detection
# 	t = threading.Thread(target=detect_motion, args=(
# 		args["frame_count"],))
# 	t.daemon = True
# 	t.start()
# 	# start the flask app
# 	app.run(host=args["ip"], port=args["port"], debug=True,
# 		threaded=True, use_reloader=False)
# # release the video stream pointer
# vs.stop()
