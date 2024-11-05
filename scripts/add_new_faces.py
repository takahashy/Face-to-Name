'''
add_new_faces.py

Given an image or images of a person or a group of people, 
this script adds the faces to the database. 
'''

import sys
from modules.db_manager import DBManager
from modules.recognize_face import RecognizeFace
from modules.utils import directory_exists, file_exists


def main(arg):
    pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: python3 add_new_faces.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    if not directory_exists(image_path):
        print(f"DIRECTORY ERROR: `{image_path}` is not a directory")

    main(sys.argv[1])