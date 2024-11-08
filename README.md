# Face-to-Name
Given an image of a person or a group photo, returns the name of the person if in the database

# Installations
Make sure you have cmake installed on your computer
For brew users 
```
brew install cmake
```
Then run the following to install dependencies
```
pip install -r requirements.txt
```

# How To Run
From the root directory, to run the programs in the scripts directory use the `-m` flag and run the following:
```
python3 -m scripts.db_init
python3 -m scripts.add_new_faces
python3 -m scripts.detect_faces
```

# *********** NOTES FOR ME ***********
### ***Main Flow*** 
1. Give the AI an image of a person or a group photo
2. Check if each person is in the database
3. If AI determines person is in the database, return a picture with the name of that person
4. If AI determines person is NOT in the database, manually check if that person is actually not in the database. If the person is not add picture to database and train AI regardless

    > P1: Real time image capture

### ***MileStone*** 
1. Create the database and manager
    - create the tables `users` and `photos`
    - insert users and photos given the name, embedding of the image, and path to image
    - select all the name and embedding of an image
    > P1: update and delete functions

2. Processing image
    - recognizing the human faces in an image
    - encode them to an embedding
    - train the AI with the name and image

3. Recognizing the names
    - process the image to look for facial features
    - check if the embedding is in the database
    - return the names on the image
