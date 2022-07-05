CSCI E14A - Building Interactive Web Applications for Data Analysis

# Image based ASL Interpretor Web Application

## Project Plan

**Meeting Times**: TBD

**Zoom Link**: provided on-demand

**Github Repo**: <<https://github.com/Harvard-DCE-BIWADA/S14A2022-final-nsxy>>

**Website Design Template**: 

**Website Location**: 

### Team Members

Shaoyi Li - shl183@g.harvard.edu


## Project Basics

Background about American Sign Language (ASL): https://en.wikipedia.org/wiki/American_Sign_Language

The purpose of this project is to help deaf & mute people to communicate using ASL with who doesn't know ASL. While we can ask deaf & mute people to learn typing but it'd be greatly useful if they don't touch keyboards in the middle of a presentation going through slides or annotating on a whiteboard. 

By the end of the semester we'll aim to be able to intepret English alphabet (instead of the whole ASL vocabulary) as this is a 7-week semester.

We'll provide web interface for users to upload or connect with the PC's camera. For each of the frames in the video, we intepret the American Sign Language gesture into an English letter. The history of the English letters of the video will be shown in the web page as the scripts. Users will need to have their own login to use the web interface and scripts in the past will be save for each account. We can also show the user the words with top frequecy. It will look something like in the below link but we'll try to make it more user interactive: https://public.roboflow.com/object-detection/american-sign-language-letters

We plan to use the database to score information per account and use flask framework for the web interface.


## Project Structure

/app/ - The folder containing the app.
/app/app.py - The main app entry point
/app/templates - Where the templates live.

/app/static - Static files, etc.

/framework/ - ???.

The main components of the app are:

1. **Base** - This module contains the skeleton that the entire framework rests on. It is responsible
   for checking for compatibility, as well as loading and securing the various sub-modules.

2. **Component Model** - This component uses mediapipe and our own ML models to translate images to English letters

3. **Component Frontend** - This component interacts with the users

4. **Component Database** - This component stores information per user account

## Project Timeline

# Milestone 1 Tasks
Xiaokang Zhang

- Github repository setup **COMPLETE**


Shaoyi Li

- README.md; Project description **COMPLETE**
- Obtain dataset **COMPLETE**
> Available from https://app.roboflow.com/ds/h6WIr3ZefA?key=IEDTxWuwkA
- Make sure mediapipe works with the dataset **COMPLETE**


# Milestone X Tasks


1. Task 1 **COMPLETE**
2. Task 2 **IN PROCESS**
3. Task 3 **IN PROCESS**
   ​
   Lady Gaga
   ​
4. Task 1 **COMPLETE**
5. Task 2 **IN PROCESS**
6. Task 3 **IN PROCESS**
   ​
   Sam Cooke
   ​
7. Task 1 **COMPLETE**
8. Task 2 **IN PROCESS**
9. Task 3 **IN PROCESS**
   ​

# References & Citations

​
Lee, D. (2020, October 15). Using computer vision in helping the deaf and hard of hearing communities with yolov5. Medium. Retrieved July 4, 2022, from https://daviddaeshinlee.medium.com/using-computer-vision-in-helping-the-deaf-and-hard-of-hearing-communities-with-yolov5-7d764c2eb614 

