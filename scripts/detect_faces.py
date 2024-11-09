'''
detect_faces.py

Given an image of a person or a group of people, this script returns the names
of the people in the image, if they are in the database.
'''

import sys
from pathlib import Path
from modules.utils import imageExists
from modules.db_manager import DBManager
from modules.recognize_face import RecognizeFace


def main(image_path):
    db_manager = DBManager()
    recognize_face = RecognizeFace()

    unknown, known = recognize_face.recognizeFaces(image_path)
    if recognize_face.checkFaces(unknown, known, image_path):
        recognize_face.recognizeFaces(image_path)

    db_manager.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: python3 -m scripts.detect_faces [file]")
        sys.exit(1)
    
    image = sys.argv[1]
    if not imageExists(image):
        print(f"FILE ERROR: `{image}` is not an image")
        sys.exit(1)

    main(str(Path(image).resolve()))