CSCI E14A - Building Interactive Web Applications for Data Analysis

# Image based ASL Interpretor Web Application

## Project Plan

**Meeting Times**: Friday 4:00-5:00pm 

**Zoom Link**: https://harvard.zoom.us/j/98977983130?pwd=Z0FnZWc0UW5kRndQN3lFTm40WGF1Zz09

**Github Repo**: <<https://github.com/Harvard-DCE-BIWADA/S14A2022-final-nsxy>>

**Heroku Repo**: <<https://git.heroku.com/cryptic-ridge-03408.git>>

**Website Design Template**: Bootstrap 5

**Website Location**: https://cryptic-ridge-03408.herokuapp.com/

### Team Members

Shaoyi Li - shl183@g.harvard.edu, 

Xiaokang(Ken) Zhang - xiz963@g.harvard.edu

Yan Zhang - yaz336@g.harvard.edu

Nikita Nair - nin500@g.harvard.edu

## Project Basics

Background about American Sign Language (ASL): https://en.wikipedia.org/wiki/American_Sign_Language

The purpose of this project is to help deaf & mute people to communicate using ASL with those who doesn't know ASL. While we can ask deaf & mute people to learn typing but it'd be greatly useful if they don't touch keyboards in the middle of a presentation going through slides or annotating on a whiteboard. 

By the end of the semester we aim to be able to intepret English alphabet (instead of the whole ASL vocabulary) as this is a 7-week semester.

We'll provide web interface for users to upload or connect with the PC's camera. For each of the frames in the video, we intepret the American Sign Language gesture into an English letter. The history of the English letters of the video will be shown in the web page as the scripts. Users will need to have their own login to use the web interface and scripts in the past will be saved for each account. We can also show the user the words with top frequecy. It will look something like in the below link but we'll try to make it more user interactive: https://public.roboflow.com/object-detection/american-sign-language-letters

We plan to use the database to store information per account and use flask framework for the web interface.


## Project Structure (to be updated as evolving)

/app/ - The folder containing the app.
/app/app.py - The main app entry point
/app/templates - Where the templates live.

/app/static - Static files, etc.


The main components of the app are:

1. **Input** - This component is about module to handle input - image/video uploaded by users, or content from web camera stream directly. It will also check compatibility - whether the input is the right type within the proper size range. 

2. **Processing** - This module contains tailored machine learning model to process reveived input and generate output, the processing time should be reasonable to achieve desired user experience. Colab notebook for model training: https://colab.research.google.com/drive/1Tuok_HFhSaD7UQCsoKiHDVf9lvWsp6kU?usp=sharing

3. **Output** - This component is to show the output - letters in scripts (or edited video, to be investigated and confirmed) in desired format. 

4. **Database** - This component stores information per user account, user ID & password, logging, letters, blabs etc. 

5. **Security** (to be investigated and confirmed) - This part contains user registration, authentication, etc. E.g., users need to provide valid email addresses for registration, and validation is needed if users want to upload files in the website.

6. **Visualization** (to be confirmed later)- This part is to describe models in a visual way, and illustrate key user activities in the webside (frequency, etc.)  


## Key Packages
- **sklearn:** We need the colab version in order to load pickled models. Please use `pip install -Iv scikit-learn==1.0.2` to sync-up
- **mediapipe:** We use this to transform pictures to hand landmarks. Overview and examples: https://google.github.io/mediapipe/solutions/hands.html
- **opencv-python-headless:** needed to run cv2 on Heroku. Add this to requirements.txt `opencv-python-headless==4.6.0.66`. We also need the Apt file for other system libraries


## Project Timeline

### Milestone 1 Tasks
Xiaokang Zhang
- Github repository setup **COMPLETE**

Shaoyi Li
- README.md; Project description **COMPLETE**
- Obtain dataset **COMPLETE**
> Available from https://app.roboflow.com/ds/h6WIr3ZefA?key=IEDTxWuwkA
- Make sure mediapipe works with the dataset **COMPLETE**
> Mediapipe Hands example: https://google.github.io/mediapipe/solutions/hands.html#python-solution-api

