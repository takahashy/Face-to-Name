'''
recognize_face.py

This module is used to process the face images, extract the embeddings, and recognize the faces.
The image to be processed is given either as a user prompt or from the data directory.
If the person is not in the database, 
'''

import cv2
import numpy as np
import face_recognition
from typing import Tuple
from modules.db_manager import DBManager

# TODO: create a method that recognizes the face and returns the name
# TODO: create a method that adds a new face to the database

class RecognizeFace:

    def __init__(self):
        """
        users is a dictionary where key is embeddings and value is (name, face_path)
        """
        self.db = DBManager()
        self.names, self.face_paths, self.embeddings = self.db.fetchFaces()

    
    def recognizeFaces(self, image_path: str):
        """
        Given a path to an image, return that image with names for each person
        and the locations of unrecognized faces
        """
        face_locations, face_embeddings = self.__processImage(image_path)
        unrecognized_faces = []

        image_cv2 = cv2.imread(image_path)

        for (top, right, bottom, left), embedding in zip(face_locations, face_embeddings):
            matches = face_recognition.compare_faces(self.embeddings, embedding)
            distances = face_recognition.face_distance(self.embeddings, embedding)
            best_match_index = np.argmin(distances) if distances else -1

            name = "Unknown"
            if matches and matches[best_match_index]:
                name = self.names[best_match_index]

            if name == "Unknown":
                unrecognized_faces.append(((top, right, bottom, left), embedding))

            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(image_cv2, (left, bottom), (right, top), color, 2)
            cv2.putText(image_cv2, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.imshow("Recognizing Faces", image_cv2)
        cv2.waitKey(0)

        return unrecognized_faces, image_cv2

        



### private methods
    def __processImage(self, image_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Given a path to an image, return the location and embeddings 
        of each face in image
        """
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        face_embeddings = face_recognition.face_encodings(image, face_locations)
        return (face_locations, face_embeddings)