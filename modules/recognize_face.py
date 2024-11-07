'''
recognize_face.py

This module is used to process the face images, extract the embeddings, and recognize the faces.
The image to be processed is given either as a user prompt or from the data directory.
If the person is not in the database, 
'''

import cv2
import numpy as np
import face_recognition
from typing import Tuple, List
from modules.utils import processImage
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

    def recognizeFaces(self, image_path: str) -> List[Tuple]:
        """
        Given a path to an image, return list of unrecognized faces 
        """
        face_locations, face_embeddings = processImage(image_path)
        unrecognized_faces = []

        image_cv2 = cv2.imread(image_path)

        for (top, right, bottom, left), embedding in zip(face_locations, face_embeddings):
            matches = face_recognition.compare_faces(self.embeddings, embedding)
            distances = face_recognition.face_distance(self.embeddings, embedding)
            best_match_index = np.argmin(distances) if len(distances) != 0 else -1

            name = "Unknown"
            if matches and matches[best_match_index]:
                name = self.names[best_match_index]

            if name == "Unknown":
                unrecognized_faces.append(((top, right, bottom, left), embedding))

            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(image_cv2, (left, bottom), (right, top), color, 2)
            cv2.putText(image_cv2, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        self.showImage(image_cv2)
        return unrecognized_faces


    def addNewFaces(self, unrecognized_faces: List[Tuple], image_path: str) -> None:
        """
        Given a list of unrecognized faces and path to image
        add them to the database. Ask the user for the name
        """

        for (top, right, bottom, left), embedding in unrecognized_faces:
            image_cv2 = cv2.imread(image_path)
            cv2.rectangle(image_cv2, (left, bottom), (right, top), (255, 0, 0), 3)
            self.showImage(image_cv2, 2)
            name = input("Enter the name of the person: ").strip()

            self.db.insertFaces(name, [image_path], [embedding])
            self.names.append(name) if name not in self.names else None
            self.face_paths.append(image_path)
            self.embeddings.append(embedding)  


    def showImage(self, image: cv2, mili_sec=0) -> None:
        cv2.imshow("Recognizing Faces", image)
        cv2.waitKey(mili_sec * 1000)
        cv2.destroyAllWindows()