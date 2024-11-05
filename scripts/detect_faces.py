'''
detect_faces.py

Given an image of a person or a group of people, this script returns the names
of the people in the image, if they are in the database.
'''

import sys
from modules.utils import image_exists
from modules.db_manager import DBManager
from modules.recognize_face import RecognizeFace


def main(arg):
    if not image_exists(arg):
        print(f"FILE ERROR: `{arg}` is not an image")
        sys.exit(1)

    db_manager = DBManager()
    recognize_face = RecognizeFace()

    recognize_face.recognizeFaces(arg)
    db_manager.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 -m scripts.detect_faces [file]")
        sys.exit(1)

    main(sys.argv[1])