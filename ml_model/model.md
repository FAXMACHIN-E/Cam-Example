# Data Processing and Training
## Pickle files
- **landmark_sets.pkl**: processed data from image files. X (landmarks), y (labels, 0-25) and indices (from original csv file, as some images are discarded). 3 sets: train, valid and test
- **xtree.pkl**: ExtaTrees model, landmarks -> labels. 81% test accuracy
