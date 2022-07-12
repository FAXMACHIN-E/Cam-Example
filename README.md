CSCI E14A - Building Interactive Web Applications for Data Analysis

# Image based ASL Interpretor Web Application

## Project Plan

**Meeting Times**: Friday 4:00-5:00pm 

**Zoom Link**: https://harvard.zoom.us/j/98977983130?pwd=Z0FnZWc0UW5kRndQN3lFTm40WGF1Zz09

**Github Repo**: <<https://github.com/Harvard-DCE-BIWADA/S14A2022-final-nsxy>>

**Website Design Template**: Not required for our project

**Website Location**: Herolu link (to be updated)

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

/framework/ - ???.

The main components of the app are:

1. **Input** - This component is about module to handle input - image/video uploaded by users, or content from web camera stream directly. It will also check compatibility - whether the input is the right type within the proper size range. 

2. **Processing** - This module contains tailored machine learning model to process reveived input and generate output, the processing time should be reasonable to achieve desired user experience. Colab notebook for model training: https://colab.research.google.com/drive/1Tuok_HFhSaD7UQCsoKiHDVf9lvWsp6kU?usp=sharing

3. **Output** - This component is to show the output - letters in scripts (or edited video, to be investigated and confirmed) in desired format. 

4. **Database**(optional) - This component stores information per user account, user ID & password, logging, uploaded files, etc. 

5. **Security** (to be investigated and confirmed) - This part contains user registration, authentication, etc. E.g., users need to provide valid email addresses for registration, and validation is needed if users want to upload files in the website.

6. **Visualization** (to be confirmed later)- This part is to describe models in a visual way, and illustrate key user activities in the webside (frequency, etc.)  


## Project Timeline

# Milestone 1 Tasks
Xiaokang Zhang
- Github repository setup **COMPLETE**

Shaoyi Li
- README.md; Project description **COMPLETE**
- Obtain dataset **COMPLETE**
> Available from https://app.roboflow.com/ds/h6WIr3ZefA?key=IEDTxWuwkA
- Make sure mediapipe works with the dataset **COMPLETE**

# Milestone 2 Tasks
Xiaokang Zhang
- Update README per discussion **COMPLETE**
- Readjust team meeting time to accommodate all members **COMPLETE**
- Use issue features to track and assign tasks **COMPLETE**


Nikita Nair  
- Build a basic website and put it on Heroku **IN PROCESS**

Shaoyi Li
- Create a model (image as input) and output letter **Complete**. Test accuracy: 81%, okay but not great. Check **Processing** section above for the Colab link.
- Push model related info to a Git folder: ml_model **Complete**

Yan Zhang
- Investigate 'how to connect webcam via web UI and pull frames from the stream/uploaded videoes'
 **IN PROCESS**
 
# Actions in the future 
- Add 'about' page to the website, e.g., how to help deal/mute people

# References & Citations

​
Lee, D. (2020, October 15). Using computer vision in helping the deaf and hard of hearing communities with yolov5. Medium. Retrieved July 4, 2022, from https://daviddaeshinlee.medium.com/using-computer-vision-in-helping-the-deaf-and-hard-of-hearing-communities-with-yolov5-7d764c2eb614 