### Milestone 2 Tasks
Xiaokang Zhang
- Update README per discussion **COMPLETE**
- Readjust team meeting time to accommodate all members **COMPLETE**
- Use issue features to track and assign tasks **COMPLETE**


Nikita Nair  
- Build a basic website and put it on Heroku **COMPLETE**
- https://arcane-reef-02788.herokuapp.com/ <-- not used anymore

Shaoyi Li
- Create a model (image as input) and output letter **COMPLETE**. Test accuracy: 81%, okay but not great. Check **Processing** section above for the Colab link.
- Push model related info to a Git folder: ml_model **COMPLETE**

Yan Zhang
- Investigate 'how to connect webcam via web UI and pull frames from the stream/uploaded videoes'
- https://pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/
 **IN PROCESS**
 
 
 ### Milestone 3 Tasks
Xiaokang Zhang
- Create a new branch (ken_dev) and make it workable locally (mainly commenting out exploration code for video stream handling) **COMPLETE**
- Add 'about' page (index) describing overall project - purpose, approach, backgroud, etc. **COMPLETE**
- Build 'Image Interpretation' page - allowing users to upload image, get it displayed and show results **COMPLETE**

Nikita Nair  
- Build and upload login and create account forms for user sign in and user sign up **COMPLETE**

Shaoyi Li
- Add a models folder with .py and .pkl so that the app can predict a given image **COMPLETE**
- Make intepretation2.html and app.py to predict ASL letters from images **COMPLETE**
- Make intepretation and intepretation2.html handle corner cases more gracefully. **COMPLETE**
- Heroku app setup -- fix the installation issues and grant access to the team **COMPLETE** 
> Updated link: https://cryptic-ridge-03408.herokuapp.com/
- Polish index.html **COMPLETE**

Yan Zhang
- Heroku app setup **COMPLETE**

### Milestone 4 Tasks
Shaoyi Li
- make camera frames passed from browser to flask server **COMPLETE**
- fix the server memory issue (exceeding heorku's limit) in image prediction **COMPLETE**
- make mediapipe call happening in Javascript (clients' browser) and pass the mdeiapipe's output to flask server **COMPLETE**
- fix the issue that mediapipe's Javascript call is processing too fast which makes client to freeze  **COMPLETE**
- add a spinner when mediapipe's Javascript is loading **COMPLETE**
- add a button to start and pause the video streaming **COMPLETE**
- add a button to flip camera horizontally for self facing camera (default to self facing) **COMPLETE**
- make elements responsive **COMPLETE**
- fix the issue that navbar is not responsive **COMPLETE**


### Milestone Final Tasks
Xiaokang Zhang
- Add login/signup features and flash alerting **COMPLETE**
- Create a new tab "community" allowing users to post messages **COMPLETE**
- Set up database for user, blab **COMPLETE**
- add protection features of "image upload", only open to loggedin users **COMPLETE**
- Investigage image storage in database 

Shaoyi Li
- Add a script box to record the history of predicted letters between video start and stop **COMPLETE**
- Add a slider to tune the probability threshold for script recording **COMPLETE**
- Add tooltip for flipcam button and the threshold slider **COMPLETE**
 


# Primary responsibility

Shaoyi
- Training/validation/testing datasets
- ML model research, training, prediction
- Video streaming (2 options)
- Javascript features
- Add new web elements for complete functionalities
- Fix Heroku issues (deployment, memory and database)
- Testing, bug fixing and code cleaning ups for the whole project.
- MVP and Final presentation
- Track the project progress and arrange meetings
- Keep readme.md up-to-date

Xiaokang
- image upload features
- login/signup features
- community features
- help updating readme.md
- help with logistics - meeting setup, progress tracking in github "issues"

# References & Citations

​
Lee, D. (2020, October 15). Using computer vision in helping the deaf and hard of hearing communities with yolov5. Medium. Retrieved July 4, 2022, from https://daviddaeshinlee.medium.com/using-computer-vision-in-helping-the-deaf-and-hard-of-hearing-communities-with-yolov5-7d764c2eb614 

