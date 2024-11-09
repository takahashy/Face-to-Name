# Face-to-Name
There are 3 main features of this program.

1. Given an image of a person or a group photo, returns the name(s) of the people, if they are in the database. AI asks the name for unrecognized faces and also asks whether the returned names of known faces are correct.
2. Train the model by supplying it faces of a certain person in the `data` directory. The images should be in a data's subdirectory with the person's name: `data/name/img1.png`. The images should be a png, jpeg, or jpg file
3. Return the images of a person that a user asks for, assuming that the person is in the database.


# Installations
Make sure you have cmake installed on your computer.

For brew users 
```
brew install cmake
```
Then run the following to install dependencies
```
pip install -r requirements.txt
```

# How To Run
Run all the programs from the root directory using the `-m` flag.

***To create and initialize tables in the database:***
```
python3 -m scripts.db_init
```
***To add images from the data directory and train the model:***
```
python3 -m scripts.add_new_faces <"all" | name_of_subdir>
```
***To recognize and return the names of people in a photo:***
```
python3 -m scripts.detect_faces <image_file>
```
***To get the images of a person:***
```
python3 -m scripts.get_faces
```

