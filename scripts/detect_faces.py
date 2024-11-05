'''
detect_faces.py

Given an image of a person or a group of people, this script returns the names
of the people in the image, if they are in the database.
'''

import sys
from modules.utils import image_exists
from modules.db_manager import DBManager
from modules.recognize_face import RecognizeFace


def main(image_path):
    db_manager = DBManager()
    recognize_face = RecognizeFace()

    unrecognized_faces = recognize_face.recognizeFaces(image_path)
    if unrecognized_faces:
        recognize_face.addNewFaces(unrecognized_faces, image_path)
        _, image_cv2 = recognize_face.recognizeFaces(image_path)

    db_manager.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 -m scripts.detect_faces [file]")
        sys.exit(1)
    
    image = sys.argv[1]
    if not image_exists(image):
        print(f"FILE ERROR: `{image}` is not an image")
        sys.exit(1)

    main(image)